from typing import Dict
import click
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from core.github.base import GithubBaseClient

class GithubGqlClient(GithubBaseClient):
    def __init__(self) -> None:
        super().__init__()
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
        
        if self.dry_run and ("mutation" in str(query).lower()):
            click.echo("Dry run: Simulating query execution. Query would be:")
            click.echo(str(query))
            return query
        else:
            return self.client.execute(query)