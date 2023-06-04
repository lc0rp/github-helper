### Manipulate git discussions from commandline
### ===========================================

This script provides a commandline interface to manipulate git discussions.

Copy .env.template to .env and fill in the values.

## Usage

```bash
$ python ./github_helper.py --help
Usage: github_helper.py [OPTIONS] COMMAND [ARGS]...

Options:
  --dry-run  Print the command that would be executed, but do not execute it.
  --help     Show this message and exit.

Commands:
  list-discussions  List discussions.
```

```bash
$ python ./github_helper.py list-discussions --help
Usage: github_helper.py list-discussions [OPTIONS]

  List discussions.

Options:
  --created-after TEXT           Return discussions created after this date
                                 (YYYY-MM-DD).
  --created-before TEXT          Return discussions created before this date
                                 (YYYY-MM-DD).
  --open                         Return only open discussions.
  --closed                       Return only closed discussions.
  --criteria TEXT                key:value pairs to filter by, separated by
                                 commas. Tested:-
                                 author:<username>,category:<category_name>
  --text TEXT                    Text to search for in the discussion body,
                                 title or comments.
  --limit INTEGER                The number of items to return.
  --sort [updated|interactions]  Sort by: default, updated or interactions.
  --sort-dir [asc|desc]          Sort direction: asc or desc (default).
  --help                         Show this message and exit.
  ```
When you've listed discussions, you can perform the following actions on them:

```bash
Displayed 1 - 50 of 346 discussion.

Actions: 
[q]: quit.
[n]: next page.
[p]: previous page.
[c #<number>]: close discussion #<number>.
[i #<number>]: convert #<number> to issue and close.
[ca]: close all.
[ia]: convert all to issues and close.

Next action: 
```
