import tkinter as tk
import copy
import textwrap

from tkinter import font

from .constants import (
    AlertType, 
    DESIGN_MAP, 
    ANCHOR_TO_COORDINATES_OPTION, 
    SUPPORTED_PARENT_TYPES
)

from .alert_utils import (
    check_parent_type,
    update_x_margin,
    update_y_margin
)

class Alert(tk.Button):
    """Alert widget, derived from tk.Button.
    Takes as init arguments the following: 
        parent (tk.Tk | tk.Frame | tk.Toplevel): Parent of the Alert widget.
        text (str): Text displayed in the Alert message.
        type (AlertType): Type of the alert (info, warning, error or success)
        anchor (str): Anchor that determines the placement, supports tk anchor constants
        margin (int): Margin of the Alert widget on screen
    
    Supports all the other Widget.configure() kwargs that a tk.Button has available.
    """
    def __init__(self, parent: tk.Tk | tk.Frame | tk.Toplevel, text: str, type: AlertType, anchor: str, margin: int, **kwargs) -> None:
        check_parent_type(parent, SUPPORTED_PARENT_TYPES)
        super().__init__(parent)
        
        self.configure(
            **self._get_design(parent, text, type, **kwargs),
            command=self.destroy
        )
        self._placement_kwargs = self._calculate_placement_kwargs(parent, anchor, margin)
    
    # TODO: Handle truncated text when changing parent size dynamically
    def _truncate_text(self, parent: tk.Tk | tk.Frame | tk.Toplevel, text: str) -> str:
        text_font = font.Font(font=self.cget("font")) # Get Font object
        
        max_pixel_width = parent.winfo_width() * 0.25 # Max pixel width for our Alert as it is 1/4 of the parent container
        
        ellipsis = "..."
        ellipsis_width = text_font.measure(ellipsis)
        truncated_text = copy.deepcopy(text)

        while text_font.measure(truncated_text) > (max_pixel_width - ellipsis_width) and len(truncated_text) > 0:
            truncated_text = truncated_text[:-1]

        if truncated_text != text:
            truncated_text = textwrap.shorten(truncated_text, len(truncated_text) - len(ellipsis), placeholder=ellipsis)
            
        return truncated_text

    def _get_design(self, parent: tk.Tk | tk.Frame | tk.Toplevel, text: str, type: AlertType, **kwargs) -> dict:
        design = copy.deepcopy(DESIGN_MAP[type])
        
        truncated_text = self._truncate_text(parent, text)
        if truncated_text != text:
            pass
            # TODO: Put tooltip if text is truncated
        
        design["text"] = truncated_text
        
        # Update design with kwargs
        design = {**design, **kwargs}

        return design

    def _calculate_placement_kwargs(self, parent: tk.Tk | tk.Frame | tk.Toplevel, anchor: str, margin: int) -> dict:
        parent.update_idletasks()  # Ensure dimensions are up to date

        # Calculate the relative position based on the anchor
        margin_options = ANCHOR_TO_COORDINATES_OPTION[anchor]
        x = margin_options["x"] * parent.winfo_width()
        y = margin_options["y"] * parent.winfo_height()

        # Update x with margin
        x = update_x_margin(x, margin, anchor)

        # Update y with margin
        y = update_y_margin(y, margin, anchor)

        placement = {"anchor": anchor, "x": x, "y": y, "relwidth": 0.25}
        return placement

    def place_alert(self) -> None:
        self.place(**self._placement_kwargs)


class AlertGenerator():
    """Driver class for placing alerts on the screen
    
    Takes as init argument only the parent of the alert, where the Alert widget will sit when placed.
    Restricted to the following Widgets: tk.Tk, tk.Frame, tk.TopLevel
    
    .send() is the functionality that sends alerts to the parent Widget.
    
    Ideally the main app class should initialize an AlertGenerator object internally and use the .send() function whenever a notification needs to be sent to the user.
    
    As after each .send() call the Alert widget gets destroyed it should not impact the memory to have the object as a class attribute.
    """
    def __init__(self, parent: tk.Tk | tk.Frame | tk.Toplevel) -> None:
        # Check to see if parent has an allowed type
        check_parent_type(parent, SUPPORTED_PARENT_TYPES)
            
        self._parent = parent

    def send(self, text: str, type: AlertType, anchor: str, duration: int | None = 2, margin: int | None = 15, **kwargs) -> None:
        """_summary_

        Args:
            text: Text message to be sent
            type: Type of alert, check AlertType enum for possible values
            anchor: Anchor that determines the placement, supports tk anchor constants. Example tk.NW
            duration (optional): How much time, in seconds, should the Alert be shown to the user. Defaults to 2.
            margin (optional): Margin of the Alert widget. Defaults to 15.
        
        Supports all the other Widget.configure() kwargs that a tk.Button has available.
        """
        alert = Alert(self._parent, text, type, anchor, margin, **kwargs)
        alert.place_alert()

        # Wait duration and destroy
        alert.after(duration * 1000, alert.destroy)