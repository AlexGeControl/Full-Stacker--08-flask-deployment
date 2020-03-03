import os
import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['JWT_SECRET'] = 'TestSecret'
        self.app = create_app('testing')
        # activate app context:
        self.app_context = self.app.app_context()
        self.app_context.push()
        # create client:
        self.client = self.app.test_client(use_cookies=True)
        # set up contents and auth:
        self.EMAIL = 'fullstackdevelopment@udacity.com'
        self.PASSWORD = 'fullstackdevelopment'

    def tearDown(self):
        # deactivate app context:
        self.app_context.pop()

    def get_api_headers(self, token):  
        """ api header generation
        """      
        return {            
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_get_contents_with_valid_auth(self):
        """  response should have status code 200 and json {"email": email, } for request GET /contents
        """
        # generate token:
        contents = {
            'email': self.EMAIL,
            'password': self.PASSWORD
        }
        # send request:
        response = self.client.post(
            url_for('api.auth'), 
            data=json.dumps(contents),
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse token:
        token = json.loads(
            response.get_data(as_text=True)
        )["token"]

        # send request:
        response = self.client.get(
            url_for('api.contents'), 
            headers=self.get_api_headers(
                token = token
            ),
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )

        # check response structure:
        self.assertTrue("email" in json_response)
        self.assertTrue("exp" in json_response)
        self.assertTrue("nbf" in json_response)

        # check response value:
        self.assertEqual(json_response["email"], self.EMAIL)