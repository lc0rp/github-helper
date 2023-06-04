import click
import requests
from utils.environment import GITHUB_URL, GITHUB_TOKEN
from utils.dry_run import execute_dry_run

@click.command()
@click.argument("discussion_id", type=int)
@click.option("--dry-run", is_flag=True, help="Print the command that would be executed, but do not execute it.")
def view_discussion_comments(discussion_id, dry_run):
    """
    Displays comments of a discussion.

    Args:
        discussion_id (int): The ID of the discussion to view comments for.
        dry_run (bool): If True, print the command that would be executed, but do not execute it.
    """
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    url = f"{GITHUB_URL}/discussions/{discussion_id}/comments"

    if dry_run:
        execute_dry_run("GET", url, headers=headers)
        return

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        comments = response.json()
        for comment in comments:
            print(f"Comment ID: {comment['id']}")
            print(f"Author: {comment['user']['login']}")
            print(f"Created at: {comment['created_at']}")
            print(f"Updated at: {comment['updated_at']}")
            print(f"Body: {comment['body']}\n")
    else:
        print(f"Error: Unable to fetch discussion comments. Status code: {response.status_code}")