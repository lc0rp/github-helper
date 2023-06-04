"""Entry point for github_helper."""
import click
from utils.environment import prompt_for_missing_environment_variables
from commands.list_discussions import list_discussions

@click.group()
@click.option("--dry-run", is_flag=True, default=True, help="Print the command that would be executed, but do not execute it.")
@click.pass_context
def cli(ctx, dry_run):
    if dry_run:
        click.echo("Dry run mode: Active - Only read operations will be executed. To execute write operations, run with --no-dry-run.")
        
    ctx.ensure_object(dict)
    ctx.obj["DRY_RUN"] = dry_run
    prompt_for_missing_environment_variables(dry_run=dry_run)
    
cli.add_command(list_discussions)

if __name__ == "__main__":
    cli()