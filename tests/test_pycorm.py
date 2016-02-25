#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pycorm
----------------------------------

Tests for `pycorm` module.
"""

import unittest

from pycorm.pycorm import Model, PycormValidationError, PycormSchemaError

class ModelTest(Model):
    schema = {
            "type": "object",
            "properties": {
                "foo": {"type": "string"},
                "bar": {
                    "type": "object",
                    "properties": {
                        "baz": {"type":"number"}
                        },
                    "required": ["baz"],
                    "additionalProperties": False
                    }
                },
            "required": ["foo", "bar"],
            "additionalProperties": False
            }

class TestPycorm(unittest.TestCase):

    def setUp(self):
        self.dict_a = {
                "foo": "test",
                "bar": {
                    "baz": 10
                    }
                }

        self.dict_b = {
                "test": "foo",
                "bar": {
                    "baz": 10
                    }
                }

    def tearDown(self):
        pass

    def test_that_it_validates(self):
        self.assertEquals(self.dict_a, ModelTest.with_validation(self.dict_a))

    def test_that_it_raises_pycorm_validation_error(self):
        self.assertRaises(PycormValidationError, ModelTest.with_validation, self.dict_b)

    def test_that_dotnotation_works(self):
        model = ModelTest(self.dict_a)
        self.assertEquals(self.dict_a['bar']['baz'], model.bar.baz)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
