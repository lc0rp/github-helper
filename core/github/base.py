import json as json_module
import click
import requests
import requests_mock
from utils.environment import prompt_for_missing_environment_variables
           
class GithubBaseClient:
    def __init__(self) -> None:
        self.get_env_vars()
        self.headers = self.get_github_api_headers()
        
    def get_env_vars(self) -> dict[str, str]:
        env_vars = prompt_for_missing_environment_variables()
        self.token = env_vars.get("GITHUB_TOKEN")
        self.url = env_vars.get("GITHUB_URL")
        self.owner = self.url.split("/")[-2]
        self.repository = self.url.split("/")[-1]
        self.dry_run = env_vars.get("DRY_RUN")
        
    def get_github_api_headers(self) -> dict[str, str]:
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json"}

    def get_github_url(self) -> str:
        self.get_env_vars()
        return self.url
    
    def get_owner(self) -> str:
        self.get_env_vars()
        return self.owner
    
    def get_repository(self) -> str:
        self.get_env_vars()
        return self.repository
    
    def execute_get_request(self, url, headers, params) -> requests.Response:
        return requests.get(url, headers=headers, params=params)
    
    def execute_post_request(self, url,  data=None, json=None, **kwargs) -> requests.Response:
        if self.dry_run:
            click.echo("Dry run: simulating post request. Request would be:")
            click.echo(data)
            with requests_mock.Mocker() as m:
                m.post(url=url, text=data, json=json, **kwargs)
                return requests.post(url=url, data=data, json=json, **kwargs)
        else:
            return requests.post(url=url, data=data, json=json, **kwargs)            
