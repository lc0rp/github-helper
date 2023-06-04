import requests
from core.github import get_github_api_headers
from utils.environment import GITHUB_URL
from utils.dry_run import execute_dry_run

def find_similar_discussions(discussion_id, dry_run=False):
    url = f"{GITHUB_URL}/discussions/{discussion_id}/similar"
    headers = get_github_api_headers()

    if dry_run:
        execute_dry_run("GET", url, headers=headers)
        return

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    similar_discussions = response.json()
    return similar_discussions