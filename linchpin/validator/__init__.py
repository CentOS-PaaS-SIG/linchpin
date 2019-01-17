#!/usr/bin/env python

import os
import json

from linchpin.exceptions import ValidationError
from linchpin.exceptions import ValidationErrorHandler
from linchpin.exceptions import SchemaError
from linchpin.exceptions import LinchpinError
from linchpin.exceptions import TopologyError

from linchpin.validator.anyofvalidator import AnyofValidator


class Validator(object):
    SECTIONS = ['topology', 'layout', 'cfgs', 'hooks']

    def __init__(self, ctx, pb_path, pb_ext):
        self.ctx = ctx
        self.pb_path = pb_path
        self.pb_ext = pb_ext


    def validate(self, target, old_schema=False):
        """
        Attemptes to validate a single target in a PinFile

        Returns the groups returned when the topology is validated

        :param target: the target being validated

        :param old_schema: whether or not to validate using the old schema
                           by default
        """

        for field in target.keys():
            if field not in Validator.SECTIONS:
                raise ValidationError("Section '{0}' not a valid top-level "
                                      "PinFile section. valid sections "
                                      "are '{1}'".format(target,
                                                         Validator.SECTIONS))
        if 'topology' not in target.keys():
            raise ValidationError("Each target must have a topology")

        topo_data = target['topology']
        try:
            resources = self.validate_topology(topo_data)
        except (SchemaError, KeyError):
            # if topology fails, try converting from old to new style
            self._convert_topology(topo_data)
            resources = self.validate_topology(topo_data)
        if 'layout' in target.keys():
            self.validate_layout(target['layout'])
        if 'cfgs' in target.keys():
            self.validate_cfgs(target['cfgs'])

        return resources


    def validate_pretty(self, target, name, old_schema=False):
        results = {}
        return_code = 0

        for field in target.keys():
            if field not in Validator.SECTIONS:
                raise ValidationError("Section '{0}' not a valid top-level "
                                      "PinFile section. valid sections "
                                      "are '{1}'".format(target,
                                                         Validator.SECTIONS))
        if 'topology' not in target.keys():
            results['topology'] = "Each target must have a topology"

        err_prefix = "errors:\n"
        topo_data = target['topology']
        try:
            self.validate_topology(topo_data)
        except (SchemaError, KeyError) as e:
            # if topology fails, try converting from old to new style
            try:
                self._convert_topology(topo_data)
                self.validate_topology(topo_data)
            except SchemaError as s:
                if old_schema:
                    # add a tab to the beginning of each line in the
                    # SchemaError and append to the existing error message
                    error = self._format_error(err_prefix, s)
                else:
                    if type(e) == KeyError:
                        error = "\tfield res_defs['type'] is no longer "\
                                "supported.  Please use 'role' instead"
                        error = self._format_error(err_prefix, e)
                    else:
                        error = self._format_error(err_prefix, e)
                results['topology'] = error
                return_code += 1
            else:
                results['topology'] = "valid under old schema"
        except TopologyError as t:
            error = self._format_error(err_prefix, t)
            results['topology'] = error
            return_code += 1
        else:
            results['topology'] = "valid"

        if 'layout' in target.keys():
            layout_data = target['layout']
            try:
                self.validate_layout(layout_data)
            except SchemaError as e:
                error = self._format_error(err_prefix, e)
                results['layout'] = error + '\n'
            else:
                results['layout'] = "valid"

        if 'cfgs' in target.keys():
            cfgs_data = target['cfgs']
            try:
                self.validate_cfgs(cfgs_data)
            except SchemaError as e:
                error = self._format_error(err_prefix, e)
                results['cfgs'] = error + '\n'
            else:
                results['cfgs'] = "valid"

        return return_code, results


    def _format_error(self, error, e):
        for line in iter(str(e).splitlines(True)):
            error += "\t" + line
        return error


    def validate_topology(self, topo_data):
        """
        Validate the provided topology against the schema

        ;param topo_data: topology dictionary
        """

        # validate high-level topology-components
        self.validate_topology_highlevel(topo_data)

        # validate each resource group
        res_grps = topo_data.get('resource_groups')
        resources = []
        for group in res_grps:
            self.validate_resource_group(group)
            resources.append(group)

        return resources


    def validate_topology_highlevel(self, topo_data):
        """
        validate the higher-level components of the topology

        These are not specific to the provider and must be validated separately
        from the items within each resource group

        :param topo_data topology data from the pinfile
        """

        pb_path = self._find_playbook_path("layout")
        try:
            sp = "{0}/roles/common/files/topo-schema.json".format(pb_path)
            schema = json.load(open(sp))
        except Exception as e:
            raise LinchpinError("Error with schema: '{0}'"
                                " {1}".format(sp, e))

        document = {'topology': topo_data}
        v = AnyofValidator(schema, error_handler=ValidationErrorHandler)

        if not v.validate(document):
            try:
                err = self._gen_error_msg("", "", v.errors)
                raise TopologyError(err)
            except NotImplementedError as e:
                # we shouldn't have this issue using cererus >= 1.2, but
                # this is here just in case an older version has to be used
                self.ctx.log_state("There was an error validating your schema,\
                      but we can't seem to format it for you")
                self.ctx.log_state("Here's the raw error data in case you want\
                      to go through it by hand:")
                self.ctx.log_state(v._errors)


    def validate_resource_group(self, res_grp):
        """
        validate the provided resource group against the schema

        :param res_grp: resource group
        """
        res_grp_type = (res_grp.get('resource_group_type') or
                        res_grp.get('res_group_type'))

        pb_path = self._find_playbook_path(res_grp_type)

        try:
            sp = "{0}/roles/{1}/files/schema.json".format(pb_path,
                                                          res_grp_type)
            schema = json.load(open(sp))
        except Exception as e:
            raise LinchpinError("Error with schema: '{0}'"
                                " {1}".format(sp, e))

        res_defs = res_grp.get('resource_definitions')

        # preload this so it will validate against the schema
        document = {'res_defs': res_defs}
        v = AnyofValidator(schema,
                           error_handler=ValidationErrorHandler)

        if not v.validate(document):
            try:
                err = self._gen_error_msg("", "", v.errors)
                raise SchemaError(err)
            except NotImplementedError as e:
                # we shouldn't have this issue using cererus >= 1.2, but
                # this is here just in case an older version has to be used
                self.ctx.log_state("There was an error validating your schema,\
                      but we can't seem to format it for you")
                self.ctx.log_state("Here's the raw error data in case you want\
                      to go through it by hand:")
                self.ctx.log_state(v._errors)

        return res_grp


    def validate_layout(self, layout_data):
        """
        Validate the provided layout against the schema

        :param layout: layout dictionary
        """

        pb_path = self._find_playbook_path("layout")
        try:
            sp = "{0}/roles/common/files/schema.json".format(pb_path)

            schema = json.load(open(sp))
        except Exception as e:
            raise LinchpinError("Error with schema: '{0}' {1}".format(e))

        v = AnyofValidator(schema)

        if not v.validate(layout_data):
            raise SchemaError('Schema validation failed: {0}'.format(v.errors))


    def validate_cfgs(self, cfgs_data):
        pass


    def _find_playbook_path(self, playbook):
        """
        returns the full path to a given playbook

        :params playbook: name of the playbook
        """

        for path in self.pb_path:
            p = '{0}/{1}{2}'.format(path, playbook, self.pb_ext)

            if os.path.exists(os.path.expanduser(p)):
                return path

        raise LinchpinError("playbook '{0}' not found in"
                            " path: {1}".format(playbook, self.pb_path))


    def _gen_error_msg(self, prefix, section, error):
        """
        Recursively generate a nicely-formatted validation error

        :param prefix:

        :param section: the section in which the error occured

        :param error: the error message itself
        """

        # set the prefix for this subtree
        if section != "":
            if prefix != "":
                prefix += '[' + str(section) + ']'
            else:
                prefix = str(section)

        if isinstance(error, str):
            if prefix == "":
                return error
            return prefix + ": " + error + os.linesep
        elif isinstance(error, list):
            msg = ""
            for i, e in enumerate(error):
                # we don't need to change the prefix here
                msg += self._gen_error_msg(prefix, "", e)
            return msg
        else:
            # in this case, error is a dict
            msg = ""
            for key, val in error.iteritems():
                msg += self._gen_error_msg(prefix, key, val)
            return msg


    def _convert_topology(self, topology):
        """
        For backward compatiblity, convert the old topology format
        into the new format. Should be pretty straightforward and simple.

        ;param topology: topology dictionary
        """
        try:
            res_grps = topology.get('resource_groups')
            if res_grps:
                for res_grp in res_grps:
                    if 'res_group_type' in res_grp.keys():
                        res_grp['resource_group_type'] = (
                            res_grp.pop('res_group_type'))

                    if 'res_defs' in res_grp.keys():
                        res_grp['resource_definitions'] = (
                            res_grp.pop('res_defs'))

                    res_defs = res_grp.get('resource_definitions')
                    if not res_defs:
                        # this means it's either a beaker or openshift topology
                        res_grp_type = res_grp.get('resource_group_type')

                        res_group = self._fix_broken_topologies(res_grp,
                                                                res_grp_type)
                        res_defs = res_group.get('resource_definitions')
                        res_grp['resource_definitions'] = res_defs

                    if res_defs:
                        for res_def in res_defs:
                            if 'res_name' in res_def.keys():
                                res_def['name'] = res_def.pop('res_name')
                            if 'type' in res_def.keys():
                                res_def['role'] = res_def.pop('type')
                            if 'res_type' in res_def.keys():
                                res_def['role'] = res_def.pop('res_type')
                            if 'count' in res_def.keys():
                                res_def['count'] = int(res_def.pop('count'))
                    else:
                        raise TopologyError("'resource_definitions' do not"
                                            " validate in topology"
                                            " ({0})".format(topology))
            else:
                raise TopologyError("'resource_groups' do not validate"
                                    " in topology ({0})".format(topology))

        except Exception:
            raise LinchpinError("Unknown error converting schema. Check"
                                " template data")
