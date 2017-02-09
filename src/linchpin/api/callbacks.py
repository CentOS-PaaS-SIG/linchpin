import ansible
from ansible.plugins.callback import CallbackBase


class PlaybookCallback(CallbackBase):
    """Playbook callback"""
    def __init__(self):
        super(PlaybookCallback, self).__init__()
        # store all results
        self.results = []

    def v2_runner_on_ok(self, result, **kwargs):
        """Save result instead of printing it"""
        self.results.append(result)
