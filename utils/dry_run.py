def execute_dry_run(command: str, args: list) -> None:
    """
    Executes a dry run of the given command with the provided arguments.

    :param command: The command to execute.
    :param args: The list of arguments for the command.
    """
    print(f"Dry run: {command} {' '.join(args)}")