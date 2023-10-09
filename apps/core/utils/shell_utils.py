from subprocess import call


def yes_or_no(question) -> bool:
    """
    Input the given yes/no question to a user, and returns the result as boolean.
    """
    reply = str(input(question + " Continue? (y/n): ")).lower().strip()
    return bool(reply == "y")


def sh(command):
    """
    Execute the given command in a shell.
    TODO: remove quotes from args otherwise it does not work in that case
    """
    args = command.split()
    call(args)
