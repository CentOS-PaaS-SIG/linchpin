from cerberus import errors as cerberus_errors


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


class ValidationErrorHandler(cerberus_errors.BasicErrorHandler):
    messages = cerberus_errors.BasicErrorHandler.messages.copy()
    messages[cerberus_errors.REQUIRED_FIELD.code] = "field '{field}' is "\
        + "required"
    messages[cerberus_errors.UNKNOWN_FIELD.code] = "field '{field}' could not "\
        + "be recognized within the schema provided"
    messages[cerberus_errors.BAD_TYPE.code] = "value for field '{field}' must "\
        + "be of type '{constraint}'"
    messages[cerberus_errors.UNALLOWED_VALUE.code] = "unallowed value " \
        + "'{value}' for field '{field}'. Allowed values are: {constraint}"
