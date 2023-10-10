from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.base import ModelBase

from ...utils.shell_utils import yes_or_no

YAML_TO_DB = "YAML_TO_DB"
DB_TO_YAML = "DB_TO_YAML"


class Command(BaseCommand):
    help = (
        "Create in database objects from serialized YAML objects for backup OR create "
        "YAML from existing database."
        "Note that it can fails if data integrity is not respected."
    )

    BACKUP_PATH = settings.BASE_DIR / "backup_data"

    def get_models(self) -> list[ModelBase]:
        # Theses apps are useless and can create integrity errors at deserialization
        blacklisted_apps = ["contenttypes", "sessions", "admin"]
        return [
            model
            for model in apps.get_models()
            if model._meta.app_label not in blacklisted_apps
        ]

    def get_full_path(self, model) -> Path:
        return self.BACKUP_PATH / f"{self.get_model_path(model)}.yml"

    def get_model_path(self, model):
        return f"{model._meta.app_label}.{model._meta.object_name}"

    def add_arguments(self, parser):
        parser.add_argument("operation", type=str, help=f"{YAML_TO_DB} or {DB_TO_YAML}")

    @transaction.atomic()
    def handle(self, *args, **options):
        operation = options["operation"]
        if operation == YAML_TO_DB:
            if yes_or_no(
                "This will flush current database and will recreate objects from existing"
                " yaml backup files."
            ):
                call_command("flush", "--noinput")
                self.stdout.write("Exising database has been flushed.")
                for model in self.get_models():
                    full_path = self.get_full_path(model)
                    try:
                        with open(full_path, "r") as readfile:
                            for obj in serializers.deserialize("yaml", readfile):
                                obj.save()
                                self.stdout.write(self.style.SUCCESS(f"✓ {obj}"))
                    except FileNotFoundError:
                        self.stdout.write(
                            self.style.WARNING(
                                f"⨉ {full_path} file not found. The script will"
                                " continue."
                            )
                        )
        elif operation == DB_TO_YAML:
            if yes_or_no(
                "This will erase current yaml files, and will create new ones from"
                " exising database."
            ):
                YAMLSerializer = serializers.get_serializer("yaml")
                yaml_serializer = YAMLSerializer()

                for model in self.get_models():
                    full_path = self.get_full_path(model)
                    with open(full_path, "w+") as out:
                        yaml_serializer.serialize(model.objects.all(), stream=out)
                        self.stdout.write(self.style.SUCCESS(f"✓ {full_path}"))
        else:
            self.stderr.write(
                f"Invalid operation provided. Must be {YAML_TO_DB} or {DB_TO_YAML}"
            )
