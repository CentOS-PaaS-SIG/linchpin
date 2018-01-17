from ansible.plugins.callback import CallbackBase


class PlaybookCallback(CallbackBase):

    """Playbook callback"""


    def __init__(self, display=None, options=None):
        super(PlaybookCallback, self).__init__(display=display,
                                               options=options)

        self._options = options
        self._display.verbosity = options.verbosity

        # store all results
        self.results = []


    def v2_runner_on_ok(self, result):

        """Save ok result"""

        self.results.append(result)

    def v2_runner_on_failed(self, result, **kwargs):

        """Save failed result"""

        self.results.append(result)
