"""Configuration module, hosts the AlertConfig class."""

# To make typing compatible with 3.8
from __future__ import annotations

import tkinter as tk

from dataclasses import dataclass, field


@dataclass
class AlertConfig:
    """Default options for the alerts sent by an AlertGenerator.

    Create one, pass it to the AlertGenerator and every .send() call will use it.
    Each option can still be overridden for a single alert by passing it to .send().

     - anchor: Anchor that determines the placement, supports tk anchor constants. Defaults to tk.NW
     - duration: How much time, in seconds, should the Alert be shown to the user. Defaults to 2.
     - margin: Margin of the Alert widget. Defaults to 15.
     - width_percentage: Used to calculate width of the alert in accordance to the width of the parent. Defaults to 0.33
     - button_options: tk.Button options applied to every alert, for example {"font": ("Helvetica", 12)}
    """

    anchor: str = tk.NW
    duration: int | float = 2
    margin: int | float = 15
    width_percentage: float = 0.33
    button_options: dict = field(default_factory=dict)