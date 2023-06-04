from typing import List
import click
from core.github import GithubAPI
from core.openai import OpenAIAPI
from utils.environment import prompt_for_missing_environment_variables
from utils.dry_run import execute_dry_run

@click.command()
@click.argument("discussion_ids", nargs=-1, type=int)
@click.option("--labels", multiple=True, help="Labels to add to the discussions.")
@click.option("--dry-run", is_flag=True, help="Print the command that would be executed, but do not execute it.")
def label_discussions(discussion_ids: List[int], labels: List[str], dry_run: bool):
    """
    Add labels to discussions using the OpenAI API to propose labels for the discussion.

    :param discussion_ids: List of discussion ids to add labels to.
    :param labels: List of labels to add to the discussions.
    :param dry_run: If True, print the command that would be executed, but do not execute it.
    """
    prompt_for_missing_environment_variables()

    github_api = GithubAPI()
    openai_api = OpenAIAPI()

    for discussion_id in discussion_ids:
        discussion = github_api.get_discussion(discussion_id)

        if not labels:
            proposed_labels = openai_api.propose_labels_for_discussion(discussion)
        else:
            proposed_labels = labels

        if dry_run:
            execute_dry_run("label_discussions", discussion_id, proposed_labels)
        else:
            github_api.add_labels_to_discussion(discussion_id, proposed_labels)