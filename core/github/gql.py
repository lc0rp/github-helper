from typing import Dict
import click
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from utils.environment import prompt_for_missing_environment_variables

class GithubGqlClient:
    def __init__(self) -> None:
        self.get_env_vars()
        self.headers = self.get_github_api_headers()
        self.transport = RequestsHTTPTransport(url='https://api.github.com/graphql', headers=self.headers)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)
        self.owner = self.get_owner()
        self.repository = self.get_repository()
        
    def execute(self, partial_query: str=None, query: str=None) -> dict:
        if partial_query is not None:
            
            query = gql(f"""
                query {{
                    repository(owner: "{self.owner}", name: "{self.repository}") {{
                        {partial_query}
                    }}
                }}
            """)
        elif isinstance(query, str):
            query = gql(query)
        elif query is None or not isinstance(query, gql):
            raise ValueError("Either partial_query or valid query string or gql query must be specified.")
        
        if self.dry_run:
            click.echo("Dry run: executing query")
            click.echo(query)
            return query
        else:
            return self.client.execute(query)
    
    def get_env_vars(self) -> Dict[str, str]:
        env_vars = prompt_for_missing_environment_variables()
        self.token = env_vars.get("GITHUB_TOKEN")
        self.url = env_vars.get("GITHUB_URL")
        self.owner = self.url.split("/")[-2]
        self.repository = self.url.split("/")[-1]
        self.dry_run = env_vars.get("DRY_RUN")
        
    def get_github_api_headers(self) -> Dict[str, str]:
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json"}
    
    def get_owner(self) -> str:
        self.get_env_vars()
        return self.owner
    
    def get_repository(self) -> str:
        self.get_env_vars()
        return self.repository