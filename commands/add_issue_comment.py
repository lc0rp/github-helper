import requests
from utils.environment import GITHUB_URL, GITHUB_TOKEN
from utils.dry_run import execute_dry_run

def add_issue_comment(issue_id: int, comment: str, dry_run: bool = False) -> str:
    url = f"{GITHUB_URL}/repos/:owner/:repo/issues/{issue_id}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {
        "body": comment,
    }

    if dry_run:
        return execute_dry_run("POST", url, headers=headers, json=data)

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return f"Comment added to issue {issue_id}."
    else:
        return f"Error adding comment to issue {issue_id}: {response.text}"