import subprocess


def yes_or_no(question) -> bool:
    """
    Input the given yes/no question to a user, and returns the result as boolean.
    """
    reply = str(input(question + " Continue? (y/n): ")).lower().strip()
    return bool(reply == "y")


def sh(command, blocking=True) -> subprocess.Popen:
    """
    Execute the given command in a shell.
    If blocking is True, it will behave like `call` command.
    Return the process (for example to get the pid to kill it later).
    TODO: remove quotes from args otherwise it does not work in that case
    """
    args = command.split()
    process = subprocess.Popen(args)
    if blocking is True:
        process.wait()
    return process
