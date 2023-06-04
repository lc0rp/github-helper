import click
import gql
from core.github.rest import GithubRestClient
from core.github.gql import GithubGqlClient
from typing import List

VALID_CRITERIA_KEYS = ["author", "category"]
TERMINAL_WIDTH = 150

@click.command()
@click.option('--created-after', default=None, help='Return discussions created before this date (YYYY-MM-DD).')
@click.option('--created-before', default=None, help='Return discussions created before this date (YYYY-MM-DD).')
@click.option('--criteria', default=None, help='key:value pairs to filter by, separated by commas. Tested:- author:<username>,category:<category_name>')
@click.option('--limit', default=None, type=int, help='The number of items to return.')
@click.option('--sort', default=None, type=click.Choice('updated','interactions'), help='Sort by: default, updated or interactions.')
@click.option('--sort-dir', default='desc', type=click.Choice(['asc','desc']), help='Sort direction: asc or desc (default).')
def list_discussions(created_after, created_before, criteria, limit, sort, sort_dir):
    """List discussions."""
    click.echo(f"Listing discussions...\n")
    github_client = GithubGqlClient()
    # results = github_client.get_discussions(ids=ids) # , criteria=criteria, dry_run=dry_run)=
    query_parts = []
    if created_after is not None:
        date_query = f"created: {created_after}"
        if created_before is not None:
            date_query += f"..{created_before}"
        query_parts.append(date_query)
    
    elif created_before is not None:
        query_parts.append(f"created: ..{created_before}")
        
    if criteria is not None:
        # split criteria into key-value pairs
        criteria_parts = criteria.split(",")
        for part in criteria_parts:
            # split key-value pairs into key and value
            key, value = part.split("=")
            # Check if the key is a valid key
            if key not in VALID_CRITERIA_KEYS:
                raise ValueError(f"Invalid criteria: {key}")
            else:
                query_parts.append(f"{key}: {value}")
    
    if limit is not None:
        limit_clause = f"first: {limit}"
    else:
        limit_clause = "first: 50"
    
    if sort is not None:
        query_parts.append(f"sort: {sort}-{sort_dir}")
    
    query_string = " ".join(query_parts)
    query = f"""query{{
        search(query: "repo:{github_client.owner}/{github_client.repository} {query_string}", type: DISCUSSION, {limit_clause}) {{
                discussionCount
                nodes {{
                ... on Discussion {{
                    id
                    number
                    title
                    url
                    author{{login}}
                    category{{id,name}}
                    comments{{totalCount}}
                    closed
                    createdAt
                    publishedAt
                    lastEditedAt
                    updatedAt
                    bodyText
                }}
            }}
        }}
    }}"""
    
    # print(query)

    # Execute the query
    results = github_client.execute(query=query)
    manage_results(results)
    
def manage_results(results):
    total = results['search']['discussionCount']
    click.echo(f"Found {total} discussions")
    if total > 50:
        click.echo(f"Printing first 50:\n\n")
    
    display_max = 50 if total > 50 else total
    display_start = 1
    display_results(results, display_start, display_max, total)
    
def display_results(results, display_start, display_max, total):
    if display_start > display_max:
        display_count_max = display_start + display_max
    else:
        display_count_max = display_max
    display_count = display_start
    skipped = 0
    for discussion in results['search']['nodes']:
        # Skip first <display_start>-1 results
        while skipped < display_start - 1:
            skipped += 1
            continue
        
        # Print pretty results
        click.echo(f"{'-'*TERMINAL_WIDTH}")
        click.echo(f"{str(display_count).rjust(2, ' ')}: {discussion['createdAt']} - \"#{discussion['number']} {discussion['title']}\" by {discussion['author']['login']}")
        click.echo(f"    Comments: {discussion['comments']['totalCount']} | Status: {'Closed' if discussion['closed'] else 'Open'} | URL: {discussion['url']}")
        display_count += 1
        if display_count > display_count_max:
            break
    click.echo(f"{'-'*TERMINAL_WIDTH}")
    click.echo(f"Displayed {display_start} - {display_count-1} of {total} discussion.\n")
    if display_count < total:
        ask_for_next(results, display_count, display_max, total)

def ask_for_next(results, display_count, display_max, total):
        options = ["[q]: quit",]
        if display_count < total:
            options.append(f"[n]: next {display_max}")
            
        if display_count > display_max:
            options.append(f"[p]: previous {display_max}")
            
        options.append(f"[c #<number>]: close discussion #<number>")
        options.append(f"[i #<number>]: convert #<number> to issue and close.")
        options.append(f"[ca]: close all")
        options.append(f"[ia]: convert all to issues and close.")
        
        click.echo(f"Actions: {', '.join(options)}\n")
        command = click.prompt("Next action", type=str)
        if command == "q":
            exit()
        elif command == "n":
            display_results(results, display_count, display_max, total)
        elif command == "p":
            display_results(results, display_count - (display_max * 2), display_max, total)
        elif command == "ca":
            close_discussions(results)
        elif command == "ia":
            convert_discussions(results)
        elif command.startswith("c #"):
            close_discussion(results, command.replace("c #", ""))
        elif command.startswith("i #"):
            convert_discussion(results, command.replace("i #", ""))

        ask_for_next(results, display_count, display_max, total)

def close_discussions(results):
    confirm = click.confirm("Are you sure you want to close all discussions?")
    if confirm:
        for discussion in results['search']['nodes']:
            close_discussion(results, discussion['number'], no_confirm=True)
        click.echo(f"Closed all discussions. Exiting.")
        exit()
    else:
        return
    
def convert_discussions(results):
    confirm = click.confirm("Are you sure you want to convert all discussions to issues? This will close all discussions.")
    if confirm:
        for discussion in results['search']['nodes']:
            convert_discussion(results, discussion['number'], no_confirm=True)
        click.echo(f"Converted all discussions to issues. Exiting.")
        exit()
    else:
        return
    
def close_discussion(results, number, no_confirm=False):
    discussion = get_discussion(results, number)
    display_discussion(discussion)
    if not no_confirm:
        confirm = click.confirm(f"Are you sure you want to close discussion #{number}?")
        if not confirm:
            return
    github_client = GithubGqlClient()
    mutation = gql(f"""
        mutation {{
            closeDiscussion(input: {{id: "{discussion['id']}"}}) {{
                clientMutationId
            }}
        }}
    """)

    github_client.execute(mutation)
    click.echo(f"Closed discussion #{number}. Displayed results may not be updated till next search.")

def convert_discussion(results, number, no_confirm=False):
    discussion = get_discussion(results, number)
    display_discussion(discussion)
    if not no_confirm:
        confirm = click.confirm(f"Are you sure you want to convert discussion #{number} to an issue? This will close the discussion.")
        if not confirm:
            return
    github_client = GithubRestClient()
    # Create issue
    issue = github_client.create_issue(title=discussion['title'], body=discussion['bodyText'] + f"\n\nFrom discussion #{discussion[number]}: {discussion['url']}")
    click.echo(f"Created issue #{issue.id} from discussion #{number}.")
    # Close discussion
    close_discussion(results, number, no_confirm=True)
    
def get_discussion(results, number):
    for discussion in results['search']['nodes']:
        if discussion['number'] == int(number):
            return discussion
        
def display_discussion(discussion):
    click.echo(f"{'-'*TERMINAL_WIDTH}")
    click.echo(f"#{discussion['number']} {discussion['title']} by {discussion['author']['login']}")
    click.echo(f"    Comments: {discussion['comments']['totalCount']} | Status: {'Closed' if discussion['closed'] else 'Open'} | URL: {discussion['url']}")
    click.echo(f"    Body: {discussion['bodyText'][0:100]}...")
    click.echo(f"{'-'*TERMINAL_WIDTH}")
    
def list_discussions_old():
    query_part = ("""
            discussions(first: 10) {
                nodes {
                    id
                    databaseId
                    number
                    title
                    url
                    author {
                        login
                    }
                    category {
                        name
                    }
                    closed
                    bodyText
                    createdAt
                    lastEditedAt
                    publishedAt
                    updatedAt
                }
            }
        """)
