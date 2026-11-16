"""
Main module that hosts the Alert and AlertGenerator classes.

The package will use this module to import Alert, AlertGenerator and AlertType.

Custom configuration for the alert will be done using AlertGenerator, not by accessing the Alert class implementation.

 - Unless of course you feel the need to :)
"""

# To make typing compatible with 3.8
from __future__ import annotations

import tkinter as tk
import copy

from .constants import (
    AlertType,
    DESIGN_MAP,
    ANCHOR_TO_COORDINATES_OPTION,
    SUPPORTED_PARENT_TYPES
)

from .alert_utils import (
    check_parent_type,
    truncate_text,
    update_x_margin,
    update_y_margin
)


class Alert(tk.Button):
    """Alert widget, derived from tk.Button.

    Takes as init arguments the following: 
     - parent (tk.Tk | tk.Frame | tk.Toplevel): Parent of the Alert widget.
     - text (str): Text displayed in the Alert message.
     - type (AlertType): Type of the alert (info, warning, error or success)
     - anchor (str): Anchor that determines the placement, supports tk anchor constants
     - margin (int): Margin of the Alert widget on screen
     - width_percentage (flaot): Used to calculate width of the alert in accordance to the width of the parent

    Supports all the other Widget.configure() kwargs that a tk.Button has available.
    """

    def __init__(self, parent: tk.Tk | tk.Frame | tk.Toplevel, text: str, type: AlertType, anchor: str, margin: int, width_percentage: float, **kwargs) -> None:
        # Enforce parent type before init
        if not check_parent_type(parent, SUPPORTED_PARENT_TYPES):
            raise TypeError(
                f"Unsupported parent type: {type(parent)}, supported (derived from) types are: {SUPPORTED_PARENT_TYPES}"
            )
            
        super().__init__(parent)
        
        # Properties
        self._parent = parent
        self._text = text
        self._width_percentage = width_percentage
        self._anchor = anchor
        self._margin = margin
        
        # Set default command if command method is not provided
        if not kwargs.get("command", None):
            kwargs["command"] = self.destroy
            
        # Configs
        self.design = self._get_design(type, **kwargs)
        self.configure(**self.design)
        self._placement_kwargs = self._calculate_placement_kwargs()

        # Placement follows the parent natively (relative coordinates), so the only thing
        # left to do when the Alert is resized is to re-fit the text to the new width
        self.bind("<Configure>", self._configure_callback)
    
    @property
    def text(self):
        return self._text
    
    @property
    def width_percentage(self):
        return self._width_percentage
    
    ##### <Configure> bind callback logic #####
    
    def _configure_callback(self, event):
        self.__update_alert_text()

    def __update_alert_text(self):
        truncated_text = truncate_text(self, self._parent, self.design["image"].width())
        if truncated_text != self.cget("text"):
            self.configure(text=truncated_text)

    #####

    def _get_design(self, type: AlertType, **kwargs) -> dict:
        design = copy.deepcopy(DESIGN_MAP[type])
        
        # Set icon
        icon_path = design["icon_path"]
        design["image"] = tk.PhotoImage(file=icon_path)
        
        design.pop("icon_path")

        # Transform text
        truncated_text = truncate_text(self, self._parent, design["image"].width())
        if truncated_text.endswith("..."):
            pass
            # TODO: In the future attach tooltip if text is truncated

        design["text"] = truncated_text

        # Update design with kwargs
        design = {**design, **kwargs}

        return design

    def _calculate_placement_kwargs(self) -> dict:
        # Relative position inside the parent, based on the anchor. Tk's place geometry
        # manager keeps it up to date when the parent is resized.
        relative_position = ANCHOR_TO_COORDINATES_OPTION[self._anchor]

        # Pixel offset from that relative position, pointing inwards
        x_offset = update_x_margin(0, self._margin, self._anchor)
        y_offset = update_y_margin(0, self._margin, self._anchor)

        placement = {
            "anchor": self._anchor,
            "relx": relative_position["x"],
            "rely": relative_position["y"],
            "x": x_offset,
            "y": y_offset,
            "relwidth": self._width_percentage,
        }
        return placement

    def place_alert(self) -> None:
        self.place(**self._placement_kwargs)
        self.lift()


class AlertGenerator():
    """Driver class for placing alerts on the screen.

    Takes as init argument only the parent of the alert, where the Alert widget will sit when placed.
    Restricted to the following Widgets: tk.Tk, tk.Frame, tk.TopLevel

    .send() is the functionality that sends alerts to the parent Widget.

    Ideally the main app class should initialize an AlertGenerator object internally and use the .send() function whenever a notification needs to be sent to the user.

    As after each .send() call the Alert widget gets destroyed it should not impact the memory to have the object as a class attribute.
    """

    def __init__(self, parent: tk.Tk | tk.Frame | tk.Toplevel) -> None:
        # Enforce parent type before init
        if not check_parent_type(parent, SUPPORTED_PARENT_TYPES):
            raise TypeError(
                f"Unsupported parent type: {type(parent)}, supported (derived from) types are: {SUPPORTED_PARENT_TYPES}"
            )

        self._parent = parent

    @property
    def parent(self):
        return self._parent
        
    def send(self, text: str, type: AlertType, anchor: str | None = tk.NW, duration: int | None = 2, margin: int | None = 15, width_percentage: float | None = 0.33, **kwargs) -> None:
        """Create the Alert Widget, places it according to the anchor for the specified duration and then destroys it from memory.

        Args:
         - text: Text message to be sent
         - type: Type of alert, check AlertType enum for possible values
         - anchor: (optional) Anchor that determines the placement, supports tk anchor constants. Defaults to tk.NW
         - duration (optional): How much time, in seconds, should the Alert be shown to the user. Defaults to 2.
         - margin (optional): Margin of the Alert widget. Defaults to 15.
         - width_percentage (optional): Used to calculate width of the alert in accordance to the width of the parent, Defaults to 0.33

        Supports all the other Widget.configure() kwargs that a tk.Button has available.
        """
        
        # Checks
        if duration and duration <= 0:
            raise ValueError(f"Negative duration value: {duration}, allowed values are greater or equal than 0.")
        
        if margin and margin <= 0:
            raise ValueError(f"Negative margin value: {margin}, allowed values are greater or equal than 0.")
        
        if width_percentage and (width_percentage <= 0 or width_percentage > 1):
            raise ValueError(f"Out of bounds width_percentage value: {width_percentage}, allowed values are between 0 (exclusive) and 1 (inclusive)")
        
        # Create Alert Widget
        alert = Alert(self._parent, text, type, anchor, margin, width_percentage, **kwargs)

        # Place it
        alert.place_alert()

        # Wait duration and destroy
        alert.after(duration * 1000, alert.destroy)
