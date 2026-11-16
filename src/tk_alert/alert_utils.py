# To make typing compatible with 3.8
from __future__ import annotations

import tkinter as tk

from tkinter import font


def check_parent_type(parent: tk.Widget, supported_parent_types: tuple[tk.Widget]) -> bool:
    if not isinstance(parent, supported_parent_types):
        return False
    return True


def truncate_text(alert: tk.Widget, parent: tk.Tk | tk.Frame | tk.Toplevel) -> str:
    text_font = font.Font(font=alert.cget("font"))  # Gets Font object
    ellipsis = "..."

    # Everything in the Alert that is not text: icon, padding and borders
    non_text_width = alert.winfo_reqwidth() - text_font.measure(alert.cget("text"))

    # Max pixel width for the text, the Alert takes width_percentage of the parent container
    max_pixel_width = parent.winfo_width() * alert.width_percentage - non_text_width

    # No change
    if text_font.measure(alert.text) <= max_pixel_width:
        return alert.text

    # Remove characters until the text fits together with the ellipsis
    truncated_text = alert.text
    while truncated_text and text_font.measure(truncated_text + ellipsis) > max_pixel_width:
        truncated_text = truncated_text[:-1]

    # Don't cut a word in half, unless it is the only word left
    if " " in truncated_text and not alert.text[len(truncated_text)].isspace():
        truncated_text = truncated_text[:truncated_text.rindex(" ")]

    return truncated_text.rstrip() + ellipsis


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