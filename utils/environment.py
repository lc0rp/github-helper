import os
from dotenv import load_dotenv

env_vars = {}

def get_environment_variable(variable_name: str, prompt_message: str) -> str:
    value = os.environ.get(variable_name)
    if value is None:
        value = input(prompt_message)
    return value

def prompt_for_missing_environment_variables(dry_run=True) -> dict:
    if not env_vars.get("GITHUB_URL"):
        load_dotenv()
        env_vars["GITHUB_URL"] = get_environment_variable("GITHUB_URL", "Enter the GitHub URL: ")
        env_vars["GITHUB_TOKEN"] = get_environment_variable("GITHUB_TOKEN", "Enter your GitHub token: ")
        env_vars["OPENAI_API_KEY"] = get_environment_variable("OPENAI_API_KEY", "Enter your OpenAI API key: ")
        env_vars["OPENAI_ENGINE"] = get_environment_variable("OPENAI_ENGINE", "Enter the OpenAI engine (gpt4 or gpt3.5-turbo): ")
        if dry_run:
            env_vars["DRY_RUN"] = "True"
    return env_vars;