from __future__ import annotations

from dataclasses import dataclass

from django.apps import AppConfig, apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models

from core.management.commands.d2 import D2Diagram, D2Shape
from core.utils.shell_utils import sh

from .d2.shape import D2SQLRow, Shape

##########################################################################################
# CONFIG
##########################################################################################

OUTPUT_FOLDER = "docs/"
OUTPUT_D2_FILE = OUTPUT_FOLDER + "diagram.d2"
OUTPUT_SVG_FILE = OUTPUT_FOLDER + "diagram.svg"

##########################################################################################
# DATA ORGANIZATION LAYER
# Select and organize relevant data in order to use them later for rendering
##########################################################################################


@dataclass
class ProjectForD2:
    """Contains all data for D2"""

    apps: list[AppForD2]

    def __init__(
        self, excluded_apps: list = settings.DJANGO_APPS + settings.THIRD_PARTY_APPS
    ) -> None:
        self.apps = [
            AppForD2(dj_app=a)
            for a in list(apps.get_app_configs())
            if a.name not in excluded_apps
        ]

    def debug(self) -> None:
        """Show a CLI reprensentation (for debug purpose only)"""
        for app in self.apps:
            print(f"[{app.name}]")
            for model in app.models:
                print(f"  {model.name}")
                for f in model.fields:
                    print(f"    - {f.name} - {f.description} {f.constraint}")
            print("\n")


@dataclass
class AppForD2:
    """Used to create a D2 container"""

    dj_app: AppConfig
    name: str
    models: list[ModelForD2]

    def __init__(self, dj_app) -> None:
        self.dj_app = dj_app
        self.name = dj_app.name
        self.models = [ModelForD2(dj_model=m) for m in self.dj_app.get_models()]


@dataclass
class ModelForD2:
    """Used to create a SQLTable D2 shape"""

    dj_model: models.Model
    name: str
    fields: list[FieldForD2]

    def __init__(self, dj_model) -> None:
        self.dj_model = dj_model
        self.name = dj_model._meta.object_name
        self.fields = [FieldForD2(dj_field=f) for f in dj_model._meta.fields]


@dataclass
class FieldForD2:
    """Used to create a D2 entry in a SQLTable shape"""

    dj_field: models.Field
    name: str
    description: str
    constraint: str

    def _get_related_prefix(self) -> str | None:
        if self.dj_field.one_to_one:
            return "0neToOne"
        if self.dj_field.many_to_one:
            return "ForeignKey"
        if self.dj_field.many_to_many:
            return "ManyToMany"
        else:
            raise ValueError("A relation should at least be one of provided field")

    @property
    def _constraint(self) -> str:
        s = ""
        if self.dj_field.primary_key:
            s += "🔑"
        if self.dj_field.auto_created:
            s += "🤖"
        return s

    @property
    def _description(self) -> str:
        """Display the relation to the model if it's a related field, or the type of the
        field if it's a normal field."""
        if self.dj_field.related_model:
            prefix = self._get_related_prefix()
            return f"{prefix} → {self.dj_field.related_model._meta.object_name}"
        else:
            return type(self.dj_field).__name__

    def __init__(self, dj_field) -> None:
        self.dj_field = dj_field  # not very useful as is, except for future inspection
        self.name = dj_field.name
        self.description = self._description
        self.constraint = self._constraint


##########################################################################################
# COMMAND FOR D2 GENERATION THEN SVG RENDERING
# Use organized data to fill
##########################################################################################


class Command(BaseCommand):
    help = "Generate a diagram view of Django models, using d2."

    def handle(self, *args, **options):
        self.stdout.write("Contructing a simple graph...")

        # TODO: this logic can live in the dataclasses too!

        project = ProjectForD2()

        shapes = []
        for app in project.apps:
            shapes.append(
                D2Shape(
                    name=app.name,
                    shapes=[
                        D2Shape(
                            name=model.name,
                            shape=Shape.sql_table,
                            sql_rows=[
                                D2SQLRow(
                                    identifier=field.name,
                                    description=field.description,
                                    constraint=field.constraint,
                                )
                                for field in model.fields
                            ],
                        )
                        for model in app.models
                    ],
                )
            )

        connections = []  # TODO

        diagram = D2Diagram(shapes=shapes, connections=connections)

        self.stdout.write("Writing graph to file...")
        with open(OUTPUT_D2_FILE, "w", encoding="utf-8") as f:
            f.write(str(diagram))
            self.stdout.write(f"Done! ({OUTPUT_D2_FILE})")
        self.stdout.write("Converting to svg and opening browser...")
        sh(f"d2 --watch  --sketch --theme 5 --center {OUTPUT_D2_FILE} {OUTPUT_SVG_FILE}")
