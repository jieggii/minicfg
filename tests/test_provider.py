import os
import unittest
from unittest.mock import patch

from minicfg.provider import EnvProvider


class TestEnvProvider(unittest.TestCase):

    def setUp(self):
        # Save the current state of environment variables
        self.provider = EnvProvider()
        self.original_environ = dict(os.environ)

    def tearDown(self):
        # Restore the original environment variables
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_get_existing_env_var(self):
        # Set up the environment variable for the test
        with patch.dict(os.environ, {"TEST_KEY": "test_value"}):
            result = self.provider.get("TEST_KEY")
            self.assertEqual(result, "test_value")

    def test_get_non_existing_env_var(self):
        # Ensure the environment variable does not exist
        with patch.dict(os.environ, {}, clear=True):
            result = self.provider.get("NON_EXISTENT_KEY")
            self.assertIsNone(result)

    def test_get_env_var_with_empty_value(self):
        # Set up the environment variable with an empty value
        with patch.dict(os.environ, {"EMPTY_KEY": ""}):
            result = self.provider.get("EMPTY_KEY")
            self.assertEqual(result, "")
