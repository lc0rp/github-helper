import requests
from core.github import get_github_api_headers
from utils.environment import GITHUB_URL
from pydantic import BaseModel
from typing import List

class Issue(BaseModel):
    id: int
    title: str
    body: str
    labels: List[str]

def find_similar_issues(issue_id: int, dry_run: bool = False) -> List[str]:
    headers = get_github_api_headers()
    issue_url = f"{GITHUB_URL}/repos/:owner/:repo/issues/{issue_id}"
    response = requests.get(issue_url, headers=headers)
    response.raise_for_status()
    issue_data = response.json()
    issue = Issue(**issue_data)

    search_url = f"{GITHUB_URL}/search/issues"
    search_query = f"repo::owner/:repo type:issue {issue.title}"
    search_params = {"q": search_query}
    search_response = requests.get(search_url, headers=headers, params=search_params)
    search_response.raise_for_status()
    search_data = search_response.json()

    similar_issues = []
    for item in search_data["items"]:
        if item["id"] != issue.id:
            similar_issue = Issue(**item)
            similar_issues.append(similar_issue)

    if dry_run:
        print(f"Found {len(similar_issues)} similar issues to issue {issue_id}:")
        for similar_issue in similar_issues:
            print(f"- {similar_issue.id}: {similar_issue.title}")
    else:
        return [f"{similar_issue.id}: {similar_issue.title}" for similar_issue in similar_issues]