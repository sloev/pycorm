# -*- coding: utf-8 -*-
#based on http://hayd.github.io/2013/dotable-dictionaries/
from jsonschema import validate as jsonschema_validate


def StringField():
    return {"type":"string"}

def NumberField():
    return {"type":"number"}
def ModelField(model):
    pass
__allowed_options__ = ["additionalProperties", "required"]
class Model(dict):
    __schema__ = None

    __getattr__= dict.__getitem__

    def __init__(self, value_dict=None, strict=False):
        if not type(self) is Model and not self.__class__.__schema__:
            # create kwargs from public class attrs
            kwargs = [(key, value) for key, value in
                        self.__class__.__dict__.iteritems() if not callable(
                    value) and not str(key).startswith("__")]
            # cache schema class attr and delete kwargs on class
            self.__class__.__schema__ = {
                "type": "object",
                "properties": {key: (delattr(self.__class__,key) or
                           self.__parse_schema(value))
                     for key, value in kwargs}
            }
            # get extra options
            options = {key: value for key, value in (
                (key, getattr(self.__class__, "__%s__" % key, None))
                for key in __allowed_options__) if value is not None}

            self.__class__.__schema__.update(options)
            [delattr(self.__class__, "__%s__" % key) for key in
             __allowed_options__ if hasattr(self.__class__, "__%s__" % key)]

        if value_dict is not None:
            self.update(**dict((k, self.__parse_input(v))
                           for k, v in value_dict.iteritems()))
        self.on_create()

    def on_create(self):
        pass

    def validate(self):
        jsonschema_validate(self, self.__schema__)

    @classmethod
    def with_validation(cls, value_dict, strict=False):
        inst = cls(value_dict, strict=strict)
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

class A(Model):
    __required__ = ["foo"]
    __additionalProperties__ = False

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


b = B.with_validation({"baz":{"foo":"lolcat"}})
#"raises exception - C.with_validation({"foo":10})
c = C.with_validation({"foo":"lolcat"})

print b.baz.foo == c.foo
#pprint(b.baz.foo)
