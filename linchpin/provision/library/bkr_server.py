import os
import sys
import logging

import xml.dom.minidom
import xml.etree.ElementTree as eT

from bkr.client import BeakerCommand, BeakerWorkflow, BeakerJob
from bkr.client import BeakerRecipeSet, BeakerRecipe
from bkr.common.hub import HubProxy
from bkr.common.pyconfig import PyConfigParser

from ansible.module_utils.basic import AnsibleModule

# WANT_JSON
# We want JSON input from Ansible. Please give it to us

LOG = logging.getLogger(__name__)
BEAKER_CONF = \
    (os.environ.get('BEAKER_CONF', '/etc/beaker/client.conf'))


class BkrConn(object):
    """
        Make connection to Beaker
    """
    enabled = True
    doc = xml.dom.minidom.Document()

    def __init__(self, logger=None, conf=None, **kwargs):
        self.conf = PyConfigParser()
        default_config = os.path.expanduser(BEAKER_CONF)
        self.conf.load_from_file(default_config)
        self.hub = HubProxy(logger=logger, conf=self.conf, **kwargs)


class BkrFactory(BkrConn):
    """
        Simple way to provision a job to the Beaker scheduler
    """
    def __init__(self, *args, **kwargs):
        super(BkrFactory, self).__init__(*args, **kwargs)

    def provision(self, *args, **kwargs):
        """
            provision resources in Beaker
        """
        # Break down kwargs for debug, dryrun, recipesets, and whiteboard
        debug = kwargs.get("debug", False)
        dryrun = kwargs.get("dryrun", False)
        recipesets = kwargs.get("recipesets", [])
        keys_path = kwargs.get('ssh_keys_path', '')

        # Create Job
        job = BeakerJob(*args, **kwargs)

        # Add All Host Requirements
        for recipeset in recipesets:
            kwargs = self.create_recipesets(recipeset, **kwargs)
            family = kwargs.get("family", None)
            distro = kwargs.get("distro", None)
            task_params = kwargs.get("taskparam", [])
            # tasks are list of dictionaries which follows format
            # for beaker in a box
            # tasks = [ {arches:[], 'name': '/distribution/utils/dummy'}]
            # for beaker production
            # tasks = [ {arches:[], 'name': '/distribution/dummy'}]
            tasks = kwargs.get("tasks",
                               [{'arches': [], 'name': '/distribution/dummy'}])
            arch = kwargs.get("arch", "x86_64")
            ks_meta = kwargs.get("ks_meta", "")
            method = kwargs.get("method", "nfs")
            priority = kwargs.get("priority", "Normal")
            hostrequires = kwargs.get("hostrequires", [])
            reserve_duration = kwargs.get("reserve_duration", None)
            if reserve_duration:
                kwargs.update({"reserve_duration": "%s" % reserve_duration})
            tags = kwargs.get("tags", [])
            if tags:
                kwargs.update({"tag": tags})
            repos = kwargs.get("repos", [])
            baseurls = []
            for repo in repos:
                if "baseurl" in repo:
                    baseurls.append(repo.get("baseurl"))
            else:
                kwargs.update({"repo": baseurls})
            ks_append = kwargs.get("ks_append", [])
            ssh_key = kwargs.get("ssh_key", [])

            for key_file in kwargs.get("ssh_key_file", []):
                file_path = os.path.join(keys_path, key_file)
                try:
                    with open(file_path, "r") as f:
                        ssh_key.append(f.read())
                except:
                    LOG.info("Unable to read from ssh key file: %s" % file_path)

            if ssh_key:
                ks_append.append("""%%post
mkdir -p /root/.ssh
cat >>/root/.ssh/authorized_keys << "__EOF__"
%s
__EOF__
restorecon -R /root/.ssh
chmod go-w /root /root/.ssh /root/.ssh/authorized_keys
%%end""" % '\n'.join(ssh_key))
                kwargs.update({"ks_append": ks_append})

            requested_tasks = []

            # adding arches=[] to every task definition
            for task in tasks:
                if not('arches' in task.keys()):
                    task['arches'] = []
                requested_tasks.append(task)

            # Tasks and harnesses
            if 'harness' in ks_meta:
                # Disable report plugins
                task_params.append("RSTRNT_DISABLED=01_dmesg_check "
                                   "10_avc_check")

                # Reserve the system after its installed
                kwargs.update({"reserve": True})
            else:
                requested_tasks.append({'arches': [],
                                        'name': '/distribution/reservesys'})
                if reserve_duration:
                    task_params.append("RESERVETIME=%s" % reserve_duration)

            # Update defaults
            kwargs.update({"suppress_install_task": True})
            kwargs.update({"method": method})
            kwargs.update({"priority": priority})

            # Must have family or distro
            if not family and not distro and not arch:
                sys.stderr.write("No Family or Distro and arch specified\n")
                sys.exit(1)

            if not requested_tasks:
                sys.stderr.write("You must specify a task to run\n")
                sys.exit(1)

            # Create Workflow
            wrkflow = BeakerWorkflow('BeakerWorkflow')

            # Create Base Recipe
            recipe_template = BeakerRecipe(*args, **kwargs)

            # Add Host Requirements
            for requirement in hostrequires:
                if 'force' in requirement:
                    # hostRequires element is created by BeakerRecipe, use it
                    hostrequires_node = recipe_template.node.getElementsByTagName('hostRequires')[0]  # noqa E501
                    # all other filters are ignored if the hostname is forced,
                    # so the use of 'force' is mutually exclusive with the use
                    # of any other 'hostRequires' filters
                    hostrequires_node.setAttribute('force',
                                                   requirement['force'])
                elif 'rawxml' in requirement:
                    requirement_node = xml.dom.minidom.parseString(
                        requirement['rawxml']).documentElement
                    recipe_template.addHostRequires(requirement_node)
                else:
                    # If force is not used, a requirement can be any number
                    # of differently formatted XML elements, each with their
                    # own combination of element name and valid attrs. So,
                    # the best we can do is generate XML based on the input,
                    # and only the "tag" key is required.
                    tag_name = requirement['tag']
                    requirement_node = self.doc.createElement(tag_name)
                    for attr, value in requirement.items():
                        # Force all values to str, which the XML writer expects.
                        requirement_node.setAttribute(attr, str(value))
                    # use the BeakerRecipe API to add the element
                    recipe_template.addHostRequires(requirement_node)

            # Add Distro Requirements
            recipe_template.addBaseRequires(*args, **kwargs)
            arch_node = self.doc.createElement('distro_arch')
            arch_node.setAttribute('op', '=')
            arch_node.setAttribute('value', arch)
            recipe_set = BeakerRecipeSet(**kwargs)
            if wrkflow.multi_host:
                for i in range(self.n_servers):
                    recipe_set.addRecipe(wrkflow.processTemplate(
                        recipe_template,
                        requested_tasks,
                        taskParams=task_params,
                        distroRequires=arch_node,
                        role='SERVERS',
                        **kwargs))
                for i in range(self.n_clients):
                    recipe_set.addRecipe(wrkflow.processTemplate(
                        recipe_template,
                        requested_tasks,
                        taskParams=task_params,
                        distroRequires=arch_node,
                        role='CLIENTS',
                        **kwargs))
            else:
                recipe_set.addRecipe(wrkflow.processTemplate(
                    recipe_template,
                    requested_tasks,
                    taskParams=task_params,
                    distroRequires=arch_node,
                    **kwargs))
            job.addRecipeSet(recipe_set)

        # jobxml
        jobxml = job.toxml(**kwargs)

        if debug:
            LOG.debug(jobxml)

        self.submitted_jobs = []

        if not dryrun:
            self.submitted_jobs.append(self.hub.jobs.upload(jobxml))
            LOG.info("Submitted: %s" % self.submitted_jobs)
        return self.submitted_jobs

    def create_recipesets(self, recipeset, **kwargs):
        kwargs = {}
        for key, values in recipeset.iteritems():
            kwargs.update({key: values})
        return kwargs

    def check_jobs(self, jobs):
        # slightly modified copy of the same method in bkr_info, used here to
        # let bkr_server return beaker job info in the same structure as
        # bkr_info so we can stash provisioning details in rundb before the
        # bkr_info task blocks on waiting for the beaker job(s) to finish.
        # Importing code from bkr_info is not an option due to ansible's
        # sandboxing; bkr_info is not guaranteed to be importable at runtime.
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
        return resources

    def cancel_jobs(self, jobs, msg):
        """
            Cancel job in Beaker
        """
        for task in jobs:
            self.hub.taskactions.stop(task, 'cancel', msg)
            LOG.info("Cancel job %s in Beaker" % task)

    def get_url(self, bkr_id):
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


def main():
    module = AnsibleModule(argument_spec={
        'whiteboard': {'required': False, 'type': 'str'},
        'recipesets': {'required': True, 'type': 'list'},
        'job_group': {'default': '', 'type': 'str'},
        'state': {'default': 'present', 'choices': ['present', 'absent']},
        'cancel_message': {'default': 'Job canceled by LinchPin'},
        'max_attempts': {'default': 60, 'type': 'int'},
        'attempt_wait_time': {'default': 60, 'type': 'int'},
        'ssh_keys_path': {'required': False, 'type': 'str'},
    })
    params = type('Args', (object,), module.params)
    factory = BkrFactory()
    recipesets = []
    for recipeset in params.recipesets:
        for x in range(0, recipeset.get('count', 1)):
            recipesets.append(recipeset)
    parsed_ids = {}
    if params.state == 'present':
        extra_params = {}
        if params.job_group:
            extra_params['job_group'] = params.job_group
        extra_params['ssh_keys_path'] = params.ssh_keys_path
        # Make provision
        try:
            job_ids = factory.provision(debug=True,
                                        recipesets=recipesets,
                                        whiteboard=params.whiteboard,
                                        **extra_params)
        except Exception as ex:
            module.fail_json(msg=str(ex))

        for job_id in job_ids:
            parsed_id = job_id[2:]
            parsed_ids[parsed_id] = factory.get_url(parsed_id)
        hosts = factory.check_jobs(job_ids)
        # pass out the provisioned job ids (or empty dict, if none) and
        # provisioning params to be used in the bkr_info task later
        module.exit_json(changed=True, ids=parsed_ids, hosts=hosts,
                         provision_params=module.params)
    else:  # state == absent, cancel provisioned jobs
        for recipeset in params.recipesets:
            # recipeset 'ids" value is set in the teardown playbook for use here
            factory.cancel_jobs(recipeset['ids'], params.cancel_message)
        module.exit_json(changed=True)


main()
