from enum import Enum


class Direction(Enum):
    TO = "->"
    FROM = "<-"
    BOTH = "<->"
    NONE = "--"


class D2Connection:
    def __init__(
        self,
        shape_1: str,
        shape_2: str,
        direction: Direction,
        label: str | None = None,
    ):
        self.shape_1 = shape_1
        self.shape_2 = shape_2
        self.direction = direction
        self.label = label

    def lines(self) -> list[str]:
        base = f"{self.shape_1} {self.direction.value} {self.shape_2}"
        if self.label:
            base += f": {self.label}"
        return [base]

    def __repr__(self) -> str:
        return "\n".join(self.lines())
