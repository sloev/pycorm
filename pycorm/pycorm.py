# -*- coding: utf-8 -*-
#based on http://hayd.github.io/2013/dotable-dictionaries/
from jsonschema.validators import validator_for as jsonschema_validator_for


def StringField():
    return {"type":"string"}

def NumberField():
    return {"type":"number"}
def ModelField(model):
    pass
__allowed_options__ = ["additionalProperties", "required"]


class Model(dict):
    __schema__ = None
    __schema_validator__ = None

    __getattr__= dict.__getitem__


    def __init__(self, value_dict=None):
        self.validate_schema()

        if value_dict is not None:
            self.update(**dict((k, self.__parse_input(v))
                           for k, v in value_dict.iteritems()))
        self.on_create()

    def on_create(self):
        pass

    def validate(self):
        self.__class__.__schema_validator__.validate(self)

    @classmethod
    def validate_schema(cls):
        if not cls is Model and not cls.__schema__:
            # pop options
            options = {key: value for key, value in (
                (key, cls.__popattr__(cls, key, None))
                for key in __allowed_options__) if value is not None}

            # pop kwargs
            kwargs = {key: cls.__parse_schema(cls.__popattr__(cls, key))
                    for key, value in cls.__dict__.items()
                    if not callable(value) and not str(key).startswith("__")}

            # create schema from kwargs and options
            cls.__schema__ = dict({
                "type": "object",
                "properties": kwargs
                },
                **options)
        if not cls is Model and not cls.__schema_validator__:
            validator_class = jsonschema_validator_for(cls.__schema__)
            validator_class.check_schema(cls.__schema__)
            cls.__schema_validator__ = validator_class(cls.__schema__)

    @classmethod
    def with_validation(cls, value_dict):
        inst = cls(value_dict)
        inst.validate()
        return inst


    @classmethod
    def __parse_schema(cls, v):
        if isinstance(v, Model):
            return v.__schema__
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v

    @classmethod
    def __parse_input(cls, v):
        if isinstance(v, dict):
            return cls(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v

    @staticmethod
    def __popattr__(inst, key, default=None):
        val = getattr(inst, key, default)
        if val is not None:
            delattr(inst, key)
        return val

class A(Model):
    required = ["foo"]
    additionalProperties = False

    foo = StringField()

class B(Model):
    baz = A()

class C(Model):
    __schema__ = {
            "type": "object",
            "properties": {
                "foo": {"type": "string"}
            },
            "required": ["foo"],
            "additionalProperties": False
            }


b = B.with_validation({"baz":A({"foo":"lolcat"})})
#"raises exception - C.with_validation({"foo":10})
c = C.with_validation({"foo":"lolcat"})

print b.baz.foo == c.foo
#pprint(b.baz.foo)
