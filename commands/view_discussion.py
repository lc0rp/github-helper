import requests
from pydantic import BaseModel
from utils.environment import GITHUB_URL, GITHUB_TOKEN

class Discussion(BaseModel):
    id: int
    title: str
    body: str
    created_at: str
    updated_at: str
    author: str
    state: str
    category: str

def get_discussion(discussion_id: int) -> Discussion:
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(f"{GITHUB_URL}/discussions/{discussion_id}", headers=headers)
    response.raise_for_status()
    data = response.json()
    return Discussion(
        id=data["id"],
        title=data["title"],
        body=data["body"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
        author=data["user"]["login"],
        state=data["state"],
        category=data["category"]["name"],
    )

def view_discussion(discussion_id: int) -> None:
    discussion = get_discussion(discussion_id)
    print(f"ID: {discussion.id}")
    print(f"Title: {discussion.title}")
    print(f"Body: {discussion.body}")
    print(f"Created at: {discussion.created_at}")
    print(f"Updated at: {discussion.updated_at}")
    print(f"Author: {discussion.author}")
    print(f"State: {discussion.state}")
    print(f"Category: {discussion.category}")

def run(args: list[str]) -> None:
    if len(args) != 1:
        print("Error: view_discussion command requires exactly 1 argument (discussion_id)")
        return

    discussion_id = int(args[0])
    view_discussion(discussion_id)