import requests
from utils.environment import GITHUB_URL, GITHUB_TOKEN
from utils.dry_run import execute_dry_run

def create_discussion(title: str, body: str, dry_run: bool = False):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    data = {
        "title": title,
        "body": body,
    }

    url = f"{GITHUB_URL}/repos/:owner/:repo/discussions"

    if dry_run:
        execute_dry_run("POST", url, headers=headers, json=data)
    else:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            print("Discussion created successfully.")
            print(response.json())
        else:
            print(f"Error creating discussion: {response.status_code} - {response.text}")

def run(args):
    title = args[0]
    body = args[1]
    dry_run = "--dry-run" in args

    create_discussion(title, body, dry_run)