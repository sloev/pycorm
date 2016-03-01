# -*- coding: utf-8 -*-
#based on http://hayd.github.io/2013/dotable-dictionaries/
import sys


from jsonschema.validators import validator_for as jsonschema_validator_for
from jsonschema import ValidationError
from . import SchemaValidationError, InheritanceNotSupportedError

def StringField():
    return {"type":"string"}


def NumberField():
    return {"type":"number"}


__allowed_options__ = {"additionalProperties":False, "required":None}


class BaseModel(dict):

    """Basemodel with dotnotation and jsonschema validation

    Basemodels create, and cache, jsonschema's of their attributes upon
    instantiation. These schemas are then used to validate a given Value
    dictionary.

    By default BaseModels do not accept additionalProperties and all their
    attributes are required.
    Also by default BaseModels are not validating input Value dictionaries
    on construction, thats what the "with_validation" class method is for!


    Example 1:
    >>>class Pilot(BaseModel):
    >>>    name = StringField()
    >>>    def greet(self):
    >>>        return "%s says hello" % self.name

    >>>class Plane(BaseModel):
    >>>    name = StringField()
    >>>    pilot = Pilot()

    You instantiate a Plane like this:
    >>>plane = Plane({'name':'Mary', 'pilot':{'name':'Hans'})
    You can then validate the plane with
    >>>plane.validate()
    Or you could validate on construction with:
    >>>plane = Plane.with_validation({'name':'Mary', 'pilot':{'name':'Hans'})

    The plane will then expose all its attributes by dotnotation. It will
    also automatically have resolved that the 'pilot' should be an instance
    of Pilot. This is shown with:
    >>>plane.pilot.greet()
    which returns
    "Hans says hello"

    """

    __schema__ = None
    __schema_validator__ = None
    # Model.an_attribute == Model['an_attribute']
    __getattr__ = dict.__getitem__

    def __init__(self, value_dict=None, _lookup=None):
        """Recursively instantiates a Model

        :param value_dict:
         :type: value_dict: dict
        :param _lookup:
         :type: _lookup: dict
        :return:
        """
        if not BaseModel in self.__class__.__bases__:
            raise InheritanceNotSupportedError()
        self.validate_schema()
        if value_dict is not None:
            if not _lookup:
                _lookup = self.__schema__.get('properties', {})
            self.update(**dict(
                (key,self.__parse_input(value, _lookup.get(key, None)))
                for key, value in value_dict.iteritems()))
        print ""

    def validate(self):
        """Validates self.__dict__ against self.__class__.__schema__

        :return:
        """
        try:
            self.__class__.__schema_validator__.validate(self)
        except ValidationError, e:
            raise SchemaValidationError, e, sys.exc_info()[2]

    @classmethod
    def with_validation(cls, value_dict):
        """Creates,validates and returns a Model instance.

        :param value_dict:
         :type: value_dict: dict
        :return:
        """
        inst = cls(value_dict)
        inst.validate()
        return inst

    @classmethod
    def validate_schema(cls):
        """Validates the validation schema of a model

        :return:
        """
        if not cls is BaseModel and not cls.__schema__:
            # pop allowed options
            options = {key: value for key, value in (
                (key, cls.__popattr__(key, default))
                for key, default in __allowed_options__.items()) if value is not
                       None}

            # pop public kwargs
            kwargs = {key: cls.__parse_schema(cls.__popattr__(key))
                    for key, value in cls.__dict__.items()
                    if not callable(value) and not str(key).startswith("__")}

            # create schema from kwargs and options
            cls.__schema__ = dict({
                "type": "object",
                "properties": kwargs
                },
                **options)

            # avoid endless recursion by fisrt creating dict and then cast it
            cls.__schema__ = cls(cls.__schema__)
            print ""

        if not cls is BaseModel and not cls.__schema_validator__:
            # cache jsonschema validator in Model class
            validator_class = jsonschema_validator_for(cls.__schema__)
            validator_class.check_schema(cls.__schema__)
            cls.__schema_validator__ = validator_class(cls.__schema__)

    @classmethod
    def __parse_schema(cls, value_dict):
        """Parses a validation schema recursively

        :param value_dict:
         :type: value_dict: dict
        :return:
        """
        if isinstance(value_dict, BaseModel):
            return value_dict.__class__(value_dict.__schema__)
        elif isinstance(value_dict, list):
            return [cls.__parse_schema(i) for i in value_dict]
        else:
            return value_dict

    @classmethod
    def __parse_input(cls, value_dict, _lookup=None):
        """Parses an input value_dict recursively

        :param value_dict:
         :type: value_dict: dict
        :param _lookup:
         :type: _lookup: dict
        :return:
        """
        if isinstance(value_dict, BaseModel):
            return value_dict.__class__(value_dict, _lookup=_lookup)
        elif isinstance(value_dict, dict):
            if isinstance(_lookup, BaseModel):
                return _lookup.__class__(value_dict, _lookup=_lookup)
            return cls(value_dict, _lookup=_lookup)
        elif isinstance(value_dict, list):
            return [cls.__parse_input(i) for i in value_dict]
        else:
            return value_dict

    @classmethod
    def __popattr__(cls, key, default=None):
        """Pop attr's from an instance

        :param inst:
        :param key:
        :param default:
        :return:
        """
        val = getattr(cls, key, None)
        if val is not None:
            delattr(cls, key)
            return val
        return default
