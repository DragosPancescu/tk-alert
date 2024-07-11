import tkinter as tk
import copy
import textwrap

from tkinter import font


def check_parent_type(parent: tk.Widget, supported_parent_types: tuple[tk.Widget]) -> None:
    if not isinstance(parent, supported_parent_types):
        raise TypeError(
            f"Unsupported parent type: {type(parent)}, supported (derived from) types are: {supported_parent_types}"
        )


def truncate_text(alert: tk.Widget, parent: tk.Tk | tk.Frame | tk.Toplevel, text: str, icon_width: int) -> str:
    text_font = font.Font(font=alert.cget("font"))  # Gets Font object
    ellipsis = "..."
    ellipsis_width = text_font.measure(ellipsis)

    truncated_text = copy.deepcopy(text)

    # Max pixel width for our Alert as it is 1/4 of the parent container
    max_pixel_width = parent.winfo_width() * 0.25 - ellipsis_width - icon_width

    # While text width in pixel count is bigger than the maximum pixel width allowed we truncate characters
    while (text_font.measure(truncated_text) > (max_pixel_width - ellipsis_width) and len(truncated_text) > 0):
        truncated_text = truncated_text[:-1]

    if truncated_text == text:
        return text
    
    if len(truncated_text[:-3]) < len(ellipsis):
        return ellipsis
    
    shortened_text = textwrap.shorten(truncated_text, len(truncated_text) - len(ellipsis), placeholder=ellipsis)
    if " " in truncated_text and text_font.measure(shortened_text) < max_pixel_width:
        return shortened_text
    
    return truncated_text[:-3] + ellipsis


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