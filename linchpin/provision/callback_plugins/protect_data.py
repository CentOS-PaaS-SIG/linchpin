from ansible.plugins.callback.default import CallbackModule as CallbackModule_default
import os, collections

class CallbackModule(CallbackModule_default):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'protect_data'

    def __init__(self, display=None):
        super(CallbackModule, self).__init__(display)

    def hide_password(self, result):
        ret = {}
        for key, value in result.iteritems():
            if isinstance(value, collections.Mapping):
                ret[key] = self.hide_password(value)
            else:
                if key in ['client_id', 'token', 'subscription_id', 'secret', 'password']:
                    ret[key] = "********"
                else:
                    ret[key] = value
        return ret

    def _dump_results(self, result, indent=None, sort_keys=True, keep_invocation=False):
        return super(CallbackModule, self)._dump_results(self.hide_password(result), indent, sort_keys, keep_invocation)
