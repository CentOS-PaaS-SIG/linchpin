#!/usr/bin/env python
import os

from time import sleep
from sys import stderr
import xml.etree.ElementTree as eT
from ansible.module_utils.basic import AnsibleModule

from bkr.client import BeakerCommand
from bkr.common.hub import HubProxy
from bkr.common.pyconfig import PyConfigParser


BEAKER_CONF = os.environ.get('BEAKER_CONF', '/etc/beaker/client.conf')


def _jprefix(job_ids):
    return ["J:" + _id for _id in job_ids]


class BeakerTargets(object):
    def __init__(self, params, logger=None):
        # params from AnsibleModule argument_spec below
        self.ids = params['ids']
        provision_params = params['provision_params']

        # Set wait methods from provision params, with reasonable defaults
        self.wait_time = provision_params.get('attempt_wait_time', 60)
        self.max_attempts = provision_params.get('max_attempts', 60)

        # set up beaker connection
        self.conf = PyConfigParser()
        default_config = os.path.expanduser(BEAKER_CONF)
        self.conf.load_from_file(default_config)
        self.hub = HubProxy(logger=logger, conf=self.conf)

    def get_system_statuses(self):
        """
        Checks on the status of a set of Beaker jobs (ids) and returns their
        hostname once the jobs have reached their defined status.
        """
        attempts = 0
        while attempts < self.max_attempts:
            job_results, all_count = self._check_jobs()
            pass_count = 0
            for resource in job_results:
                result = resource['result']
                status = resource['status']
                print >> stderr, "status: %s, result: %s" % (status, result)
                if status not in ['Cancelled', 'Aborted']:
                    if result == 'Pass':
                        pass_count += 1
                    elif result in ['Fail', 'Warn', 'Panic', 'Completed']:
                        self._cancel_jobs()
                        raise Exception("System failed with state"
                                        " '{0}'".format(result))
                elif status == 'Aborted':
                    self._cancel_jobs()
                    raise Exception("System aborted")
                elif status == 'Cancelled':
                    self._cancel_jobs()
                    raise Exception("System canceled")
            attempts += 1
            if pass_count == all_count:
                return job_results
            sleep(self.wait_time)

        # max attempts exceeded, cancel jobs and fail
        self._cancel_jobs('Provision request timed out')
        # Fail with error msg, include results from last attempt to include
        # in topology outputs even if provisioning failed so a destroy still
        # cancels jobs
        msg = ("{0} system(s) never completed in {1} polling attempts, jobs "
               "have been cancelled: {2}".format(
                   all_count - pass_count, attempts, ', '.join(self.ids)))
        raise Exception(msg, job_results)

    def _check_jobs(self):
        """
            Get state of a job in Beaker
        """
        jobs = _jprefix(self.ids)
        resources = []
        bkrcmd = BeakerCommand('BeakerCommand')
        bkrcmd.check_taskspec_args(jobs)
        for task in jobs:
            myxml = self.hub.taskactions.to_xml(task)
            myxml = myxml.encode('utf8')
            root = eT.fromstring(myxml)
            # Using getiterator() since its backward compatible with py26
            for recipe in root.getiterator('recipe'):
                resources.append({'family': recipe.get('family'),
                                  'distro': recipe.get('distro'),
                                  'arch': recipe.get('arch'),
                                  'variant': recipe.get('variant'),
                                  'system': recipe.get('system'),
                                  'status': recipe.get('status'),
                                  'result': recipe.get('result'),
                                  'rid': recipe.get('id'),
                                  'id': recipe.get('job_id')})
        return resources, len(resources)

    def _cancel_jobs(self, msg='Unabled to provision system(s)'):
        for job_id in _jprefix(self.ids):
            self.hub.taskactions.stop(job_id, 'cancel', msg)

def main():
    mod = AnsibleModule(argument_spec={
        'ids': {'type': 'dict'},
        'provision_params': {'type': 'dict'},
    })
    beaker = BeakerTargets(mod.params)
    try:
        if len(beaker.ids) > 1:
            mod.warn('When using multiple resource_definitions for beaker '
                     'resources, only the provisioning parameters '
                     '(max_attempts, attempt_wait_time) from the first '
                     'resource_definition will be used. Consider using a '
                     'single resource_definition with multiple recipes or '
                     'recipesets instead.')
        results = beaker.get_system_statuses()
        mod.exit_json(hosts=results, changed=True)
    except Exception as ex:
        msg = ": For more details please check jobs on beaker"
        msg = str(ex) + msg
        mod.fail_json(msg=msg, changed=True)


# import module snippets
main()
