import unittest
import json

from flask import current_app
from flask import url_for

from application import create_app


class HealthCheckTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        # activate app context:
        self.app_context = self.app.app_context()
        self.app_context.push()
        # create client:
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        # deactivate app context:
        self.app_context.pop()

    def test_get_health_check(self):
        """  response should have status code 200 and json "Healthy" for request GET /
        """

        # send request:
        response = self.client.get(
            url_for('api.health'), 
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check success:
        self.assertEqual(
            json_response, "Healthy"
        )

    def test_post_health_check(self):
        """  response should have status code 200 and json "Healthy" for request POST /
        """

        # send request:
        response = self.client.get(
            url_for('api.health'), 
            content_type='application/json'
        )        
        
        # check status code:
        self.assertEqual(response.status_code, 200)

        # parse json response:
        json_response = json.loads(
            response.get_data(as_text=True)
        )
        # check success:
        self.assertEqual(
            json_response, "Healthy"
        )