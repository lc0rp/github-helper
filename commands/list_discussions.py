import click
from core.github.rest import GithubRestClient
from core.github.gql import GithubGqlClient
from typing import List

VALID_CRITERIA_KEYS = ["author", "category"]
TERMINAL_WIDTH = 150

@click.command()
@click.option('--created-after', default=None, help='Return discussions created after this date (YYYY-MM-DD).')
@click.option('--created-before', default=None, help='Return discussions created before this date (YYYY-MM-DD).')
@click.option('--open', is_flag=True, help='Return only open discussions.')
@click.option('--closed', is_flag=True, help='Return only closed discussions.')
@click.option('--criteria', default=None, help='key:value pairs to filter by, separated by commas. Tested:- author:<username>,category:<category_name>')
@click.option('--text', default=None, help='Text to search for in the discussion body, title or comments.')
@click.option('--limit', default=None, type=int, help='The number of items to return.')
@click.option('--sort', default=None, type=click.Choice(['updated','interactions']), help='Sort by: default, updated or interactions.')
@click.option('--sort-dir', default='desc', type=click.Choice(['asc','desc']), help='Sort direction: asc or desc (default).')
def list_discussions(created_after, created_before, open, closed, criteria, text, limit, sort, sort_dir):
    """List discussions."""
    click.echo(f"Listing discussions...\n")
    github_client = GithubGqlClient()
    # results = github_client.get_discussions(ids=ids) # , criteria=criteria, dry_run=dry_run)=
    query_parts = []
    if created_after is not None:
        date_query = f"created:{created_after}"
        if created_before is not None:
            date_query += f"..{created_before}"
        query_parts.append(date_query)
    
    elif created_before is not None:
        query_parts.append(f"created:<{created_before}")
        
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
                query_parts.append(f"{key}:{value}")
    
    if text is not None:
        query_parts.append(text)
        
    if limit is not None:
        limit_clause = f"first: {limit}"
    else:
        limit_clause = "first: 50"
    
    if sort is not None:
        query_parts.append(f"sort:{sort}-{sort_dir}")
    
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
    
    if closed:
        results['search']['nodes'] = [discussion for discussion in results['search']['nodes'] if discussion['closed']]
        results['search']['discussionCount'] = len(results['search']['nodes'])
    elif open:
        results['search']['nodes'] = [discussion for discussion in results['search']['nodes'] if not discussion['closed']]
        results['search']['discussionCount'] = len(results['search']['nodes'])
        
    manage_results(results)
    
def manage_results(results):
    total = results['search']['discussionCount']
    click.echo(f"Found {total} discussions")
    if total > 50:
        click.echo(f"Displaying 50...\n")
    
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
        
        display_discussion(discussion, display_count, display_max)
        display_count += 1
        if display_count > display_count_max:
            break
    click.echo(f"{'-'*TERMINAL_WIDTH}")
    click.echo(f"Displayed {display_start} - {display_count-1} of {total} discussion.\n")
    ask_for_next_action(results, display_count, display_max, total)

def ask_for_next_action(results, display_count, display_max, total):
        options = ["[q]: quit",]
        if display_count < total:
            options.append(f"[n]: next {display_max}")
            
        if display_count > display_max:
            options.append(f"[p]: previous {display_max}")
            
        options.append(f"[c <number>,<number>]: close discussions.")
        options.append(f"[i <number>,<number>]: convert to issues and close.")
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
        elif command.startswith("c "):
            close_discussions(results, command.replace("c ", ""))
        elif command.startswith("i "):
            convert_discussions(results, command.replace("i ", ""))

        ask_for_next_action(results, display_count, display_max, total)

def close_discussions(results, numbers=None):
    confirm = click.confirm("Are you sure you want to close the discussions?")
    
    if not confirm:
        return
    else:
        discussions_to_close = []
        if numbers is not None:
            for number in str(numbers).split(','):
                discussions_to_close.append(get_discussion(results, number))
        else:
            discussions_to_close = results['search']['nodes']
            
        for discussion in discussions_to_close:
            close_discussion(results, discussion['number'], no_confirm=True)
            
        if numbers is not None:
            click.echo(f"Closed discussions {numbers}.")
            return
        else:
            click.echo(f"Closed all discussions. Exiting.")
            exit()
            
    
def convert_discussions(results, numbers=None):
    confirm = click.confirm("Are you sure you want to convert the discussions to issues? This will also close the discussions.")
    
    if not confirm:
        return
    else:
        discussions_to_convert = []
        if numbers is not None:
            for number in str(numbers).split(','):
                discussions_to_convert.append(get_discussion(results, number))
        else:
            discussions_to_convert = results['search']['nodes']
        
        for discussion in discussions_to_convert:
            convert_discussion(results, discussion['number'], no_confirm=True)
        
        if numbers is not None:
            click.echo(f"Converted discussions {numbers}.")
            return
        else:
            click.echo(f"Converted all discussions to issues. Exiting.")
            exit()
    
def close_discussion(results, number, no_confirm=False):
    discussion = get_discussion(results, number)
    display_discussion(discussion)
    click.echo(f"{'-'*TERMINAL_WIDTH}")
    if not no_confirm:
        confirm = click.confirm(f"Are you sure you want to close discussion #{number}?")
        if not confirm:
            return
    github_client = GithubGqlClient()
    mutation = f"""
        mutation {{
            closeDiscussion(input: {{discussionId: "{discussion['id']}"}}) {{
                clientMutationId
            }}
        }}
    """

    github_client.execute(query=mutation)
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
    issue = github_client.create_issue(title=discussion['title'], body=discussion['bodyText'] + f"\n\nFrom discussion #{discussion['number']}: {discussion['url']}")
    click.echo(f"Created issue #{issue.id} from discussion #{number}.")
    # Close discussion
    close_discussion(results, number, no_confirm=True)
    
def get_discussion(results, number):
    for discussion in results['search']['nodes']:
        if discussion['number'] == int(number):
            return discussion
        
def display_discussion(discussion, display_count=0, total=0):
    if total and display_count:
        # Figure out the number of spaces to pad the number with
        num_digits = len(str(total))
        display_count_str = str(display_count).rjust(num_digits, ' ') + ". | "
        row_prefix = f"{' '*(num_digits+1)} | " 
    elif display_count:
        display_count_str = str(display_count).rjust(2, ' ') + ". | "
        row_prefix = f"{' '*(3)} | "
    else:
        display_count_str = ""
        row_prefix = ""
        
    click.echo(f"{'-'*TERMINAL_WIDTH}")
    click.echo(f"{display_count_str}#{discussion['number']} - \"{discussion['title']}\" by {discussion['author']['login']}\n{row_prefix}")
    body_text = discussion['bodyText'].replace("\n", "\n" + row_prefix)
    click.echo(f"{row_prefix}{body_text[0 : TERMINAL_WIDTH - 10]}{'...'if len(body_text) > TERMINAL_WIDTH - 10 else ''}\n{row_prefix}")
    click.echo(f"{row_prefix}URL: {discussion['url']}")
    click.echo(f"{row_prefix}Category: {discussion['category']['name']} | Comments: {discussion['comments']['totalCount']} | Status: {'Closed' if discussion['closed'] else 'Open'}")
    click.echo(f"{row_prefix}Created: {discussion['createdAt']} | Updated: {discussion['updatedAt']} | Last Edited: {discussion['lastEditedAt']} | Published: {discussion['publishedAt']}")
    
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
