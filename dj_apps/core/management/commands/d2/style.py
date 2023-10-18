from .helpers import add_label_and_properties


def stringify_bool(val: bool) -> str:
    return "true" if val else "false"


class D2Style:
    def __init__(
        self,
        stroke: str | None = None,
        stroke_width: int | None = None,
        fill: str | None = None,
        shadow: bool | None = None,
        opacity: float | None = None,
        stroke_dash: int | None = None,
        three_d: bool | None = None,
    ):
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.fill = fill
        self.shadow = shadow
        self.opacity = opacity
        self.stroke_dash = stroke_dash
        self.three_d = three_d

    def lines(self) -> list[str]:
        styles: list[str] = []

        if self.stroke:
            styles.append(f"stroke: {self.stroke}")

        if self.stroke_width:
            styles.append(f"stroke-width: {self.stroke_width}")

        if self.fill:
            styles.append(f"fill: {self.fill}")

        if self.shadow:
            styles.append(f"shadow: {stringify_bool(self.shadow)}")

        if self.opacity:
            styles.append(f"opacity: {self.opacity}")

        if self.stroke_dash:
            styles.append(f"stroke-dash: {self.stroke_dash}")

        if self.three_d:
            styles.append(f"3d: {stringify_bool(self.three_d)}")

        if len(styles) == 0:
            return []

        return add_label_and_properties("style", None, styles)

    def __repr__(self) -> str:
        lines = self.lines()
        return "\n".join(lines)
