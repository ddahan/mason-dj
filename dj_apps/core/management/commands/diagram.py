from __future__ import annotations

from django.apps import AppConfig, apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models

from core.utils.shell_utils import sh

from .d2 import D2Diagram, D2Shape, D2SQLRow
from .d2.connection import D2Connection, Direction
from .d2.helpers import flatten
from .d2.shape import Shape

"""
These classes are used to organize and build Django D2 schemas using introspection.

Some random notes:
- classes (ProjectD2, AppD2, ModelD2, FieldD2) mirror Django structures, they are holders
for these classes.
- __init__ methods create classes that introspect and organize useful data
- build_<...> methods generate actual D2 classes (D2Shape, D2Connection, D2SQLRow, etc.)
- dj_<...> attributes are used to pass Django full object to keep the context

Usage:
1 - Create a ProjectD2 instance
2 - Call build method on this instance to build the diagram (this will build the shapes first, then the connections).
"""


class ProjectD2:
    apps: list[AppD2]

    def __init__(self, excluded_apps: list[AppConfig] = None) -> None:
        if excluded_apps is None:
            excluded_apps = []

        self.apps = [
            AppD2(dj_app=a)
            for a in list(apps.get_app_configs())
            if a.name not in excluded_apps
        ]

    def build(self) -> D2Diagram:
        return D2Diagram(shapes=self.build_shapes(), connections=self.build_connections())

    def build_shapes(self) -> list[D2Shape]:
        return [app.build_shape() for app in self.apps]

    def build_connections(self) -> list[D2Connection]:
        return flatten([app.build_connections() for app in self.apps])

    def debug(self) -> None:
        """Show a CLI reprensentation (for debug purpose only)"""
        for app in self.apps:
            print(f"[{app.name}]")
            for model in app.models:
                print(f"  {model.name}")
                for f in model.fields:
                    print(f"    - {f.name} - {f.description} {f.constraint}")
            print("\n")


class AppD2:
    dj_app: AppConfig
    models: list[ModelD2]

    def __init__(self, dj_app) -> None:
        self.dj_app = dj_app
        self.models = [
            ModelD2(dj_model=m, parent_app=self) for m in self.dj_app.get_models()
        ]

    @property
    def name(self) -> str:  # sugar
        return self.dj_app.name

    def build_shape(self) -> D2Shape:
        return D2Shape(  # this shape is a container
            name=self.name,
            shape=Shape.rectangle,
            shapes=[model.build_shape() for model in self.models],
        )

    def build_connections(self) -> list[D2Connection]:
        return flatten([model.build_connections() for model in self.models])


class ModelD2:
    parent_app: AppD2
    dj_model: models.Model
    fields: list[FieldD2]

    def __init__(self, parent_app, dj_model) -> None:
        self.dj_model = dj_model
        self.parent_app = parent_app
        self.fields = [
            FieldD2(dj_field=f, parent_model=self) for f in dj_model._meta.fields
        ]

    @property
    def name(self) -> str:  # sugar
        return self.dj_model._meta.object_name

    def build_shape(self) -> D2Shape:
        return D2Shape(
            name=self.name,
            shape=Shape.sql_table,
            sql_rows=[field.build_sql_row() for field in self.fields],
        )

    def build_connections(self) -> list[D2Connection]:
        return flatten([field.build_connections() for field in self.fields])


class FieldD2:
    parent_model: ModelD2
    dj_field: models.Field

    def __init__(self, parent_model, dj_field) -> None:
        self.dj_field = dj_field  # not very useful as is, except for future inspection
        self.parent_model = parent_model

    @property
    def name(self) -> str:
        return self.dj_field.name

    @property
    def constraint(self) -> str:
        return "".join(
            [
                "🔑" if self.dj_field.primary_key else "",
                "🤖" if self.dj_field.auto_created else "",
                "🔍" if self.dj_field.db_index else "",
            ]
        )

    @property
    def description(self) -> str:
        """Return the relation to the model if it's a related field, or the type of the
        field if it's a normal field."""

        if self.dj_field.related_model:  # FK / M2M / 1T1
            if self.dj_field.one_to_one:
                prefix = "0neToOne"
            elif self.dj_field.many_to_one:
                prefix = "ForeignKey"
            elif self.dj_field.many_to_many:
                prefix = "ManyToMany"
            else:
                raise ValueError("A relation should at least be one of provided field")
            return f"{prefix} → {self.dj_field.related_model._meta.object_name}"
        else:
            return type(self.dj_field).__name__

    def build_sql_row(self) -> D2SQLRow:
        return D2SQLRow(
            identifier=self.name,
            description=self.description,
            constraint=self.constraint,
        )

    def build_connections(self) -> list[D2Connection]:
        """Build potential connections between existing shapes."""

        if not any(
            [
                self.dj_field.one_to_one,
                self.dj_field.many_to_one,
                self.dj_field.many_to_many,
            ]
        ):
            return []

        return [
            D2Connection(
                shape_1=app_model_display(self.parent_model.dj_model),
                shape_2=app_model_display(self.dj_field.related_model),
                direction=Direction.BOTH if self.dj_field.many_to_many else Direction.TO,
            )
        ]


def app_model_display(dj_model) -> str:
    """Get a string formatted as <app_name>.<Model>
    This is used to describe D2 connections"""
    return f"{dj_model._meta.app_label}.{dj_model._meta.object_name}"


class Command(BaseCommand):
    help = "Generate a diagram view of Django models, using d2."

    def handle(self, *args, **options):
        # Config
        OUTPUT_FOLDER = "docs/"
        OUTPUT_D2_FILE = OUTPUT_FOLDER + "diagram.d2"
        OUTPUT_SVG_FILE = OUTPUT_FOLDER + "diagram.svg"
        EXCLUDED_APPS = settings.DJANGO_APPS + settings.THIRD_PARTY_APPS

        # Script
        self.stdout.write("Contructing graph from Django apps...")
        project = ProjectD2(excluded_apps=EXCLUDED_APPS)
        diagram = project.build()

        self.stdout.write("Writing graph to file...")
        with open(OUTPUT_D2_FILE, "w", encoding="utf-8") as f:
            f.write(str(diagram))
            self.stdout.write(f"Done! ({OUTPUT_D2_FILE})")
        self.stdout.write("Converting d2 file to svg and opening browser...")

        process = sh(
            f"d2 --watch  --sketch --theme 5 {OUTPUT_D2_FILE} {OUTPUT_SVG_FILE}",
            blocking=False,
        )
        # NOTE: this is dirty code as there is no option to automatic closing
        self.stdout.write("Waiting a few seconds before killing the process..")
        sh("sleep 2")
        sh(f"kill -9 {process.pid}")
