import warnings

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from ...utils.shell_utils import yes_or_no
from .mixins.dump_and_load import DumpAndLoadMixin


class Command(DumpAndLoadMixin, BaseCommand):
    help = """Slight wrapper around loaddata to:
    - flush the database first
    - have default parameters
    - have a confirmation prompt
    - remove warnings if a file has no model in it
    """

    @transaction.atomic()
    def handle(self, *args, **options):
        if yes_or_no(
            "This will flush current database and will recreate objects from existing"
            " yaml backup files."
        ):
            call_command("flush", "--noinput")
            self.stdout.write("Exising database has been flushed.")
            for model in self.get_models():
                # if a model is detected but has no related file, it will raise an error
                full_path = self.get_full_path(model)
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=RuntimeWarning)
                    call_command(
                        "loaddata",
                        full_path,
                        "--verbosity",
                        2,
                    )
                    self.stdout.write("\n\n")
