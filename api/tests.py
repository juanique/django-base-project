"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from resources import FieldsValidation
from jsonrpc.proxy import ServiceProxy
from django.test import Client
import json


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

class TestUserResource(TestCase):
    def setUp(self):
        self.user_data = {
            "username":"godinez5",
            "password":"mypassword",
            "first_name" : "juanelo", 
            "last_name" : "godinez", 
            "email" : "juanelo@godinez.cl"
        }

    def test_missing_email(self):
        client = Client()
        del self.user_data['email']
        post_response = client.post('/api/resources/user/',
                json.dumps(self.user_data), 
                'application/json')
        self.assertEqual(400, post_response.status_code) # 400: CLIENT ERROR
        response_dict = json.loads(post_response.content)
        self.assertEqual(['email'], response_dict.keys())

    def test_missing_password(self):
        client = Client()
        del self.user_data['password']
        post_response = client.post('/api/resources/user/',
                json.dumps(self.user_data), 
                'application/json')
        self.assertEqual(400, post_response.status_code) # 400: CLIENT ERROR
        response_dict = json.loads(post_response.content)
        self.assertEqual(['password'], response_dict.keys())
    
    def test_post_get_authenticate(self):
        '''Happy path test.'''

        client = Client()

        #test POST
        post_response = client.post('/api/resources/user/',
                json.dumps(self.user_data), 
                'application/json')
        self.assertEqual(201, post_response.status_code) # 201: CREATED
        get_response = client.get('/api/resources/user/')

        #test GET
        response_dict = json.loads(get_response.content)
        self.assertEqual(1, response_dict['meta']['total_count'])

        expected = dict(self.user_data)
        del expected['password']
        del expected['email']
        self.assertDictContainsSubset(expected, response_dict['objects'][0])

        #test Authenticate
        #rpc = ServiceProxy('http://localhost:8000/api/rpc/')
        #auth_response = rpc.authenticate(username=self.user_data['username'], 
        #        password=self.user_data['password'])
        #print auth_response





'''
class TestAuthenticationRPC(TestCase):

    def test_valid_authentication(self):
        rpc = ServiceProxy('http://localhost:8000/api/rpc/')
        rpc.authenticate(
'''






