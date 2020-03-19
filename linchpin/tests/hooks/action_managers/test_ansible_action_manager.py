from nose.tools import with_setup
from nose.tools import assert_true
from nose.tools import assert_equal
from nose.tools import assert_dict_equal

from linchpin.hooks.action_managers import AnsibleActionManager


# ------------------------------- #
#    Setup functions for tests    #
# ------------------------------- #
def setup_ansible_action_manager():
    global manager

    name = "ansible"
    action_data = {'name': 'success_hook',
                   'context': True,
                    'path': 'docs/source/examples/workspaces/dummy-hook-flags/hooks/ansible/success_hook/',
                   'actions': [{
                       'playbook': 'success_hook.yaml'
                   }]}
    target_data = {'inventory_dir': 'inventories',
                   'inventory_file': 'docs/source/examples/workspaces/dummy-hook-flags/inventories/dummy-da1711.inventory'}
    context = True
    use_shell = True
    state = "postup"
    kwargs = {'context': True, 'verbosity': 2, 'use_shell': False}

    manager = AnsibleActionManager(name, action_data, target_data, state=state, context=context, use_shell=use_shell)


# ----------- #
#    Tests    #
# ----------- #
@with_setup(setup_ansible_action_manager)
def test_validate():
    status = manager.validate()
    # the status will be 'True' if the validation succeeded
    assert_true(status)


@with_setup(setup_ansible_action_manager)
def test_load():
    pass


@with_setup(setup_ansible_action_manager)
def test_get_ctx_params():
    params = manager.get_ctx_params()
    assert_equal(list(params.keys()), ['resource_file',
                                     'layout_file',
                                     'inventory_file'])

@with_setup(setup_ansible_action_manager)
def test_execute():
    expected_results = {'state': 'postup', 'return_code': 0, 'data': []}
    results = manager.execute([])
    assert_equal(len(results), 1)
    assert_dict_equal(results[0], expected_results)
