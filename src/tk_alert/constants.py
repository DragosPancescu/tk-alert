from enum import unique, Enum


@unique
class AlertType(Enum):
    SUCCESS = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


COMMON_DESIGN = {
    "foreground": "#f8f8f8",
    "activeforeground": "#f8f8f8",
    "borderwidth": 0,
    "padx": 5,
    "pady": 5,
    "relief": "sunken",
    "cursor": "hand2"
}

DESIGN_MAP = {
    AlertType.SUCCESS: {"background": "#41cc4f", "activebackground": "#41cc4f", **COMMON_DESIGN},
    AlertType.INFO: {"background": "#3f96fd", "activebackground": "#3f96fd", **COMMON_DESIGN},
    AlertType.WARNING: {"background": "#eed202", "activebackground": "#eed202", **COMMON_DESIGN},
    AlertType.ERROR: {"background": "#f95959", "activebackground": "#f95959", **COMMON_DESIGN},
}


ANCHOR_TO_MARGIN_OPTION = {
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
