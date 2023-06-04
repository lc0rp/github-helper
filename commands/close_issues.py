import requests
from utils.environment import GITHUB_URL, GITHUB_TOKEN
from utils.dry_run import execute_dry_run

def close_issues(issue_ids, dry_run=False):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    closed_issues = []
    for issue_id in issue_ids:
        url = f"{GITHUB_URL}/repos/:owner/:repo/issues/{issue_id}"
        if dry_run:
            execute_dry_run("PATCH", url, headers=headers, json={"state": "closed"})
        else:
            response = requests.patch(url, headers=headers, json={"state": "closed"})
            if response.status_code == 200:
                closed_issues.append(response.json())
            else:
                print(f"Failed to close issue {issue_id}: {response.status_code} {response.text}")

    return closed_issues

def run(args):
    issue_ids = [int(arg) for arg in args if arg.isdigit()]
    dry_run = "--dry-run" in args

    closed_issues = close_issues(issue_ids, dry_run)
    if not dry_run:
        for issue in closed_issues:
            print(f"Closed issue {issue['number']}: {issue['title']}")