#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pycorm
----------------------------------

Tests for `pycorm` module.
"""

import unittest

from pycorm.pycorm import Model, StringField, NumberField


class ModelA(Model):
    required = ["bar"]
    additionalProperties = False

    bar = StringField()

    def baz(self):
        return "baz"

class ModelB(Model):
    foo = ModelA()
    baz = NumberField()

class ModelC(Model):
    __schema__ = {
            "type": "object",
            "properties": {
                "foo": {"type": "string"}
            },
            "required": ["foo"],
            "additionalProperties": False
            }

class TestPycorm(unittest.TestCase):

    def setUp(self):
        self.model_b_dict_1 = {
                "baz": 20,
                "foo": {
                    "bar": "bar"
                    }
                }

        self.model_b_dict_2 = {
                "baz" : "baz",
                "foo":{
                    "bar": 10
                    }
                }

    def tearDown(self):
        pass
    def test_that_dotnotation_works(self):
        self.assertEquals(self.model_b_dict_1['foo']['bar'],ModelB.with_validation(self.model_b_dict_1).foo.bar)
    
    def test_that_wrong_type_raises_exception(self):
        self.assertRaises(Exception, ModelB.with_validation, self.model_b_dict_2)

    def test_that_implicit_inheritance_works(self):
        self.assertEquals("baz", ModelB.with_validation(self.model_b_dict_1).foo.baz())



if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
