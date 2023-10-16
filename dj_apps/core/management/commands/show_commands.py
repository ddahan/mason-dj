from collections import defaultdict

from django.core.management import get_commands, load_command_class
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Show all commands with their help (unlike the built-in help command)."

    def handle(self, *args, **options):
        commands_dict = defaultdict(lambda: [])

        for name, app in get_commands().items():
            CommandClass = load_command_class(app, name)

            if app == "django.core":
                app = "django"
            else:
                app = app.rpartition(".")[-1]
            commands_dict[app].append((name, CommandClass.help or "no description"))

        for app in sorted(commands_dict):
            self.stdout.write(f"[{app}]", self.style.NOTICE)
            for name, help in sorted(commands_dict[app]):
                self.stdout.write(self.style.SUCCESS(f"    {name}: ") + help + "\n")
            print("\n")
