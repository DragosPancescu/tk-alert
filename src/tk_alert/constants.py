"""Constants module used in alert and alert_utils."""

import os
import tkinter as tk

from enum import unique, auto, Enum


@unique
class AlertType(Enum):
    """Type of the alert that dictates the default appearence of the GUI.

    SUCCESS, INFO, WARNING, ERROR are the possible types.
    """

    SUCCESS = auto()
    """Success alert type, use this for green colored alerts.
    """
    INFO = auto()
    """Information alert type, use this for blue colored alerts.
    """
    WARNING = auto()
    """Warning alert type, use this for yellow colored alerts.
    """
    ERROR = auto()
    """Error alert type, use this for red colored alerts.
    """


COMMON_DESIGN = {
    "foreground": "#0E0E0C",
    "activeforeground": "#0E0E0C",
    "borderwidth": 0,
    "padx": 7.5,
    "pady": 7.5,
    "relief": tk.SUNKEN,
    "cursor": "hand2",
    "anchor": tk.W,
    "compound": tk.LEFT,
}

DESIGN_MAP = {
    AlertType.SUCCESS: {
        "background": "#58B866",
        "activebackground": "#58B866",
        "icon_path": os.path.join(os.path.dirname(__file__), "icons", "success-icon.png"),
        **COMMON_DESIGN,
    },
    AlertType.INFO: {
        "background": "#5FA5F7",
        "activebackground": "#5FA5F7",
        "icon_path": os.path.join(os.path.dirname(__file__), "icons", "information-icon.png"),
        **COMMON_DESIGN,
    },
    AlertType.WARNING: {
        "background": "#EAD644",
        "activebackground": "#EAD644",
        "icon_path": os.path.join(os.path.dirname(__file__), "icons", "warning-icon.png"),
        **COMMON_DESIGN,
    },
    AlertType.ERROR: {
        "background": "#FF7373",
        "activebackground": "#FF7373",
        "icon_path": os.path.join(os.path.dirname(__file__), "icons", "error-icon.png"),
        **COMMON_DESIGN,
    },
}

ANCHOR_TO_COORDINATES_OPTION = {
    "nw": {"x": 0, "y": 0},
    "n": {"x": 0.5, "y": 0},
    "ne": {"x": 1, "y": 0},
    "w": {"x": 0, "y": 0.5},
    "center": {"x": 0.5, "y": 0.5},
    "e": {"x": 1, "y": 0.5},
    "sw": {"x": 0, "y": 1},
    "s": {"x": 0.5, "y": 1},
    "se": {"x": 1, "y": 1},
}

SUPPORTED_PARENT_TYPES = (tk.Tk, tk.Frame, tk.Toplevel)
