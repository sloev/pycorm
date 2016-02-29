#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pycorm
----------------------------------

Tests for `pycorm` module.
"""

import unittest

from pycorm.pycorm import BaseModel, StringField, NumberField


class BaseModelA(BaseModel):
    bar = StringField()

    def baz(self):
        return "baz"

class BaseModelB(BaseModel):
    additionalProperties = True
    foo = BaseModelA()
    baz = NumberField()

class TestPycorm(unittest.TestCase):

    def setUp(self):
        self.BaseModel_b_dict_1 = {
                "baz": 20,
                "foo": {
                    "bar": "bar"
                    }
                }

        self.BaseModel_b_dict_2 = {
                "baz" : "baz",
                "foo":{
                    "bar": 10
                    }
                }
        self.BaseModel_b_dict_3 = {
            "baz" : 20,
            "wrong_key":"wrong_value",
            "foo":{
                "bar": "bar"
                }
            }

    def tearDown(self):
        pass
    def test_that_dotnotation_works(self):
        self.assertEquals(self.BaseModel_b_dict_1['foo']['bar'],BaseModelB.with_validation(self.BaseModel_b_dict_1).foo.bar)

    def test_that_wrong_type_raises_exception(self):
        self.assertRaises(Exception, BaseModelB.with_validation, self.BaseModel_b_dict_2)

    def test_that_implicit_inheritance_works(self):
        self.assertEquals("baz", BaseModelB.with_validation(self.BaseModel_b_dict_1).foo.baz())

    def test_that_additional_properties_true_works(self):
        self.assertEquals(self.BaseModel_b_dict_3['wrong_key'],
                          BaseModelB.with_validation(
            self.BaseModel_b_dict_3).wrong_key)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
