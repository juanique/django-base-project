"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from resources import FieldsValidation


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class FieldsValidationTest(TestCase):
    def test_parse_methods_key(self):
        validation = FieldsValidation()
        key = "required_post"
        #value = ['field1','field2']
        target = {}

        methods = validation.parse_methods_key(key,'required')
        self.assertEqual(['POST'], methods)

    def test_map_method_validation(self):
        validation = FieldsValidation()
        fields = ['field1','field2']
        methods = ["POST","PUT","GET","DELETE"]
        target = {}
        validation.map_method_validations(target, fields, methods)

        expected = {
                'POST' : ['field1','field2'],
                'GET' : ['field1','field2'],
                'PUT' : ['field1','field2'],
                'DELETE' : ['field1','field2'],
                }

        self.assertEqual(expected, target)

        validation.map_method_validations(target, ['field3'], ['PUT','POST'])

        expected = {
                'POST' : ['field1','field2','field3'],
                'GET' : ['field1','field2'],
                'PUT' : ['field1','field2','field3'],
                'DELETE' : ['field1','field2'],
                }

        self.assertEqual(expected, target)

    def test_fieldsvalidation_constructor(self):
        validation = FieldsValidation(required = ['f1','f2'],
                                      validated = ['f1','f3'],
                                      required_post_get = ['f4'],
                                      validated_put = ['f5'])

        expected_required = {
                'POST' : ['f1','f2','f4'],
                'GET' : ['f1','f2','f4'],
                'PUT' : ['f1','f2'],
                'DELETE' : ['f1','f2'],
                }

        expected_validated = {
                'POST' : ['f1','f3'],
                'GET' : ['f1','f3'],
                'PUT' : ['f1','f3','f5'],
                'DELETE' : ['f1','f3'],
                }

        self.assertEqual(expected_validated, validation.validated_fields)
        self.assertEqual(expected_required, validation.required_fields)





