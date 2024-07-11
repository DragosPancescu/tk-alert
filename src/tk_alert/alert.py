"""
Main module that hosts the Alert and AlertGenerator classes.

The package will use this module to import AlertGenerator and AlertType.

Custom configuration for the alert will be done using AlertGenerator, not by accessing the Alert class implementation.
"""

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
        parent (tk.Tk | tk.Frame | tk.Toplevel): Parent of the Alert widget.
        text (str): Text displayed in the Alert message.
        type (AlertType): Type of the alert (info, warning, error or success)
        anchor (str): Anchor that determines the placement, supports tk anchor constants
        margin (int): Margin of the Alert widget on screen

    Supports all the other Widget.configure() kwargs that a tk.Button has available.
    """

    def __init__(self, parent: tk.Tk | tk.Frame | tk.Toplevel, text: str, type: AlertType, anchor: str, margin: int, **kwargs) -> None:
        self.parent = parent
        self.text = text

        check_parent_type(self.parent, SUPPORTED_PARENT_TYPES)
        super().__init__(self.parent)

        # Configs
        self.design = self._get_design(text, type, **kwargs)
        self.configure(
            **self.design,
            command=self.destroy
        )
        self._placement_kwargs = self._calculate_placement_kwargs(anchor, margin)

        # Callback binding on width change, as width is changing dynamically with the parent,
        # we can only bind <Configure> on the Alert
        self.bind("<Configure>", lambda event: self._update_alert_text(event))

    def _update_alert_text(self, event):
        truncated_text = truncate_text(self, self.parent, self.text, self.design["image"].width())
        self.configure(text=truncated_text)

    def _get_design(self, text: str, type: AlertType, **kwargs) -> dict:
        design = copy.deepcopy(DESIGN_MAP[type])
        
        # Set icon
        icon_path = design["icon_path"]
        design["image"] = tk.PhotoImage(file=icon_path)
        
        design.pop("icon_path")

        # Transform text
        truncated_text = truncate_text(self, self.parent, text, design["image"].width())
        if truncated_text.endswith("..."):
            pass
            # TODO: Put tooltip if text is truncated

        design["text"] = truncated_text

        # Update design with kwargs
        design = {**design, **kwargs}

        return design

    def _calculate_placement_kwargs(self, anchor: str, margin: int) -> dict:
        self.parent.update_idletasks()  # Ensure dimensions are up to date

        # Calculate the relative position based on the anchor
        margin_options = ANCHOR_TO_COORDINATES_OPTION[anchor]
        x = margin_options["x"] * self.parent.winfo_width()
        y = margin_options["y"] * self.parent.winfo_height()

        # Update x with margin
        x = update_x_margin(x, margin, anchor)

        # Update y with margin
        y = update_y_margin(y, margin, anchor)

        placement = {"anchor": anchor, "x": x, "y": y, "relwidth": 0.25}
        return placement

    def place_alert(self) -> None:
        self.place(**self._placement_kwargs)


class AlertGenerator():
    """Driver class for placing alerts on the screen.

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
        # TODO: Don't send if already sent
        self._already_sent = False

    def send(self, text: str, type: AlertType, anchor: str | None = tk.NW, duration: int | None = 2, margin: int | None = 15, **kwargs) -> None:
        """Create the Alert Widget, places it according to the anchor for the specified duration and then destroys it from memory.

        Args:
            text: Text message to be sent
            type: Type of alert, check AlertType enum for possible values
            anchor: (optional) Anchor that determines the placement, supports tk anchor constants. Defaults to tk.NW
            duration (optional): How much time, in seconds, should the Alert be shown to the user. Defaults to 2.
            margin (optional): Margin of the Alert widget. Defaults to 15.

        Supports all the other Widget.configure() kwargs that a tk.Button has available.
        """
        alert = Alert(self._parent, text, type, anchor, margin, **kwargs)

        alert.place_alert()

        # Wait duration and destroy
        alert.after(duration * 1000, alert.destroy)
