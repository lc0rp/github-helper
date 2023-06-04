import os

import click
from core.github.base import GithubBaseClient
import requests
from typing import Dict, List, Union
from pydantic import BaseModel

class Issue(BaseModel):
    id: int | None
    title: str
    body: str
    labels: List[str] | None
    url: str | None

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

class GithubRestClient(GithubBaseClient):
    def __init__(self) -> None:
        self.get_env_vars()
        self.headers = self.get_github_api_headers()
    
    def get_issues(self, criteria: Dict[str, Union[str, int]]) -> List[Issue]:
        url = f"{self.get_github_url()}/issues"
        headers = self.get_github_api_headers()
        response = self.get_url(url, headers=headers, params=criteria)
        response.raise_for_status()
        return [Issue(**issue) for issue in response.json()]

    def get_issue_comments(self, issue_id: int) -> List[Comment]:
        url = f"{self.get_github_url()}/issues/{issue_id}/comments"
        headers = self.get_github_api_headers()
        response = self.execute_get_request(url, headers=headers)
        response.raise_for_status()
        return [Comment(**comment) for comment in response.json()]

    def get_discussion_comments(self, discussion_id: int) -> List[Comment]:
        url = f"{self.get_github_url()}/discussions/{discussion_id}/comments"
        headers = self.get_github_api_headers()
        response = self.execute_get_request(url, headers=headers)
        response.raise_for_status()
        return [Comment(**comment) for comment in response.json()]

    def create_issue(self, title: str, body: str) -> Issue:
        url = f"{self.get_github_url()}/issues"
        headers = self.get_github_api_headers()
        data = {"title": title, "body": body}
        response = self.execute_post_request(url, headers=headers, json=data)
        response.raise_for_status()
        return Issue(**response.json())

    def create_discussion(self, title: str, body: str, category: str) -> Discussion:
        url = f"{self.get_github_url()}/discussions"
        headers = self.get_github_api_headers()
        data = {"title": title, "body": body, "category": category}
        response = self.execute_post_request(url, headers=headers, json=data)
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
        response = self.execute_post_request(url, headers=headers, json=data)
        response.raise_for_status()
        return Comment(**response.json())

    def add_discussion_comment(self, discussion_id: int, comment: str) -> Comment:
        url = f"{self.get_github_url()}/discussions/{discussion_id}/comments"
        headers = self.get_github_api_headers()
        data = {"body": comment}
        response = self.execute_post_request(url, headers=headers, json=data)
        response.raise_for_status()
        return Comment(**response.json())

    def add_labels_to_issue(self, issue_id: int, labels: List[str]) -> List[Label]:
        url = f"{self.get_github_url()}/issues/{issue_id}/labels"
        headers = self.get_github_api_headers()
        data = {"labels": labels}
        response = self.execute_post_request(url, headers=headers, json=data)
        response.raise_for_status()
        return [Label(**label) for label in response.json()]

    def add_labels_to_discussion(self, discussion_id: int, labels: List[str]) -> List[Label]:
        url = f"{self.get_github_url()}/discussions/{discussion_id}/labels"
        headers = self.get_github_api_headers()
        data = {"labels": labels}
        response = self.execute_post_request(url, headers=headers, json=data)
        response.raise_for_status()
        return [Label(**label) for label in response.json()]

