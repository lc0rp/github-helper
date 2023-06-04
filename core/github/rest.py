import os

import click
from utils.environment import prompt_for_missing_environment_variables
import requests
from typing import Dict, List, Union
from pydantic import BaseModel

class Issue(BaseModel):
    id: int
    title: str
    body: str
    state: str
    labels: List[str]
    url: str

class Discussion(BaseModel):
    id: int
    title: str
    body: str
    state: str
    category: str
    labels: List[str]

class Comment(BaseModel):
    id: int
    body: str
    author: str

class Label(BaseModel):
    id: int
    name: str

class GithubRestClient:
    def __init__(self) -> None:
        self.get_vars()
        self.headers = self.get_github_api_headers()
        self.dry_run = self.get_dry_run()
    
    def get_vars(self) -> Dict[str, str]:
        vars = prompt_for_missing_environment_variables()
        self.token = vars.get("GITHUB_TOKEN")
        self.url = vars.get("GITHUB_URL")
        self.dry_run = vars.get("DRY_RUN")
        
    def get_github_api_headers(self) -> Dict[str, str]:
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable not set")
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json"}

    def get_github_url(self) -> str:
        if not self.url:
            raise ValueError("GITHUB_URL environment variable not set")
        return self.url
    
    def get_issues(self, criteria: Dict[str, Union[str, int]]) -> List[Issue]:
        url = f"{self.get_github_url()}/issues"
        headers = self.get_github_api_headers()
        response = requests.get(url, headers=headers, params=criteria)
        response.raise_for_status()
        return [Issue(**issue) for issue in response.json()]

    def get_discussions(self, ids: list[int] = None, criteria: str | Dict[str, Union[str, int]]=None) -> List[Discussion]:
        url = f"{self.get_github_url()}/discussions"
        headers = self.get_github_api_headers()
        # Parse criteria if it's a string
        if isinstance(criteria, str):
            criteria = parse_criteria(criteria)
        
        response = requests.get(url, headers=headers, params=criteria)
        response.raise_for_status()
        return [Discussion(**discussion) for discussion in response.json()]

    def get_issue_comments(self, issue_id: int) -> List[Comment]:
        url = f"{self.get_github_url()}/issues/{issue_id}/comments"
        headers = self.get_github_api_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return [Comment(**comment) for comment in response.json()]

    def get_discussion_comments(self, discussion_id: int) -> List[Comment]:
        url = f"{self.get_github_url()}/discussions/{discussion_id}/comments"
        headers = self.get_github_api_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return [Comment(**comment) for comment in response.json()]

    def create_issue(self, title: str, body: str) -> Issue:
        url = f"{self.get_github_url()}/issues"
        headers = self.get_github_api_headers()
        data = {"title": title, "body": body}
        if self.dry_run:
            click.echo("Dry run: creating issue")
            click.echo(data)
            return Issue(**data)
        else:
            print("!!Creating issue!!")
            return
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return Issue(**response.json())

    def create_discussion(self, title: str, body: str, category: str) -> Discussion:
        url = f"{self.get_github_url()}/discussions"
        headers = self.get_github_api_headers()
        data = {"title": title, "body": body, "category": category}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return Discussion(**response.json())

    def close_issue(self, issue_id: int) -> None:
        url = f"{self.get_github_url()}/issues/{issue_id}"
        headers = self.get_github_api_headers()
        data = {"state": "closed"}
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()

    def close_discussion(self, discussion_id: int) -> None:
        url = f"{self.get_github_url()}/discussions/{discussion_id}"
        headers = self.get_github_api_headers()
        data = {"state": "closed"}
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()

    def add_issue_comment(self, issue_id: int, comment: str) -> Comment:
        url = f"{self.get_github_url()}/issues/{issue_id}/comments"
        headers = self.get_github_api_headers()
        data = {"body": comment}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return Comment(**response.json())

    def add_discussion_comment(self, discussion_id: int, comment: str) -> Comment:
        url = f"{self.get_github_url()}/discussions/{discussion_id}/comments"
        headers = self.get_github_api_headers()
        data = {"body": comment}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return Comment(**response.json())

    def add_labels_to_issue(self, issue_id: int, labels: List[str]) -> List[Label]:
        url = f"{self.get_github_url()}/issues/{issue_id}/labels"
        headers = self.get_github_api_headers()
        data = {"labels": labels}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return [Label(**label) for label in response.json()]

    def add_labels_to_discussion(self, discussion_id: int, labels: List[str]) -> List[Label]:
        url = f"{self.get_github_url()}/discussions/{discussion_id}/labels"
        headers = self.get_github_api_headers()
        data = {"labels": labels}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return [Label(**label) for label in response.json()]

