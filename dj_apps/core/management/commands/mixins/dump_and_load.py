from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.db.models.base import ModelBase


class DumpAndLoadMixin:
    """Used by both mydumpdata and myloaddata command to share common parameters and
    methods"""

    def get_models(self) -> list[ModelBase]:
        """Return all installed models using introspection, except the one specified
        because they are useless and can create integrity errors during deserialization.
        """
        BLACKLISTED_APPS = ["sessions", "admin"]
        return [
            model
            for model in apps.get_models()
            if model._meta.app_label not in BLACKLISTED_APPS
        ]

    def get_full_path(self, model) -> Path:
        BACKUP_PATH = settings.BASE_DIR / "backup_data"
        return BACKUP_PATH / f"{self.get_model_path(model)}.yaml"

    def get_model_path(self, model) -> str:
        return f"{model._meta.app_label}.{model._meta.object_name}"
