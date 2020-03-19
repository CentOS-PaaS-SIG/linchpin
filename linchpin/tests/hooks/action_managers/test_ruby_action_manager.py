from nose.tools import with_setup
from nose.tools import assert_true
from nose.tools import assert_equal
from nose.tools import assert_dict_equal

from linchpin.hooks.action_managers import RubyActionManager


# ------------------------------- #
#    Setup functions for tests    #
# ------------------------------- #
def setup_ruby_action_manager():
    global manager

    name = "ruby"
    action_data = {'name': 'success_hook',
                   'context': True,
                   'path': 'linchpin/tests/mockdata/dummy/hooks/ruby/success_hook',
                   'actions': ['success_hook.rb']
    }
    target_data = {'inventory_dir': 'inventories',
                   'inventory_file': 'docs/source/examples/workspaces/dummy-hook-flags/inventories/dummy-da1711.inventory'}
    context = True
    use_shell = True
    state = "postup"
    kwargs = {'context': True, 'verbosity': 2, 'use_shell': False}

    manager = RubyActionManager(name, action_data, target_data, state=state, context=context, use_shell=use_shell)


# ----------- #
#    Tests    #
# ----------- #
@with_setup(setup_ruby_action_manager)
def test_validate():
    status = manager.validate()
    # the status will be 'True' if the validation succeeded
    assert_true(status)


@with_setup(setup_ruby_action_manager)
def test_load():
    pass


@with_setup(setup_ruby_action_manager)
def test_add_ctx_params():
    # test add_ctx_params when context=False
    hook_path = '/tmp/hook_path'
    results = 'results'
    data_path = '/tmp/data_path'
    params = manager.add_ctx_params(hook_path, results, data_path, False)
    expected_params = "{0} -- '{1}' {2}".format(hook_path, results, data_path)
    assert_equal(params, expected_params)
    # test add_ctx_params when context=True
    params = manager.add_ctx_params(hook_path, results, data_path, True)
    expected_params = "{0} inventory_dir=inventories inventory_file=docs/source/examples/workspaces/dummy-hook-flags/inventories/dummy-da1711.inventory -- '{1}' {2}".format(hook_path, results, data_path)
    print(expected_params)
    print(params)
    assert_equal(params, expected_params)



@with_setup(setup_ruby_action_manager)
def test_execute():
    expected_results = {'state': 'postup', 'return_code': 0, 'data': ''}
    results = manager.execute([])
    assert_equal(len(results), 1)
    assert_dict_equal(results[0], expected_results)
