# -*- coding: utf-8 -*-
#based on http://hayd.github.io/2013/dotable-dictionaries/
from jsonschema import validate as jsonschema_validate
from jsonschema import SchemaError, ValidationError

from exceptions import PycormSchemaError, PycormValidationError

class Model(dict):
    __schema__ = None

    __getattr__= dict.__getitem__

    def __init__(self, d, validate_on_construction=False):
        self.update(**dict((k, self.parse(v))
                           for k, v in d.iteritems()))

        if validate_on_construction:
            self.validate()
        self.on_create()

    def on_create(self):
        pass

    def validate(self):
        try:
            jsonschema_validate(self, self.__schema__)
        except SchemaError as e:
            raise PycormSchemaError(e)
        except ValidationError as e:
            raise PycormValidationError(e)

    @classmethod
    def with_validation(cls, d):
        return cls(d, validate_on_construction=True)

    @classmethod
    def parse(cls, v):
        if isinstance(v, dict):
            return cls(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v
