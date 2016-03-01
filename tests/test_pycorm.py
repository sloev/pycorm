#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pycorm
----------------------------------

Tests for `pycorm` module.
"""

import unittest

from pycorm import BaseModel, StringField, NumberField
from pycorm import SchemaValidationError, InheritanceNotSupportedError


class BaseModelA(BaseModel):
    bar = StringField()

    def baz(self):
        return "baz"


class BaseModelB(BaseModel):
    additionalProperties = True
    foo = BaseModelA()
    baz = NumberField()


class BaseModelC(BaseModel):
    foo = BaseModelA()
    baz = NumberField()


class BaseModelD(BaseModelA):
    foo = StringField()

class Mixin(object):
    def baz(self):
        return "baz"

class BaseModelE(BaseModel, Mixin):
    foo = StringField()
    def bar(self):
        return "bar"

class TestPycorm(unittest.TestCase):

    def setUp(self):
        self.valid_dict = {
                "baz": 20,
                "foo": {
                    "bar": "bar"
                    }
                }

        self.invalid_dict = {
                "baz" : "baz",
                "foo":{
                    "bar": 10
                    }
                }
        self.additional_properties_dict = {
            "baz" : 20,
            "wrong_key":"wrong_value",
            "foo":{
                "bar": "bar"
                }
            }


    def tearDown(self):
        pass

    def test_that_dotnotation_works(self):
        self.assertEquals(self.valid_dict['foo']['bar'],
                BaseModelB.with_validation(self.valid_dict).foo.bar)

    def test_that_wrong_type_raises_exception(self):
        self.assertRaises(SchemaValidationError,BaseModelB.with_validation,
                self.invalid_dict)

    def test_that_embedded_model_instantiation_works(self):
        self.assertEquals(
                "baz", BaseModelB.with_validation(self.valid_dict).foo.baz())

    def test_that_additional_properties_true_works(self):
        self.assertEquals(
                self.additional_properties_dict['wrong_key'],
                BaseModelB.with_validation(
                    self.additional_properties_dict).wrong_key)

    def test_that_additional_properties_raise_error(self):
        self.assertRaises(SchemaValidationError, BaseModelC.with_validation,
            self.additional_properties_dict)

    def test_that_inheritance_raises_error(self):
        self.assertRaises(InheritanceNotSupportedError, BaseModelD)

    def test_that_mixins_work(self):
        self.assertEquals("baz", BaseModelE.with_validation({"foo":"bar"}).baz())
        self.assertEquals("bar", BaseModelE.with_validation({"foo":"bar"}).bar())

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
