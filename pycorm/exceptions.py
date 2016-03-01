from jsonschema import ValidationError as ValidationError

class SchemaValidationError(ValidationError):
    pass

class InheritanceNotSupportedError(Exception):
    pass

