import tkinter as tk


def check_parent_type(parent: tk.Widget, supported_parent_types: tuple[tk.Widget]) -> None:
    if not isinstance(parent, supported_parent_types):
        raise TypeError(f"Unsupported parent type: {type(parent)}, supported (derived from) types are: {supported_parent_types}")


def update_x_margin(x: float, margin: int, anchor: str) -> float:
    if anchor in ["nw", "w", "sw"]:
        return x + margin

    if anchor in ["ne", "e", "se"]:
        return x - margin

    return x


def update_y_margin(y: float, margin: int, anchor: str) -> float:
    if anchor in ["nw", "n", "ne"]:
        return y + margin

    if anchor in ["sw", "s", "se"]:
        return y - margin

    return y