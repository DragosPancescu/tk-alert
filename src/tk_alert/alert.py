import tkinter as tk

from enum import unique, Enum
import copy

@unique
class AlertType(Enum):
    SUCCESS = 1
    INFO = 2
    WARNING = 3
    ERROR = 4


@unique
class AlertPlacement(Enum):
    TOP = 1
    TOP_RIGHT = 2
    RIGHT = 3
    BOTTOM_RIGHT = 4
    BOTTOM = 5
    BOTTOM_LEFT = 6
    LEFT = 7
    TOP_LEFT = 8


COMMON_DESIGN = {
    "foreground": "#f8f8f8",
    "borderwidth" : 0,
    "padx" : 5,
    "pady" : 5,
    "width": 50
}

DESIGN_MAP = {
    AlertType.SUCCESS: {
        "background": "#41cc4f",
        **COMMON_DESIGN
    },
    AlertType.INFO: {
        "background": "#3f96fd",
        **COMMON_DESIGN
    },
    AlertType.WARNING: {
        "background": "",
        **COMMON_DESIGN
    },
    AlertType.ERROR: {
        "background": "#f95959",
        **COMMON_DESIGN
    },
}


class Alert(tk.Button):
    def __init__(self, parent: tk.Widget, text: str, type: AlertType, placement: AlertPlacement) -> None:
        super().__init__(parent)
        self.configure(**self._get_design(text, type))
        
        self._placement_kwargs = self._calculate_placement_kwargs(parent, placement)

    def _get_design(self, text: str, type: AlertType) -> dict:
        design = copy.deepcopy(DESIGN_MAP[type])
        design["text"] = text
        
        return design

    def _calculate_placement_kwargs(self, parent: tk.Widget, placement: AlertPlacement) -> dict:
        pwidth, pheight = parent.winfo_width(), parent.winfo_height()
        
        placement = {
            "x": 15,
            "y": 15
        }
        
        return placement
    
    def place_alert(self) -> None:
        self.place(**self._placement_kwargs)


class AlertGenerator():
    def __init__(self, parent: tk.Widget) -> None:
        self._parent = parent
        
    def send(self, text: str, type: AlertType, placement: AlertPlacement, duration: (int | None) = 2) -> None:
        alert = Alert(self._parent, text, type, placement)
        alert.place_alert()
        
        # Wait duration and destroy
        alert.after(duration * 1000, alert.destroy)
