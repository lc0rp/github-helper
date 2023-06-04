import requests
from core.github import get_github_api_headers
from utils.environment import prompt_for_missing_environment_variables

def view_issue(issue_id: int, dry_run: bool = False) -> None:
    prompt_for_missing_environment_variables()

    headers = get_github_api_headers()
    url = f"{GITHUB_URL}/repos/{GITHUB_REPOSITORY}/issues/{issue_id}"

    if dry_run:
        print(f"GET {url}")
        return

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        issue = response.json()
        print(f"Issue #{issue['number']}: {issue['title']}")
        print(f"State: {issue['state']}")
        print(f"Created at: {issue['created_at']}")
        print(f"Updated at: {issue['updated_at']}")
        print(f"Labels: {', '.join([label['name'] for label in issue['labels']])}")
        print(f"Assignees: {', '.join([assignee['login'] for assignee in issue['assignees']])}")
        print(f"Author: {issue['user']['login']}")
        print("\nDescription:")
        print(issue['body'])
    else:
        print(f"Error: Unable to fetch issue #{issue_id}. Status code: {response.status_code}")