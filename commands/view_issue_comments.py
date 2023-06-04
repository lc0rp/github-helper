import requests
from pydantic import BaseModel
from typing import List
from utils.environment import GITHUB_URL, GITHUB_TOKEN
from utils.dry_run import execute_dry_run

class Comment(BaseModel):
    id: int
    body: str
    user: str

def view_issue_comments(issue_id: int, dry_run: bool = False) -> List[str]:
    url = f"{GITHUB_URL}/repos/:owner/:repo/issues/{issue_id}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    if dry_run:
        execute_dry_run("GET", url, headers=headers)
        return []

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    comments_data = response.json()
    comments = [Comment(**comment_data) for comment_data in comments_data]

    output = []
    for comment in comments:
        output.append(f"Comment ID: {comment.id}")
        output.append(f"User: {comment.user}")
        output.append(f"Body: {comment.body}")
        output.append("")

    return output