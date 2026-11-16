"""
Contains:
 - Alert widget.
 - AlertGenerator class used for creating Alert widgets on demand.
 - AlertType that dictates the style.
"""

from .alert import Alert, AlertGenerator, AlertType
from .config import AlertConfig

__all__ = ["Alert", "AlertConfig", "AlertGenerator", "AlertType"]
