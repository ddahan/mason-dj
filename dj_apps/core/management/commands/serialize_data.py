from dataclasses import dataclass
from typing import Any

from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from ...utils.shell_utils import yes_or_no


@dataclass
class SerializableModel:
    app: str
    model: str

    @property
    def json_file(self) -> str:
        return self.model + ".json"


##########################################################################################
# CONFIG
##########################################################################################

SERIALIZABLE_MODELS = [
    # Fill the models to be processed
    SerializableModel("profiles", "User"),
]

# WARN: the backup file MUST exist, it will not be created automatically
BACKUP_PATH = settings.BASE_DIR / "backup_data"

##########################################################################################
# COMMAND
##########################################################################################

JSON_TO_DB = "JSON_TO_DB"
DB_TO_JSON = "DB_TO_JSON"


class Command(BaseCommand):
    help = (
        "Create in database objects from serialized JSON objects for backup OR create "
        "JSON from existing database."
        "It can fails if data integrity is not respected. "
    )

    def add_arguments(self, parser):
        parser.add_argument("operation", type=str, help=f"{JSON_TO_DB} or {DB_TO_JSON}")

    @transaction.atomic()
    def handle(self, *args, **options):
        operation = options["operation"]
        if operation == JSON_TO_DB:
            if yes_or_no(
                "This will flush current database and will create a new one from existing"
                " json backup files."
            ):
                call_command("flush", "--noinput")
                self.stdout.write("Exising database has been flushed.")
                for item in SERIALIZABLE_MODELS:
                    full_path = BACKUP_PATH / f"{item.json_file}"
                    try:
                        with open(full_path, "r") as readfile:
                            for obj in serializers.deserialize("json", readfile):
                                obj.save()
                                self.stdout.write(
                                    self.style.SUCCESS(f"{obj.object} is saved")
                                )
                    except FileNotFoundError:
                        self.stdout.write(
                            self.style.WARNING(
                                f"{item.json_file} file not found. The script will"
                                " continue."
                            )
                        )
        elif operation == DB_TO_JSON:
            if yes_or_no(
                "This will erase current json files, and will create new ones from"
                " exising database."
            ):
                JSONSerializer = serializers.get_serializer("json")
                json_serializer = JSONSerializer()

                for item in SERIALIZABLE_MODELS:
                    full_path = BACKUP_PATH / item.json_file
                    with open(full_path, "w+") as out:
                        Model: Any = apps.get_model(item.app, item.model)
                        json_serializer.serialize(Model.objects.all(), stream=out)
        else:
            self.stderr.write(
                f"Invalid operation provided. Must be {JSON_TO_DB} or {DB_TO_JSON}"
            )
