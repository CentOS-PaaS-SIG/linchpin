#!/usr/bin/env python

import os
import ast
import json
import time
import errno
import hashlib

from cerberus import Validator
from uuid import getnode as get_mac
from collections import OrderedDict

from linchpin.ansible_runner import ansible_runner

from linchpin.hooks.state import State
from linchpin.hooks import LinchpinHooks

from linchpin.rundb.basedb import BaseDB
from linchpin.rundb.drivers import DB_DRIVERS

from linchpin.exceptions import ActionError
from linchpin.exceptions import LinchpinError
from linchpin.exceptions import SchemaError
from linchpin.exceptions import TopologyError
from linchpin.exceptions import ValidationError


class LinchpinAPI(object):

    def __init__(self, ctx):
        """
        LinchpinAPI constructor

        :param ctx: context object from context.py

        """

        self.ctx = ctx

        self.hook_state = None
        self._hook_observers = []
        self.playbook_pre_states = self.get_cfg('playbook_pre_states',
                                                {'up': 'preup',
                                                 'destroy': 'predestroy'})
        self.playbook_post_states = self.get_cfg('playbook_post_states',
                                                 {'up': 'postup',
                                                  'destroy': 'postdestroy',
                                                  'postinv': 'inventory'})
        self.hooks = LinchpinHooks(self)

        self.target_data = {}

        base_path = '/'.join(os.path.dirname(__file__).split('/')[0:-1])
        pkg = self.get_cfg(section='lp', key='pkg', default='linchpin')
        lp_path = '{0}/{1}'.format(base_path, pkg)
        self.pb_ext = self.get_cfg('extensions', 'playbooks', default='.yml')

        # get external_provider_path
        xp_path = self.get_cfg('lp',
                               'external_providers_path',
                               default='').split(':')

        pb_path = '{0}/{1}'.format(lp_path,
                                   self.get_evar('playbooks_folder',
                                                 default='provision'))
        self.pb_path = [pb_path]

        for path in xp_path:
            self.pb_path.append(os.path.expanduser(path))

        self.set_evar('lp_path', lp_path)
        self.set_evar('pb_path', self.pb_path)
        self.set_evar('from_api', True)
        self.workspace = self.get_evar('workspace')


    def setup_rundb(self):
        """
        Configures the run database parameters, sets them into extra_vars
        """

        rundb_conn = self.get_cfg(section='lp',
                                  key='rundb_conn')
        rundb_type = self.get_cfg(section='lp',
                                  key='rundb_type',
                                  default='TinyRunDB')
        rundb_conn_type = self.get_cfg(section='lp',
                                       key='rundb_conn_type',
                                       default='file')
        self.rundb_hash = self.get_cfg(section='lp',
                                       key='rundb_hash',
                                       default='sha256')

        if rundb_conn_type == 'file':

            rundb_conn_f = rundb_conn.replace('::mac::', str(get_mac()))
            rundb_conn_f = rundb_conn_f.replace('{{ workspace }}',
                                                self.workspace)
            rundb_conn_f = os.path.realpath(os.path.expanduser(rundb_conn_f))
            rundb_conn_dir = os.path.dirname(rundb_conn_f)

            if not os.path.exists(rundb_conn_dir):
                try:
                    os.makedirs(rundb_conn_dir)
                except OSError as exc:
                    if (exc.errno == errno.EEXIST and
                            os.path.isdir(rundb_conn_dir)):
                        pass
                    else:
                        raise

        self.set_evar('rundb_type', rundb_type)
        self.set_evar('rundb_conn', rundb_conn_f)
        self.set_evar('rundb_hash', self.rundb_hash)

        return BaseDB(DB_DRIVERS[rundb_type], rundb_conn_f)


    def get_cfg(self, section=None, key=None, default=None):
        """
        Get cfgs value(s) by section and/or key, or the whole cfgs object

        :param section: section from ini-style config file

        :param key: key to get from config file, within section

        :param default: default value to return if nothing is found.
        """

        return self.ctx.get_cfg(section=section, key=key, default=default)


    def set_cfg(self, section, key, value):
        """
        Set a value in cfgs. Does not persist into a file,
        only during the current execution.

        :param section: section within ini-style config file

        :param key: key to use

        :param value: value to set into section within config file
        """

        self.ctx.set_cfg(section, key, value)


    def get_evar(self, key=None, default=None):
        """
        Get the current evars (extra_vars)

        :param key: key to use

        :param default: default value to return if nothing is found
        (default: None)
        """

        return self.ctx.get_evar(key=key, default=default)


    def set_evar(self, key, value):
        """
        Set a value into evars (extra_vars). Does not persist into a file,
        only during the current execution.

        :param key: key to use

        :param value: value to set into evars
        """

        self.ctx.set_evar(key, value)


    @property
    def hook_state(self):
        """
        getter function for hook_state property of the API object
        """

        return self.hook_state


    @hook_state.setter
    def hook_state(self, hook_state):
        """
        hook_state property setter , splits the hook_state string in
        subhook_state and sets linchpin.hook_state object

        :param hook_state: valid hook_state string mentioned in linchpin.conf
        """

        # call run_hooks after hook_state is being set
        if hook_state is None:
            return
        else:
            self.ctx.log_debug('hook {0} initiated'.format(hook_state))
            self._hook_state = State(hook_state, None, self.ctx)

            for callback in self._hook_observers:
                callback(self._hook_state)


    def bind_to_hook_state(self, callback):
        """
        Function used by LinchpinHooksclass to add callbacks

        :param callback: callback function
        """

        self._hook_observers.append(callback)


    def lp_journal(self, view='target', targets=[],
                   fields=None, count=1, tx_ids=None):

        rundb = self.setup_rundb()

        journal = {}

        if not len(targets):
            targets = rundb.get_tables()

        if view == 'target':
            # initialize rundb table
            dateformat = self.get_cfg('logger',
                                      'dateformat',
                                      default='%m/%d/%Y %I:%M:%S %p')
            for target in targets:
                tgt_records = rundb.get_records(table=target, count=count)

                if fields and 'start' in fields:
                    for run_id, record in tgt_records.iteritems():
                        st = record.get('start')
                        strt = float(st) if len(st) else float(1000000000.0)
                        start = time.localtime(strt)
                        record['start'] = time.strftime(dateformat, start)

                if fields and 'end' in fields:
                    for run_id, record in tgt_records.iteritems():
                        en = record.get('end')
                        endt = float(st) if len(en) else float(1000000000.0)
                        end = time.localtime(endt)
                        record['end'] = time.strftime(dateformat, end)


                journal[target] = tgt_records
        if view == 'tx':
            if len(tx_ids):
                journal = rundb.get_tx_records(tx_ids)
            else:
                journal = rundb.get_records('linchpin', count=count)

        return journal


    def _find_playbook_path(self, playbook):

        for path in self.pb_path:
            p = '{0}/{1}{2}'.format(path, playbook, self.pb_ext)

            if os.path.exists(os.path.expanduser(p)):
                return path

        raise LinchpinError("playbook '{0}' not found in"
                            " path: {1}".format(playbook, self.pb_path))


    def _fix_broken_topologies(self, res_grp, res_grp_type):
        """
        Because the new tooling requires resource_definitions, both beaker
        and openshift didn't previously suport this section in topologies.
        This function is called if resource_definitions are not included
        in the topology. The topology will be given a resource_definitions
        section.

        :param res_grp: The resource group to update

        :param res_grp_type: Which type to convert (this may not matter)
        """

        res_defs = {}
        # with beaker, there will only be one
        # resource_definition upon conversion
        if res_grp_type == 'beaker':
            res_defs['role'] = 'bkr_server'
            res_defs['whiteboard'] = res_grp.pop('whiteboard',
                                                 'Provisioned with LinchPin')
            res_defs['job_group'] = res_grp.pop('job_group')
            res_defs['recipesets'] = res_grp.pop('recipesets')
            res_defs['cancel_message'] = res_grp.pop('cancel_message',
                                                     'Canceled by LinchPin')
            res_defs['max_attempts'] = res_grp.pop('max_attempts', 60)
            res_defs['attempt_wait_time'] = res_grp.pop('attempt_wait_time',
                                                        60)
            res_grp['resource_definitions'] = [res_defs]

            return res_grp

        if res_grp_type == 'openshift':
            res_defs = res_grp.pop('resources')

            count = 0
            for res in res_defs:
                res['name'] = 'openshift-res_{0}'.format(str(count))
                count += 1
                if res.get('inline_data'):
                    res['role'] = 'openshift_inline'
                    res['data'] = res.pop('inline_data')
                if res.get('file_reference'):
                    res['role'] = 'openshift_external'
                    res['filiename'] = res.pop('file_reference')

            res_grp['resource_definitions'] = res_defs

            # the old openshift role put credentials in the
            # resource group definition. Moving to credentials
            creds = {}
            creds['api_endpoint'] = res_grp.pop('api_endpoint')
            creds['api_token'] = res_grp.pop('api_token')
            res_grp['credentials'] = creds

            return res_grp


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

    def _convert_layout(self, layout_data):
        """
        Convert the layout to retain order of the layout hosts
        ;param layout_data: layout_data
        """
        layout_json = layout_data
        layout_hosts = []
        ihosts = layout_data["inventory_layout"]["hosts"]
        for k in ihosts:
            layout_host = {}
            layout_host["name"] = k
            for key in ihosts[k]:
                layout_host[key] = ihosts[k][key]
            layout_hosts.append(layout_host)
        layout_json["inventory_layout"]["hosts"] = layout_hosts
        return layout_json


    def _validate_topology(self, topology):
        """
        Validate the provided topology against the schema

        ;param topology: topology dictionary
        """

        res_grps = topology.get('resource_groups')
        resources = []

        for group in res_grps:
            res_grp_type = (group.get('resource_group_type') or
                            group.get('res_group_type'))

            pb_path = self._find_playbook_path(res_grp_type)

            try:
                sp = "{0}/roles/{1}/files/schema.json".format(pb_path,
                                                              res_grp_type)

                schema = json.load(open(sp))
            except Exception as e:
                raise LinchpinError("Error with schema: '{0}'"
                                    " {1}".format(sp, e))

            res_defs = group.get('resource_definitions')

            # preload this so it will validate against the schema
            document = {'res_defs': res_defs}
            v = Validator(schema)

            if not v.validate(document):
                raise SchemaError('Schema validation failed:'
                                  ' {0}'.format(v.errors))

            resources.append(group)

        return resources


    def get_pf_data_from_rundb(self, targets, run_id=None, tx_id=None):
        """
        This function takes the action and provision_data, returns the
        pinfile data

        :param targets: A list of targets for which to get the data

        :param targets: Tuple of target(s) for which to gather data.

        :param run_id: run_id associated with target (Default: None)

        :param tx_id: tx_id for which to gather data (Default: None)
        """

        rundb = self.setup_rundb()

        if run_id and tx_id:
            raise ActionError("'run_id' and 'tx_id' are mutually exclusive")

        pf_data = {}
        pinfile = OrderedDict()

        if run_id:
            for target in targets:
                pf_data[target] = rundb.get_record(target,
                                                   action='up',
                                                   run_id=run_id)
        if tx_id:
            record = rundb.get_tx_record(tx_id)

            if not record or not len(record):
                return None

            if len(targets):
                for tgts in record['targets']:
                        for tgt, data in tgts.iteritems():
                            run_id = int(data.keys()[0])
                            if tgt in targets:
                                tgt_data = (rundb.get_record(tgt,
                                            action=record['action'],
                                            run_id=run_id))
                                pf_data[tgt] = tgt_data
            else:
                for tgts in record['targets']:
                    for tgt, data in tgts.iteritems():
                        run_id = int(data.keys()[0])
                        tgt_data = (rundb.get_record(tgt,
                                    action=record['action'],
                                    run_id=run_id))
                        pf_data[tgt] = tgt_data


        for t, data in pf_data.iteritems():
            topo_data = data[0]['inputs'][0].get('topology_data')
            layout_data = data[0]['inputs'][0].get('layout_data')
            hooks_data = data[0]['inputs'][0].get('hooks_data')

            pinfile[t] = {}
            pinfile[t]['topology'] = topo_data
            pinfile[t]['run_id'] = data[1]
            if layout_data:
                pinfile[t]['layout'] = layout_data
            if hooks_data:
                pinfile[t]['hooks'] = hooks_data

        return pinfile


    def do_action(self, provision_data, action='up', run_id=None, tx_id=None):
        """
        This function takes provision_data, and executes the given
        action for each target within the provision_data disctionary.

        :param provision_data: PinFile data as a dictionary, with
        target information

        :param action: Action taken (up, destroy, etc). (Default: up)

        :param run_id: Provided run_id to duplicate/destroy (Default: None)

        :param tx_id: Provided tx_id to duplicate/destroy (Default: None)

        .. .note:: The `run_id` value differs from the `rundb_id`, in that
                   the `run_id` is an existing value in the database.
                   The `rundb_id` value is created to store the new record.
                   If the `run_id` is passed, it is used to collect an existing
                   `uhash` value from the given `run_id`, which is in turn used
                   to perform an idempotent reprovision, or destroy provisioned
                   resources.
        """

        ansible_console = False
        if self.ctx.cfgs.get('ansible'):
            ansible_console = (
                ast.literal_eval(self.get_cfg('ansible',
                                              'console',
                                              default='False')))

        if not ansible_console:
            ansible_console = bool(self.ctx.verbosity)

        results = {}


        return_code = 99

        for target in provision_data.keys():
            if not isinstance(provision_data[target], dict):
                raise LinchpinError("Target '{0}' does not"
                                    " exist.".format(target))

        targets = [x.lower() for x in provision_data.keys()]
        if 'linchpin' in targets:
            raise LinchpinError("Target 'linchpin' is not allowed.")

        for target in provision_data.keys():

            self.ctx.log_debug("Processing target: {0}".format(target))

            results[target] = {}
            self.set_evar('target', target)

            rundb = self.setup_rundb()

            if tx_id:
                record = rundb.get_tx_record(tx_id)
                run_id = (record['targets'][0][target].keys()[0])


            rundb_schema = json.loads(self.get_cfg(section='lp',
                                      key='rundb_schema'))
            rundb.schema = rundb_schema
            self.set_evar('rundb_schema', rundb_schema)

            start = time.time()
            st_uhash = int(start * 1000)
            uhash = None

            # generate a new rundb_id
            # (don't confuse it with an already existing run_id)
            rundb_id = rundb.init_table(target)
            orig_run_id = rundb_id

            uhash_length = self.get_cfg('lp', 'rundb_uhash_length')
            uhash_len = int(uhash_length)
            if not run_id:
                uh = hashlib.new(self.rundb_hash,
                                 ':'.join([target, str(tx_id),
                                          str(rundb_id), str(st_uhash)]))
                uhash = uh.hexdigest()[:uhash_len]

            if action == 'destroy' or run_id:
                # look for the action='up' records to destroy
                data, orig_run_id = rundb.get_record(target,
                                                     action='up',
                                                     run_id=run_id)

                if data:
                    uhash = data.get('uhash')
                    self.ctx.log_debug("using data from"
                                       " run_id: {0}".format(run_id))

            elif action not in ['up', 'destroy']:
                # it doesn't appear this code will will execute,
                # but if it does...
                raise LinchpinError("Attempting '{0}' action on"
                                    " target: '{1}' failed. Not an"
                                    " action.".format(action, target))


            self.ctx.log_debug('rundb_id: {0}'.format(rundb_id))
            self.ctx.log_debug('uhash: {0}'.format(uhash))

            rundb.update_record(target, rundb_id, 'uhash', uhash)
            rundb.update_record(target, rundb_id, 'start', str(start))
            rundb.update_record(target, rundb_id, 'action', action)

            self.set_evar('orig_run_id', orig_run_id)
            self.set_evar('rundb_id', rundb_id)
            self.set_evar('uhash', uhash)

            topology_data = provision_data[target].get('topology')

            # if validation fails the first time, convert topo from old -> new
            try:
                resources = self._validate_topology(topology_data)
            except SchemaError:
                # if topology fails, try converting from old to new style
                try:
                    self._convert_topology(topology_data)
                    resources = self._validate_topology(topology_data)
                except SchemaError:
                    raise ValidationError("Topology '{0}' does not"
                                          " validate".format(topology_data))

            self.set_evar('topo_data', topology_data)
            self.set_evar('resources', resources)

            rundb.update_record(target,
                                rundb_id,
                                'inputs',
                                [
                                    {'topology_data':
                                     provision_data[target]['topology']}
                                ])

            if provision_data[target].get('layout', None):
                l_data = provision_data[target]['layout']
                provision_data[target]['layout'] = self._convert_layout(l_data)
                self.set_evar('layout_data', provision_data[target]['layout'])

                rundb.update_record(target,
                                    rundb_id,
                                    'inputs',
                                    [
                                        {'layout_data':
                                         provision_data[target]['layout']}
                                    ])

            if provision_data[target].get('hooks', None):
                hooks_data = provision_data[target].get('hooks')
                self.set_evar('hooks_data', hooks_data)
                rundb.update_record(target,
                                    rundb_id,
                                    'inputs',
                                    [
                                        {'hooks_data':
                                         provision_data[target]['hooks']}
                                    ])

            if provision_data[target].get('cfgs', None):
                vars_data = provision_data[target].get('cfgs')
                self.set_evar('cfgs_data', vars_data)
                rundb.update_record(target,
                                    rundb_id,
                                    'cfgs',
                                    [
                                        {'user':
                                         provision_data[target]['cfgs']}
                                    ])

            # note : changing the state triggers the hooks
            self.hooks.rundb = (rundb, rundb_id)
            self.pb_hooks = self.get_cfg('hookstates', action)
            self.ctx.log_debug('calling: {0}{1}'.format('pre', action))

            if 'pre' in self.pb_hooks:
                self.hook_state = '{0}{1}'.format('pre', action)

            # FIXME need to add rundb data for hooks results

            # invoke the appropriate action
            return_code, results[target]['task_results'] = (
                self._invoke_playbooks(resources, action=action,
                                       console=ansible_console)
            )

            if not return_code:
                self.ctx.log_state("Action '{0}' on Target '{1}' is "
                                   "complete".format(action, target))

            # FIXME Check the result[target] value here, and fail if applicable.
            # It's possible that a flag might allow more targets to run, then
            # return an error code at the end.

            # add post provision hook for inventory generation
            if 'inv' in self.pb_hooks:
                self.hook_state = 'postinv'

            if 'post' in self.pb_hooks:
                self.hook_state = '{0}{1}'.format('post', action)

            end = time.time()

            rundb.update_record(target, rundb_id, 'end', str(end))
            rundb.update_record(target, rundb_id, 'rc', return_code)

            run_data = rundb.get_record(target,
                                        action=action,
                                        run_id=rundb_id)

            results[target]['rundb_data'] = {rundb_id: run_data[0]}


        # generate the linchpin_id and structure
        lp_schema = ('{"action": "", "targets": []}')

        rundb = self.setup_rundb()
        rundb.schema = json.loads(lp_schema)
        lp_id = rundb.init_table('linchpin')

        summary = {}

        for target, data in results.iteritems():
            for k, v in data['rundb_data'].iteritems():
                summary[target] = {k: {'rc': v['rc'], 'uhash': v['uhash']}}

        rundb.update_record('linchpin', lp_id, 'action', action)
        rundb.update_record('linchpin', lp_id, 'targets', [summary])

        lp_data = {lp_id: {'action': action,
                           'summary_data': summary,
                           'results_data': results}}

        return (return_code, lp_data)


    def get_run_data(self, tx_id, fields, targets=()):
        """
        Returns the RunDB for data from a specified field given a tx_id.
        The fields consist of the major sections in the RunDB (target
        view only). Those fields are action, start, end, inputs, outputs,
        uhash, and rc.

        :param tx_id: tx_id to search
        :param fields: Tuple of fields to retrieve for each record requested.
        :param targets: Tuple of targets to search from within the tx_ids
        """

        rundb = self.setup_rundb()

        tgt_run_ids = {}
        target_data = {}

        record = rundb.get_tx_record(tx_id)

        if not record or not len(record):
            return None


        # get run_ids to query
        if len(targets):
            for tgts in record['targets']:
                    for tgt, data in tgts.iteritems():
                        if tgt in targets:
                            tgt_run_ids[tgt] = int(data.keys()[0])
        else:
            for tgts in record['targets']:
                for tgt, data in tgts.iteritems():
                    tgt_run_ids[tgt] = int(data.keys()[0])

        for target, run_id in tgt_run_ids.iteritems():
            record = rundb.get_record(target, run_id=run_id, action='up')
            field_data = {}
            single_value_fields = ('action', 'start', 'end', 'rc', 'uhash')

            for field in fields:
                f = record[0].get(field)
                if f:
                    if field in single_value_fields:
                        field_data[field] = f
                    else:
                        data_array = {}
                        for fld in f:
                            for k, v in fld.iteritems():
                                if field == 'outputs':
                                    values = []
                                    for value in v:
                                        values.append(value)
                                    data_array[k] = values
                                else:
                                    data_array[k] = v

                            field_data[field] = data_array

            target_data[target] = field_data

        return target_data


    def _invoke_playbooks(self, resources, action='up', console=True):
        """
        Uses the Ansible API code to invoke the specified linchpin playbook

        :param resources: dict of resources to provision
        :param action: Which ansible action to run (default: 'up')
        :param console: Whether to display the ansible console (default: True)
        """

        return_code = 0
        results = []

        self.set_evar('_action', action)
        self.set_evar('state', 'present')

        if action == 'destroy':
            self.set_evar('state', 'absent')

        for resource in resources:
            playbook = resource.get('resource_group_type')
            pb_path = self._find_playbook_path(playbook)
            playbook_path = '{0}/{1}{2}'.format(pb_path, playbook, self.pb_ext)

            module_paths = []
            module_folder = self.get_cfg('lp',
                                         'module_folder',
                                         default='library')

            for path in reversed(self.pb_path):
                module_paths.append('{0}/{1}/'.format(path, module_folder))

            extra_vars = self.get_evar()
            inventory_src = '{0}/localhost'.format(self.workspace)

            verbosity = self.ctx.verbosity
            return_code, res = ansible_runner(playbook_path,
                                              module_paths,
                                              extra_vars,
                                              inventory_src=inventory_src,
                                              verbosity=verbosity,
                                              console=console)

            if res:
                results.append(res)


        if not len(results):
            results = None

        return (return_code, results)
