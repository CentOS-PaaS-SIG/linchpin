
class LinchpinError(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class HookError(LinchpinError):

    def __init__(self, *args, **kwargs):
        LinchpinError.__init__(self, *args, **kwargs)


class StateError(LinchpinError):

    def __init__(self, *args, **kwargs):
        LinchpinError.__init__(self, *args, **kwargs)


class ActionManagerError(LinchpinError):

    def __init__(self, *args, **kwargs):
        LinchpinError.__init__(self, *args, **kwargs)


class SchemaError(LinchpinError):

    def __init__(self, *args, **kwargs):
        LinchpinError.__init__(self, *args, **kwargs)


class ValidationError(LinchpinError):

    def __init__(self, *args, **kwargs):
        LinchpinError.__init__(self, *args, **kwargs)


class TopologyError(LinchpinError):

    def __init__(self, *args, **kwargs):
        LinchpinError.__init__(self, *args, **kwargs)


class ActionError(LinchpinError):

    def __init__(self, *args, **kwargs):
        LinchpinError.__init__(self, *args, **kwargs)
