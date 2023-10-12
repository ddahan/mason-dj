from django.core.management import CommandError, call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from ...utils.shell_utils import yes_or_no
from .mixins.dump_and_load import DumpAndLoadMixin


class Command(DumpAndLoadMixin, BaseCommand):
    help = """Slight wrapper around dumpdata to:
    - have default parameters
    - have a confirmation prompt
    - create 1 file per model, to ease reading"""

    @transaction.atomic()
    def handle(self, *args, **options):
        if yes_or_no(
            "This will erase current yaml files, and will create new ones from"
            " exising database."
        ):
            for model in self.get_models():
                full_path = self.get_full_path(model)
                try:
                    call_command(
                        "dumpdata",
                        self.get_model_path(model),
                        "--format",
                        "yaml",
                        "--output",
                        full_path,
                        "--verbosity",
                        0,
                    )
                except CommandError:
                    self.stderr.write(self.style.ERROR(f"⨉ {full_path}"))
                else:
                    # use custom output as dumpdata one is useless
                    self.stdout.write(self.style.SUCCESS(f"✓ {full_path}"))
