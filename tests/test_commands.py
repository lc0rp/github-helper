import pytest
from unittest.mock import MagicMock
from commands import (
    convert_discussions_to_issues,
    list_discussions,
    list_issues,
    close_issues,
    close_discussions,
    view_issue,
    view_discussion,
    view_issue_comments,
    view_discussion_comments,
    add_issue_comment,
    add_discussion_comment,
    create_issue,
    create_discussion,
    find_similar_issues,
    find_similar_discussions,
    label_issues,
    label_discussions,
)

def test_convert_discussions_to_issues():
    convert_discussions_to_issues.run = MagicMock()
    args = ["1", "2", "3"]
    convert_discussions_to_issues.run(args)
    convert_discussions_to_issues.run.assert_called_once_with(args)

def test_list_discussions():
    list_discussions.run = MagicMock()
    args = ["state:open", "category:question"]
    list_discussions.run(args)
    list_discussions.run.assert_called_once_with(args)

def test_list_issues():
    list_issues.run = MagicMock()
    args = ["state:open", "sort:created"]
    list_issues.run(args)
    list_issues.run.assert_called_once_with(args)

def test_close_issues():
    close_issues.run = MagicMock()
    args = ["1", "2", "3"]
    close_issues.run(args)
    close_issues.run.assert_called_once_with(args)

def test_close_discussions():
    close_discussions.run = MagicMock()
    args = ["1", "2", "3"]
    close_discussions.run(args)
    close_discussions.run.assert_called_once_with(args)

def test_view_issue():
    view_issue.run = MagicMock()
    args = ["1"]
    view_issue.run(args)
    view_issue.run.assert_called_once_with(args)

def test_view_discussion():
    view_discussion.run = MagicMock()
    args = ["1"]
    view_discussion.run(args)
    view_discussion.run.assert_called_once_with(args)

def test_view_issue_comments():
    view_issue_comments.run = MagicMock()
    args = ["1"]
    view_issue_comments.run(args)
    view_issue_comments.run.assert_called_once_with(args)

def test_view_discussion_comments():
    view_discussion_comments.run = MagicMock()
    args = ["1"]
    view_discussion_comments.run(args)
    view_discussion_comments.run.assert_called_once_with(args)

def test_add_issue_comment():
    add_issue_comment.run = MagicMock()
    args = ["1", "This is a test comment."]
    add_issue_comment.run(args)
    add_issue_comment.run.assert_called_once_with(args)

def test_add_discussion_comment():
    add_discussion_comment.run = MagicMock()
    args = ["1", "This is a test comment."]
    add_discussion_comment.run(args)
    add_discussion_comment.run.assert_called_once_with(args)

def test_create_issue():
    create_issue.run = MagicMock()
    args = ["Test issue", "This is a test issue."]
    create_issue.run(args)
    create_issue.run.assert_called_once_with(args)

def test_create_discussion():
    create_discussion.run = MagicMock()
    args = ["Test discussion", "This is a test discussion."]
    create_discussion.run(args)
    create_discussion.run.assert_called_once_with(args)

def test_find_similar_issues():
    find_similar_issues.run = MagicMock()
    args = ["1"]
    find_similar_issues.run(args)
    find_similar_issues.run.assert_called_once_with(args)

def test_find_similar_discussions():
    find_similar_discussions.run = MagicMock()
    args = ["1"]
    find_similar_discussions.run(args)
    find_similar_discussions.run.assert_called_once_with(args)

def test_label_issues():
    label_issues.run = MagicMock()
    args = ["1", "bug", "enhancement"]
    label_issues.run(args)
    label_issues.run.assert_called_once_with(args)

def test_label_discussions():
    label_discussions.run = MagicMock()
    args = ["1", "question", "feedback"]
    label_discussions.run(args)
    label_discussions.run.assert_called_once_with(args)