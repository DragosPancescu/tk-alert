"""Constants module used in alert and alert_utils."""

import tkinter as tk

from enum import unique, Enum


@unique
class AlertType(Enum):
    """Type of the alert that dictates the default appearence of the GUI.

    SUCCESS, INFO, WARNING, ERROR are the possible types.
    """
    
    SUCCESS = 1
    """Success alert type, use this for green colored alerts.
    """
    INFO = 2
    """Information alert type, use this for blue colored alerts.
    """
    WARNING = 3
    """Warning alert type, use this for yellow colored alerts.
    """
    ERROR = 4
    """Error alert type, use this for red colored alerts.
    """


COMMON_DESIGN = {
    "foreground": "#0d0907",
    "activeforeground": "#0d0907",
    "borderwidth": 0,
    "padx": 5,
    "pady": 5,
    "relief": "sunken",
    "cursor": "hand2",
    "anchor": "w"
}

DESIGN_MAP = {
    AlertType.SUCCESS: {"background": "#4bb543", "activebackground": "#41cc4f", **COMMON_DESIGN},
    AlertType.INFO: {"background": "#3f96fd", "activebackground": "#3f96fd", **COMMON_DESIGN},
    AlertType.WARNING: {"background": "#e9d543", "activebackground": "#eed202", **COMMON_DESIGN},
    AlertType.ERROR: {"background": "#f95959", "activebackground": "#f95959", **COMMON_DESIGN},
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
