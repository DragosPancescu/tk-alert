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
    SUPPORTED_PARENT_TYPES,
    STACK_SPACING
)

from .config import AlertConfig

from .alert_utils import (
    check_parent_type,
    truncate_text,
    update_x_margin,
    update_y_margin
)


class Alert(tk.Button):
    """Alert widget, derived from tk.Button.

    Takes as init arguments the following: 
     - parent (tk.Misc): Parent of the Alert widget, one of the containers in SUPPORTED_PARENT_TYPES.
     - text (str): Text displayed in the Alert message.
     - type (AlertType): Type of the alert (info, warning, error or success)
     - anchor (str): Anchor that determines the placement, supports tk anchor constants
     - margin (int): Margin of the Alert widget on screen
     - width_percentage (flaot): Used to calculate width of the alert in accordance to the width of the parent
     - min_width (int): Width in pixels the Alert never gets smaller than, 0 means no minimum

    Supports all the other Widget.configure() kwargs that a tk.Button has available.
    """

    def __init__(self, parent: tk.Misc, text: str, type: AlertType, anchor: str, margin: int, width_percentage: float, min_width: int = 0, **kwargs) -> None:
        # Enforce parent type before init
        if not check_parent_type(parent, SUPPORTED_PARENT_TYPES):
            raise TypeError(
                f"Unsupported parent type: {parent.__class__}, supported (derived from) types are: {SUPPORTED_PARENT_TYPES}"
            )

        # Validate the rest before the widget is created, so a bad argument never leaves an orphan widget behind
        if not isinstance(type, AlertType):
            raise TypeError(f"Unsupported alert type: {type!r}, supported types are the members of AlertType.")

        if not isinstance(anchor, str) or anchor not in ANCHOR_TO_COORDINATES_OPTION:
            raise ValueError(f"Unsupported anchor: {anchor!r}, supported anchors are: {list(ANCHOR_TO_COORDINATES_OPTION)}")

        if margin < 0:
            raise ValueError(f"Negative margin value: {margin}, allowed values are greater or equal than 0.")

        if width_percentage <= 0 or width_percentage > 1:
            raise ValueError(f"Out of bounds width_percentage value: {width_percentage}, allowed values are between 0 (exclusive) and 1 (inclusive)")

        if min_width < 0:
            raise ValueError(f"Negative min_width value: {min_width}, allowed values are greater or equal than 0.")

        super().__init__(parent)

        # Properties
        self._parent = parent
        self._text = text
        self._width_percentage = width_percentage
        self._min_width = min_width
        self._extra_width = 0
        self._anchor = anchor
        self._margin = margin
        
        # Set default command if command method is not provided
        if not kwargs.get("command", None):
            kwargs["command"] = self.destroy
            
        # Configs
        self.design = self._get_design(type, **kwargs)
        self.configure(**self.design)
        self._placement_kwargs = self._calculate_placement_kwargs()

        # Placement follows the parent natively (relative coordinates), so the only things
        # left to do when the Alert is resized are to enforce min_width and re-fit the text
        self.bind("<Configure>", self._configure_callback)

    @property
    def text(self):
        return self._text

    @property
    def width_percentage(self):
        return self._width_percentage

    @property
    def min_width(self):
        return self._min_width

    ##### <Configure> bind callback logic #####

    def _configure_callback(self, event):
        self.__update_alert_width()
        self.__update_alert_text()

    def __update_alert_width(self):
        # Tk's place adds `width` to the relative width, so the Alert keeps following
        # the parent and only gets the pixels it is missing to reach min_width
        relative_width = self.winfo_width() - self._extra_width
        extra_width = max(0, self._min_width - relative_width)
        if extra_width != self._extra_width:
            self._extra_width = extra_width
            self.place_configure(width=extra_width)

    def __update_alert_text(self):
        truncated_text = truncate_text(self, self._parent)
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
        truncated_text = truncate_text(self, self._parent)
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

    def place_alert(self, stack_offset: int = 0) -> None:
        """Places the Alert, stack_offset moves it that many pixels away from its anchor edge.

        Bottom anchors stack upwards, all the others stack downwards.
        """
        placement = dict(self._placement_kwargs)
        direction = -1 if self._anchor in ["sw", "s", "se"] else 1
        placement["y"] += direction * stack_offset

        self.place(**placement)
        self.lift()


class AlertGenerator():
    """Driver class for placing alerts on the screen.

    Takes as init arguments the parent of the alert, where the Alert widget will sit when placed,
    and optionally an AlertConfig with the default options for the alerts it sends.
    Restricted to container widgets: windows, frames, label frames, canvases, paned windows and notebooks (see SUPPORTED_PARENT_TYPES)

    .send() is the functionality that sends alerts to the parent Widget.

    Ideally the main app class should initialize an AlertGenerator object internally and use the .send() function whenever a notification needs to be sent to the user.

    As after each .send() call the Alert widget gets destroyed it should not impact the memory to have the object as a class attribute.
    """

    def __init__(self, parent: tk.Misc, config: AlertConfig | None = None) -> None:
        # Enforce parent type before init
        if not check_parent_type(parent, SUPPORTED_PARENT_TYPES):
            raise TypeError(
                f"Unsupported parent type: {type(parent)}, supported (derived from) types are: {SUPPORTED_PARENT_TYPES}"
            )

        self._parent = parent
        self._config = config if config is not None else AlertConfig()
        self._alerts = []  # Alerts currently on screen, oldest first

    @property
    def parent(self):
        return self._parent

    @property
    def config(self):
        return self._config

    def _restack(self) -> None:
        """Places the alerts on screen so the ones sharing an anchor sit next to each other instead of overlapping."""
        used_height = {}  # Pixels already taken by alerts, per anchor
        for alert in self._alerts:
            offset = used_height.get(alert._anchor, 0)
            alert.place_alert(offset)
            used_height[alert._anchor] = offset + alert.winfo_reqheight() + STACK_SPACING

    def _on_alert_destroyed(self, alert: Alert) -> None:
        """Forgets the alert and moves the remaining ones to close the gap it left."""
        if alert in self._alerts:
            self._alerts.remove(alert)
            self._restack()

    def send(self, text: str, type: AlertType, anchor: str | None = None, duration: int | float | None = None, margin: int | float | None = None, width_percentage: float | None = None, min_width: int | None = None, **kwargs) -> None:
        """Create the Alert Widget, places it according to the anchor for the specified duration and then destroys it from memory.

        Args:
         - text: Text message to be sent
         - type: Type of alert, check AlertType enum for possible values
         - anchor: (optional) Anchor that determines the placement, supports tk anchor constants.
         - duration (optional): How much time, in seconds, should the Alert be shown to the user.
         - margin (optional): Margin of the Alert widget.
         - width_percentage (optional): Used to calculate width of the alert in accordance to the width of the parent.
         - min_width (optional): Width in pixels the Alert never gets smaller than.

        The optional arguments that are not passed (or passed as None) take their value from the AlertConfig of the generator.

        Supports all the other Widget.configure() kwargs that a tk.Button has available.
        """

        # Anything not passed for this alert comes from the config
        anchor = self._config.anchor if anchor is None else anchor
        duration = self._config.duration if duration is None else duration
        margin = self._config.margin if margin is None else margin
        width_percentage = self._config.width_percentage if width_percentage is None else width_percentage
        min_width = self._config.min_width if min_width is None else min_width
        kwargs = {**self._config.button_options, **kwargs}

        # Checks, the Alert widget validates the rest of the arguments itself
        if duration < 0:
            raise ValueError(f"Negative duration value: {duration}, allowed values are greater or equal than 0.")

        # Create Alert Widget
        alert = Alert(self._parent, text, type, anchor, margin, width_percentage, min_width, **kwargs)

        # Place it after the alerts already shown on its anchor, and close the gap when it goes away
        self._alerts.append(alert)
        alert.bind("<Destroy>", lambda event: self._on_alert_destroyed(alert), add="+")
        self._restack()

        # Wait duration and destroy, Tk only accepts whole milliseconds
        alert.after(int(duration * 1000), alert.destroy)
