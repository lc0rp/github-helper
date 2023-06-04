import pytest
from unittest.mock import MagicMock
from core import github, openai
from utils import environment

def test_convert_discussions_to_issues():
    github.convert_discussions_to_issues = MagicMock()
    discussion_ids = [1, 2, 3]

    github_helper.convert_discussions_to_issues(discussion_ids)

    github.convert_discussions_to_issues.assert_called_once_with(discussion_ids)

def test_list_discussions():
    github.list_discussions = MagicMock()
    criteria = "state:open,category:question"

    github_helper.list_discussions(criteria)

    github.list_discussions.assert_called_once_with(criteria)

def test_list_issues():
    github.list_issues = MagicMock()
    criteria = "state:open,sort:created"

    github_helper.list_issues(criteria)

    github.list_issues.assert_called_once_with(criteria)

def test_close_issues():
    github.close_issues = MagicMock()
    issue_ids = [1, 2, 3]

    github_helper.close_issues(issue_ids)

    github.close_issues.assert_called_once_with(issue_ids)

def test_close_discussions():
    github.close_discussions = MagicMock()
    discussion_ids = [1, 2, 3]

    github_helper.close_discussions(discussion_ids)

    github.close_discussions.assert_called_once_with(discussion_ids)

def test_view_issue():
    github.view_issue = MagicMock()
    issue_id = 1

    github_helper.view_issue(issue_id)

    github.view_issue.assert_called_once_with(issue_id)

def test_view_discussion():
    github.view_discussion = MagicMock()
    discussion_id = 1

    github_helper.view_discussion(discussion_id)

    github.view_discussion.assert_called_once_with(discussion_id)

def test_view_issue_comments():
    github.view_issue_comments = MagicMock()
    issue_id = 1

    github_helper.view_issue_comments(issue_id)

    github.view_issue_comments.assert_called_once_with(issue_id)

def test_view_discussion_comments():
    github.view_discussion_comments = MagicMock()
    discussion_id = 1

    github_helper.view_discussion_comments(discussion_id)

    github.view_discussion_comments.assert_called_once_with(discussion_id)

def test_add_issue_comment():
    github.add_issue_comment = MagicMock()
    issue_id = 1
    comment = "Test comment"

    github_helper.add_issue_comment(issue_id, comment)

    github.add_issue_comment.assert_called_once_with(issue_id, comment)

def test_add_discussion_comment():
    github.add_discussion_comment = MagicMock()
    discussion_id = 1
    comment = "Test comment"

    github_helper.add_discussion_comment(discussion_id, comment)

    github.add_discussion_comment.assert_called_once_with(discussion_id, comment)

def test_create_issue():
    github.create_issue = MagicMock()
    title = "Test issue"
    body = "This is a test issue."

    github_helper.create_issue(title, body)

    github.create_issue.assert_called_once_with(title, body)

def test_create_discussion():
    github.create_discussion = MagicMock()
    title = "Test discussion"
    body = "This is a test discussion."

    github_helper.create_discussion(title, body)

    github.create_discussion.assert_called_once_with(title, body)

def test_find_similar_issues():
    github.find_similar_issues = MagicMock()
    issue_id = 1

    github_helper.find_similar_issues(issue_id)

    github.find_similar_issues.assert_called_once_with(issue_id)

def test_find_similar_discussions():
    github.find_similar_discussions = MagicMock()
    discussion_id = 1

    github_helper.find_similar_discussions(discussion_id)

    github.find_similar_discussions.assert_called_once_with(discussion_id)

def test_label_issues():
    openai.label_issues = MagicMock()
    issue_ids = [1, 2, 3]
    labels = ["bug", "enhancement"]

    github_helper.label_issues(issue_ids, labels)

    openai.label_issues.assert_called_once_with(issue_ids, labels)

def test_label_discussions():
    openai.label_discussions = MagicMock()
    discussion_ids = [1, 2, 3]
    labels = ["question", "general"]

    github_helper.label_discussions(discussion_ids, labels)

    openai.label_discussions.assert_called_once_with(discussion_ids, labels)

def test_environment_variables():
    environment.get_github_api_headers = MagicMock()
    environment.prompt_for_missing_environment_variables = MagicMock()

    github_helper.main()

    environment.get_github_api_headers.assert_called_once()
    environment.prompt_for_missing_environment_variables.assert_called_once()