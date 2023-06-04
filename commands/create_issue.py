import requests
from utils.environment import GITHUB_URL, GITHUB_TOKEN
from utils.dry_run import execute_dry_run

def create_issue(title: str, body: str, dry_run: bool = False) -> str:
    url = f"{GITHUB_URL}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {
        "title": title,
        "body": body,
    }

    if dry_run:
        return execute_dry_run("create_issue", data)

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        issue = response.json()
        return f"Issue created: {issue['html_url']}"
    else:
        return f"Error creating issue: {response.status_code} - {response.text}"