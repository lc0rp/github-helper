import click
import gql
from core.github.gql import GithubGqlClient
import requests
from pydantic import BaseModel
from utils.environment import GITHUB_URL, GITHUB_TOKEN


@click.command()
@click.option('--number', type=int, help='The number of the discussion to view.')
@click.option('--id', type=int, help='The id of the discussion to view.')
def view_discussion(number: int, id: int):
    """View discussion."""
    click.echo(f"Retrieving discussion...\n")
    github_client = GithubGqlClient()
    
    if id:
        query = gql(f"""
            query {{
                repository(owner: "{github_client.owner}", name: "{github_client.repository}") {{
                    discussion(id: "{id}") {{
                        id
                        number
                        title
                        url
                        author{{login}}
                        category{{id,name}}
                        comments{{totalCount}}
                        closed
                        createdAt
                        publishedAt
                        lastEditedAt
                        updatedAt
                        bodyText
                    }}
                }}
            }}
        """)
    elif number:
        pass
        
    query = f"""query{{
        search(query: "repo:{github_client.owner}/{github_client.repository} {query_string}", type: DISCUSSION, {limit_clause}) {{
                discussionCount
                nodes {{
                ... on Discussion {{
                    id
                    number
                    title
                    url
                    author{{login}}
                    category{{id,name}}
                    comments{{totalCount}}
                    closed
                    createdAt
                    publishedAt
                    lastEditedAt
                    updatedAt
                    bodyText
                }}
            }}
        }}
    }}"""
    
    # print(query)

    # Execute the query
    results = github_client.execute(query=query)
    manage_results(results)
    
def display_discussion(discussion):
    click.echo(f"{'-'*TERMINAL_WIDTH}")
    click.echo(f"#{discussion['number']} {discussion['title']} by {discussion['author']['login']}")
    click.echo(f"    Comments: {discussion['comments']['totalCount']} | Status: {'Closed' if discussion['closed'] else 'Open'} | URL: {discussion['url']}")
    click.echo(f"    Body: {discussion['bodyText'][0:100]}...")
    click.echo(f"{'-'*TERMINAL_WIDTH}")
    
    
class Discussion(BaseModel):
    id: int
    title: str
    body: str
    created_at: str
    updated_at: str
    author: str
    state: str
    category: str

def get_discussion(discussion_id: int) -> Discussion:
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(f"{GITHUB_URL}/discussions/{discussion_id}", headers=headers)
    response.raise_for_status()
    data = response.json()
    return Discussion(
        id=data["id"],
        title=data["title"],
        body=data["body"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
        author=data["user"]["login"],
        state=data["state"],
        category=data["category"]["name"],
    )

def view_discussion(discussion_id: int) -> None:
    discussion = get_discussion(discussion_id)
    print(f"ID: {discussion.id}")
    print(f"Title: {discussion.title}")
    print(f"Body: {discussion.body}")
    print(f"Created at: {discussion.created_at}")
    print(f"Updated at: {discussion.updated_at}")
    print(f"Author: {discussion.author}")
    print(f"State: {discussion.state}")
    print(f"Category: {discussion.category}")

def run(args: list[str]) -> None:
    if len(args) != 1:
        print("Error: view_discussion command requires exactly 1 argument (discussion_id)")
        return

    discussion_id = int(args[0])
    view_discussion(discussion_id)