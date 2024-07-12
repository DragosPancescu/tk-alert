import tkinter as tk
import copy
import textwrap

from tkinter import font


def check_parent_type(parent: tk.Widget, supported_parent_types: tuple[tk.Widget]) -> None:
    if not isinstance(parent, supported_parent_types):
        raise TypeError(
            f"Unsupported parent type: {type(parent)}, supported (derived from) types are: {supported_parent_types}"
        )


def truncate_text(alert: tk.Widget, parent: tk.Tk | tk.Frame | tk.Toplevel, icon_width: int) -> str:
    text_font = font.Font(font=alert.cget("font"))  # Gets Font object
    ellipsis = "..."
    ellipsis_width = text_font.measure(ellipsis)

    truncated_text = copy.deepcopy(alert.text)

    # Max pixel width for our Alert as it is 1/4 of the parent container
    max_pixel_width = parent.winfo_width() * alert.width_percentage - ellipsis_width - icon_width

    # While text width in pixel count is bigger than the maximum pixel width allowed we truncate characters
    while (text_font.measure(truncated_text) > (max_pixel_width - ellipsis_width) and len(truncated_text) > 0):
        truncated_text = truncated_text[:-1]

    # No change
    if truncated_text == alert.text:
        return alert.text
    
    # Smaller then ellipsis we just return ellipsis
    if len(truncated_text[:-len(ellipsis)]) < len(ellipsis):
        return ellipsis
    
    # Corner case where the truncated text is between the second and fourth condition we return the text after 
    # it is processed by textwrap.shorten() to be sure we don't break words
    shortened_text = textwrap.shorten(truncated_text, len(truncated_text) - len(ellipsis), placeholder=ellipsis)
    if " " in truncated_text and text_font.measure(shortened_text) < max_pixel_width:
        return shortened_text
    
    # Happy path just return ellipsis instead of the last 3 characters
    return truncated_text[:-len(ellipsis)] + ellipsis


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