import click
from core.github import GithubAPI
from core.openai import OpenAIAPI
from utils.environment import prompt_for_missing_environment_variables
from utils.dry_run import execute_dry_run

@click.command()
@click.argument("issue_ids", nargs=-1, type=int)
@click.option("--labels", multiple=True, help="Labels to add to the issues.")
@click.option("--dry-run", is_flag=True, help="Print the command that would be executed, but do not execute it.")
def label_issues(issue_ids, labels, dry_run):
    """
    Add labels to issues. Takes a list of issue IDs and labels as arguments.
    Uses a call to the OpenAI API to propose labels for the issue if no labels are provided.
    """
    prompt_for_missing_environment_variables()

    github_api = GithubAPI()
    openai_api = OpenAIAPI()

    for issue_id in issue_ids:
        if not labels:
            issue = github_api.get_issue(issue_id)
            proposed_labels = openai_api.propose_labels_using_openai_api(issue)
            labels_to_add = [label.name for label in proposed_labels]
        else:
            labels_to_add = labels

        if dry_run:
            execute_dry_run("label_issues", issue_id, labels_to_add)
        else:
            github_api.add_labels_to_issue(issue_id, labels_to_add)
            click.echo(f"Labels {', '.join(labels_to_add)} added to issue {issue_id}.")