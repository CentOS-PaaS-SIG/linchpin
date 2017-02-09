#!/usr/bin/env python
import os
import xml.etree.ElementTree as eT

from bkr.client import conf, BeakerCommand
from bkr.common.hub import HubProxy
from bkr.common.pyconfig import PyConfigParser
from json import dumps, loads
from time import sleep
from sys import stderr


BEAKER_CONF = \
    (os.environ.get('BEAKER_CONF', '/etc/beaker/client.conf'))
WAIT_TIME = 60


class BeakerTargets(object):
    def __init__(self, params={}, logger=None):
        self.__dict__ = params.copy()
        self.conf = PyConfigParser()
        default_config = os.path.expanduser(BEAKER_CONF)
        self.conf.load_from_file(default_config)
        self.hub = HubProxy(logger=logger, conf=self.conf)

    def _get_url(self, bkr_id):
        """
        Constructs the Beaker URL for the job related to the provided Beaker
        ID. That ID should be all numeric, unless the structure of Beaker
        changes in the future. If that's the case, then the ID should be
        appropriately URL encoded to be appended to the end of a URL properly.
        """
        base = self.conf.get('HUB_URL', '')
        if base == '':
            raise Exception("Unable to construct URL")
        if base[-1] != '/':
            base += '/'
        return base + 'jobs/' + bkr_id

    def get_system_statuses(self):
        """
        Checks on the status of a set of Beaker jobs (ids) and returns their
        hostname once the jobs have reached their defined status.
        """
        attempts = 0
        pass_count = 0
        all_count = len(self.ids)
        while attempts < self.max_attempts:
            job_results = self._check_jobs(self.ids)
            pass_count = 0
            for resource in job_results['resources']:
                result = resource['result']
                status = resource['status']
                print >> stderr, "status: %s, result: %s" % (status, result)
                if status not in ['Cancelled', 'Aborted']:
                    if result == 'Pass' or (result == 'Warn' and self.skip_no_system):
                        pass_count += 1
                    elif result in ['Fail', 'Warn', 'Panic', 'Completed']:
                        raise Exception("System failed with state '{0}'"\
                                .format(result))
                elif status == 'Aborted':
                    if result == 'Warn' and self.skip_no_system:
                        pass_count += 1
                    else:
                        raise Exception("System aborted")
                elif status == 'Cancelled':
                    raise Exception("System canceled")
            attempts += 1
            if pass_count == all_count:
                return job_results['resources']
            sleep(WAIT_TIME)
        raise Exception("{0} system(s) never completed in {1} polling attempts. {2}"\
                .format(all_count - pass_count, attempts, dumps(job_results)))

    def _check_jobs(self, ids):
        """
            Get state of a job in Beaker
        """
        jobs = ["J:" + _id for _id in ids]
        results = {}
        resources = []
        bkrcmd = BeakerCommand('BeakerCommand')
        bkrcmd.check_taskspec_args(jobs)
        for task in jobs:
            myxml = self.hub.taskactions.to_xml(task)
            myxml = myxml.encode('utf8')
            root = eT.fromstring(myxml)
            # TODO: Using getiterator() since its backward compatible
            # with Python 2.6
            # This is deprectated in 2.7 and we should be using iter()
            for job in root.getiterator('job'):
                results.update({'job_id': job.get('id'),
                                'results': job.get('result')})
            for recipe in root.getiterator('recipe'):
                resources.append({'family': recipe.get('family'),
                                  'distro': recipe.get('distro'),
                                  'arch': recipe.get('arch'),
                                  'variant': recipe.get('variant'),
                                  'system': recipe.get('system'),
                                  'status': recipe.get('status'),
                                  'result': recipe.get('result'),
                                  'id': recipe.get('job_id')})
                results.update({'resources': resources})
        return results


def main():
    mod = AnsibleModule(argument_spec={
        'ids': {'type': 'list'},
        'skip_no_system': {'type': 'bool', 'default': False},
        'max_attempts': {'type': 'int', 'default': 60}
    })
    beaker = BeakerTargets(mod.params)
    try:
        results=beaker.get_system_statuses()
        mod.exit_json(hosts=results, changed=True, success=True)
    except Exception as ex:
        mod.fail_json(msg=str(ex))


# import module snippets
from ansible.module_utils.basic import *
main()
