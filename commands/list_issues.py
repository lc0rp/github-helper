import click
import requests
from typing import List
from utils.environment import GITHUB_URL, GITHUB_TOKEN
from utils.dry_run import execute_dry_run
from criteria.base import parse_criteria

@click.command()
@click.argument("ids", type=str, required=False)
@click.option("--ids", )
def list_issues(ids: str=None, criteria: str, dry_run: bool = False) -> List[str]:
    criteria_list = parse_criteria(criteria)
    query_params = {criterion.name: criterion.value for criterion in criteria_list}
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    
    url = f"{GITHUB_URL}/issues"
    if dry_run:
        execute_dry_run("GET", url, headers=headers, params=query_params)
        return []

    response = requests.get(url, headers=headers, params=query_params)
    response.raise_for_status()
    issues = response.json()

    issue_strings = []
    for issue in issues:
        issue_strings.append(f"Issue #{issue['number']}: {issue['title']}")

    return issue_strings