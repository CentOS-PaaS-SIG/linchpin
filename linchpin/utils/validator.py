from cerberus import Validator
from cerberus import errors


class AnyofValidator(Validator):
    def __init__(self, *args, **kwargs):
        super(AnyofValidator, self).__init__(*args, **kwargs)

    def _validate_anyof(self, definitions, field, value):
        """ {'type': 'list', 'logical': 'anyof'} """

        if 'role' not in definitions[0]['schema'].keys():
            return super(AnyofValidator, self)._validate_anyof(definitions,
                                                               field, value)

        valids = 0
        found_valid_role = False
        _errors = errors.ErrorList()
        valid_roles = []
        for i, definition in enumerate(definitions):
            valid_roles.extend(definition['schema']['role']['allowed'])
            if value['role'] not in definition['schema']['role']['allowed']:
                continue

            found_valid_role = True

            schema = {field: definition.copy()}
            for rule in ('allow_unknown', 'type'):
                if rule not in schema[field] and rule in self.schema[field]:
                    schema[field][rule] = self.schema[field][rule]
            if 'allow_unknown' not in schema[field]:
                schema[field]['allow_unknown'] = self.allow_unknown

            validator = self._get_child_validator(
                schema_crumb=(field, 'role', value['role']), schema=schema,
                allow_unknown=True
            )
            if validator(self.document, update=self.update, normalize=False):
                valids += 1
            else:
                _errors.extend(validator._errors)

        if valids == 0:
            if not found_valid_role:
                role_error = errors.ValidationError(
                    ("resource_definitions", 0, "role"),
                    ("res_defs", "schema", "anyof", -1, "schema", "role"),
                    0x44, "rule", valid_roles, value['role'], ""
                )
                self._error([role_error])
            else:
                self._error(validator._errors)
