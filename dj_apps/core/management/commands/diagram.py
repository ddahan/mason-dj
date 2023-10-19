from __future__ import annotations

from django.apps import AppConfig, apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models

from core.utils.shell_utils import sh

from .d2 import D2Diagram, D2Shape, D2SQLRow
from .d2.shape import Shape

"""
These classes are used to organize and build Django D2 schemas using introspection.

Some random notes:
- classes (ProjectD2, AppD2, ModelD2, FieldD2) mirror Django structures
- __init__ methods create classes that introspect and organize useful data
- build_<...> methods generate actual D2 classes (D2Shape, D2Connection, D2SQLRow, etc.)
- dj_<...> attributes are used to pass Django full object to keep context

Usage:
1 - Create a ProjectD2 instance
2 - Call build method on this instance to build the diagram
  2.1 - Build the shapes
  2.2 - Build the connections
"""


class ProjectD2:
    apps: list[AppD2]

    def __init__(
        self,
        excluded_apps: list[AppConfig] = settings.DJANGO_APPS + settings.THIRD_PARTY_APPS,
    ) -> None:
        self.apps = [
            AppD2(dj_app=a)
            for a in list(apps.get_app_configs())
            if a.name not in excluded_apps
        ]

    def build_shapes(self) -> list[D2Shape]:
        return [app.build_shape() for app in self.apps]

    # def build_connections(self, shapes: list[D2Shape]) -> list[D2Connection]:
    #     return [app.build_connections(shapes) for app in self.apps]

    def build(self) -> D2Diagram:
        shapes = self.build_shapes()
        return D2Diagram(shapes=shapes, connections=[])
        # connections = self.build_connections(shapes)
        # return D2Diagram(shapes=shapes, connections=connections)

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
        self.models = [ModelD2(dj_model=m) for m in self.dj_app.get_models()]

    @property
    def name(self) -> str:  # sugar
        return self.dj_app.name

    def build_shape(self) -> D2Shape:
        return D2Shape(  # this shape is a container
            name=self.name,
            shape=Shape.rectangle,
            shapes=[model.build_shape() for model in self.models],
        )

    # def build_connections(self, shapes) -> list[D2Connection]:
    #     return [model.build_connections(shapes) for model in self.models]


class ModelD2:
    dj_model: models.Model
    fields: list[FieldD2]

    def __init__(self, dj_model) -> None:
        self.dj_model = dj_model
        self.fields = [FieldD2(dj_field=f) for f in dj_model._meta.fields]

    @property
    def name(self) -> str:  # sugar
        return self.dj_model._meta.object_name

    def build_shape(self) -> D2Shape:
        return D2Shape(
            name=self.name,
            shape=Shape.sql_table,
            sql_rows=[field.build_sql_row() for field in self.fields],
        )

    # def build_connections(self, shapes) -> list[D2Connection]:
    #     return todo


class FieldD2:
    dj_field: models.Field

    def __init__(self, dj_field) -> None:
        self.dj_field = dj_field  # not very useful as is, except for future inspection

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


class Command(BaseCommand):
    help = "Generate a diagram view of Django models, using d2."

    def handle(self, *args, **options):
        OUTPUT_FOLDER = "docs/"
        OUTPUT_D2_FILE = OUTPUT_FOLDER + "diagram.d2"
        OUTPUT_SVG_FILE = OUTPUT_FOLDER + "diagram.svg"

        self.stdout.write("Contructing graph from Django apps...")
        diagram = ProjectD2().build()

        self.stdout.write("Writing graph to file...")
        with open(OUTPUT_D2_FILE, "w", encoding="utf-8") as f:
            f.write(str(diagram))
            self.stdout.write(f"Done! ({OUTPUT_D2_FILE})")
        self.stdout.write("Converting d2 file to svg and opening browser...")
        sh(f"d2 --watch  --sketch --theme 5 {OUTPUT_D2_FILE} {OUTPUT_SVG_FILE}")
