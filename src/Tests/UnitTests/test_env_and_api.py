import os
from unittest import TestCase, mock
from your_module_name import test_env_and_api  # Replace 'your_module_name' with the actual module name

class TestEnvAndApi(TestCase):

    @mock.patch.dict(os.environ, {"API_USERNAME": "test_user", "API_PASSWORD": "test_pass"})
    @mock.patch("your_module_name.requests.post")
    def test_valid_credentials(self, mock_post):
        # Mock a successful API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {
                "authToken": "test_token"
            }
        }

        result = test_env_and_api()

        self.assertEqual(result, "test_token")
        mock_post.assert_called_once_with(
            "https://api.metallic.io/login",
            headers={
                "Content-Type": "application/json",
                "User-Agent": "PostmanRuntime/7.43.0"
            },
            data=mock.ANY  # Match any payload
        )

    @mock.patch.dict(os.environ, {})
    def test_missing_environment_variables(self):
        with self.assertRaises(ValueError) as context:
            test_env_and_api()

        self.assertEqual(str(context.exception), "Environment variables API_USERNAME or API_PASSWORD are not set.")

    @mock.patch.dict(os.environ, {"API_USERNAME": "test_user", "API_PASSWORD": "test_pass"})
    @mock.patch("your_module_name.requests.post")
    def test_api_failure(self, mock_post):
        # Mock a failed API response
        mock_post.return_value.status_code = 401
        mock_post.return_value.text = "Unauthorized"

        result = test_env_and_api()

        self.assertIsNone(result)
        mock_post.assert_called_once()
