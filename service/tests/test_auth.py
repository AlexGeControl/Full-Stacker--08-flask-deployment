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

    def test_post_auth_with_invalid_contents_missing_email(self):
        """  response should have status code 400 and json {"success": False} for request POST /auth with invalid contents
        """
        contents = {
            'password': self.PASSWORD
        }
        # send request:
        response = self.client.post(
            url_for('api.auth'), 
            data=json.dumps(contents),
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 400)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )

        # check success:
        self.assertFalse(json_response["success"])

    def test_post_auth_with_invalid_contents_missing_password(self):
        """  response should have status code 400 and json {"success": False} for request POST /auth with invalid contents
        """
        contents = {
            'email': self.EMAIL
        }
        # send request:
        response = self.client.post(
            url_for('api.auth'), 
            data=json.dumps(contents),
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 400)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )

        # check success:
        self.assertFalse(json_response["success"])

    def test_post_auth_with_valid_contents(self):
        """  response should have status code 200 and json {"token": token} for request POST /auth
        """
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

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )

        # check success:
        self.assertTrue(
            "token" in json_response
        )