from .connection import D2Connection
from .shape import D2Shape


class D2Diagram:
    def __init__(
        self,
        shapes: list[D2Shape] | None = None,
        connections: list[D2Connection] | None = None,
    ):
        self.shapes = shapes or []
        self.connections = connections or []

    def add_shape(self, shape: D2Shape):
        self.shapes.append(shape)

    def add_connection(self, connection: D2Connection):
        self.connections.append(connection)

    def __repr__(self) -> str:
        shapes = [str(shape) for shape in self.shapes]
        connections = [str(connection) for connection in self.connections]

        return "\n".join(shapes + connections)
