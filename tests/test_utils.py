import os
import pytest
from unittest.mock import patch

from utils.environment import prompt_for_missing_environment_variables
from utils.dry_run import execute_dry_run

def test_prompt_for_missing_environment_variables():
    with patch("builtins.input", side_effect=["https://github.com", "my_token", "my_openai_key", "gpt3.5-turbo"]):
        os.environ.pop("GITHUB_URL", None)
        os.environ.pop("GITHUB_TOKEN", None)
        os.environ.pop("OPENAI_API_KEY", None)
        os.environ.pop("OPENAI_ENGINE", None)

        prompt_for_missing_environment_variables()

        assert os.environ["GITHUB_URL"] == "https://github.com"
        assert os.environ["GITHUB_TOKEN"] == "my_token"
        assert os.environ["OPENAI_API_KEY"] == "my_openai_key"
        assert os.environ["OPENAI_ENGINE"] == "gpt3.5-turbo"

def test_execute_dry_run():
    command = "gh issue create --title 'Test issue' --body 'This is a test issue'"
    expected_output = f"Dry run: {command}"

    with patch("builtins.print") as mock_print:
        execute_dry_run(command)

    mock_print.assert_called_once_with(expected_output)