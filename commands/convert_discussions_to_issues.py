from core.github import GithubRestClient
from utils.dry_run import execute_dry_run

def convert_discussions_to_issues(discussion_ids, dry_run=False):
    github_client = GithubRestClient()

    for discussion_id in discussion_ids:
        discussion = github_client.get_discussions(discussion_id)
        if not discussion:
            print(f"Discussion with ID {discussion_id} not found.")
            continue

        issue_title = f"[Discussion] {discussion['title']}"
        issue_body = f"Originally posted by {discussion['user']['login']} at {discussion['created_at']}\n\n{discussion['body']}\n\n[Original discussion]({discussion['html_url']})"
        issue_data = {
            "title": issue_title,
            "body": issue_body
        }

        if dry_run:
            execute_dry_run("create_issue", issue_data)
        else:
            created_issue = github_client.create_issue(issue_data)
            print(f"Created issue #{created_issue['number']} for discussion #{discussion_id}")

            github_client.close_discussion(discussion_id)
            print(f"Closed discussion #{discussion_id}")