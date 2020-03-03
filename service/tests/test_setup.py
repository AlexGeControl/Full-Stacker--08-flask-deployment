import unittest

from flask import current_app

from application import create_app

class SetupTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        # activate app context:
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # deactivate app context:
        self.app_context.pop()

    def test_app_exists(self):
        """ app should be created
        """
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """ testing config should be used
        """
        self.assertTrue(current_app.config['TESTING'])
