from subprocess_action_manager import SubprocessActionManager
from ansible_action_manager import AnsibleActionManager
from python_action_manager import PythonActionManager
from ruby_action_manager import RubyActionManager
from node_action_manager import NodeActionManager

# dict of core action manager packaged with linchpin
ACTION_MANAGERS = {
    "shell" : SubprocessActionManager,
    "ansible" : AnsibleActionManager,
    "python": PythonActionManager,
    "ruby" : RubyActionManager,
    "node" : NodeActionManager
}
