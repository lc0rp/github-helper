import requests
from utils.environment import GITHUB_URL, GITHUB_TOKEN
from utils.dry_run import execute_dry_run

def add_discussion_comment(discussion_id: int, comment: str, dry_run: bool = False) -> str:
    url = f"{GITHUB_URL}/discussions/{discussion_id}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {
        "body": comment,
    }

    if dry_run:
        return execute_dry_run("POST", url, headers=headers, json=data)

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return f"Comment added to discussion {discussion_id}."
    else:
        return f"Error adding comment to discussion {discussion_id}: {response.text}"

def run(args):
    discussion_id = int(args[0])
    comment = args[1]
    dry_run = "--dry-run" in args

    result = add_discussion_comment(discussion_id, comment, dry_run)
    print(result)