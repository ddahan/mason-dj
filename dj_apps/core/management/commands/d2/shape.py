from __future__ import annotations

from enum import Enum

from .connection import D2Connection
from .helpers import add_label_and_properties, flatten, indent
from .style import D2Style


class Shape(Enum):
    rectangle = "rectangle"
    square = "square"
    page = "page"
    parallelogram = "parallelogram"
    document = "document"
    cylinder = "cylinder"
    queue = "queue"
    package = "package"
    step = "step"
    callout = "callout"
    stored_data = "stored_data"
    person = "person"
    diamond = "diamond"
    oval = "oval"
    circle = "circle"
    hexagon = "hexagon"
    cloud = "cloud"
    text = "text"
    code = "code"
    sql_table = "sql_table"
    image = "image"
    classs = "class"
    sequence_diagram = "sequence_diagram"


class D2Text:
    def __init__(
        self,
        # The actual text body (multiline is fine)
        text: str,
        # The format, eg) md, tex, html, css etc
        formatting: str,
        # The number of pipes to use
        pipes: int = 1,
    ):
        self.text = text
        self.formatting = formatting
        self.pipes = pipes

    def lines(self) -> list[str]:
        sep = "|" * self.pipes
        return [f"{sep}{self.formatting}", *self.text.split("\n"), sep]

    def __repr__(self) -> str:
        return "\n".join(self.lines())


class D2Shape:
    def __init__(
        self,
        name: str,
        # The label of this shape (default: given name)
        label: str | None = None,
        # The actual 2D shape of this shape (default: rectangle)
        shape: Shape | None = None,
        # A list of child shapes (when this shape is a container)
        shapes: list[D2Shape] | None = None,
        # The style of this shape
        style: D2Style | None = None,
        # Connections for the child shapes (NOT the connections for this shape)
        connections: list[D2Connection] | None = None,
        # A shape this is near
        near: str | None = None,
        **kwargs: D2Text,
    ):
        self.name = name
        self.label = label
        self.shape = shape
        self.shapes = shapes or []
        self.style = style
        self.connections = connections or []
        self.near = near
        self.kwargs = kwargs

    def add_shape(self, shape: D2Shape):
        self.shapes.append(shape)

    def add_connection(self, connection: D2Connection):
        self.connections.append(connection)

    def lines(self) -> list[str]:
        shapes = flatten([shape.lines() for shape in self.shapes])
        connections = flatten([connection.lines() for connection in self.connections])
        properties = shapes + connections

        if self.shape:
            properties.append(f"shape: {self.shape.value}")

        if self.near:
            properties.append(f"near: {self.near}")

        if self.style:
            properties += self.style.lines()

        for key, value in self.kwargs.items():
            other_property = value.lines()
            other_property_line_1 = other_property[0]
            other_property_lines_other = other_property[1:-1]
            other_property_line_end = other_property[-1]
            properties += [
                f"{key}: {other_property_line_1}",
                *indent(other_property_lines_other),
                other_property_line_end,
            ]

        lines = add_label_and_properties(self.name, self.label, properties)

        return lines

    def __repr__(self) -> str:
        lines = self.lines()
        return "\n".join(lines)
