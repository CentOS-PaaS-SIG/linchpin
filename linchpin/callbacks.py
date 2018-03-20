from ansible.plugins.callback import CallbackBase


class PlaybookCallback(CallbackBase):

    """Playbook callback"""


    def __init__(self, display=None, options=None):
        super(PlaybookCallback, self).__init__(display=display,
                                               options=options)

        self._options = options
        self._display.verbosity = options.verbosity

        # store all results
        self.results = {'failed': [], 'ok': []}


    def v2_runner_on_ok(self, result):

        """Save ok result"""

        self.results['ok'].append(result)

    def v2_runner_on_failed(self, result, **kwargs):

        """Save failed result"""

        ignore_errors = kwargs.get('ignore_errors')

        if not ignore_errors:
            self.results['failed'].append(result)
