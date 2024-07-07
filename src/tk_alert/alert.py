import tkinter as tk
import copy

from .constants import AlertType, DESIGN_MAP, ANCHOR_TO_MARGIN_OPTION


class Alert(tk.Button):
    def __init__(self, parent: tk.Widget, text: str, type: AlertType, anchor: str, margin: int, **kwargs) -> None:
        super().__init__(parent)
        self.configure(
            **self._get_design(text, type, **kwargs),
            command=self.destroy
        )

        self._placement_kwargs = self._calculate_placement_kwargs(
            parent, anchor, margin)

    def _get_design(self, text: str, type: AlertType, **kwargs) -> dict:
        design = copy.deepcopy(DESIGN_MAP[type])
        design["text"] = text

        # Update design with kwargs
        design = {**design, **kwargs}

        return design

    def _calculate_placement_kwargs(self, parent: tk.Widget, anchor: str, margin: int) -> dict:
        parent.update_idletasks()  # Ensure dimensions are up to date

        # Calculate the relative position based on the anchor
        margin_options = ANCHOR_TO_MARGIN_OPTION[anchor]
        x = margin_options["x"] * parent.winfo_width()
        y = margin_options["y"] * parent.winfo_height()

        # Update x with margin
        if anchor in ["nw", "w", "sw"]:
            x += margin
        elif anchor in ["ne", "e", "se"]:
            x -= margin
        else:
            pass

        # Update y with margin
        if anchor in ["nw", "n", "ne"]:
            y += margin
        elif anchor in ["sw", "s", "se"]:
            y -= margin
        else:
            pass

        placement = {"anchor": anchor, "x": x, "y": y, "relwidth": 0.25}
        return placement

    def place_alert(self) -> None:
        self.place(**self._placement_kwargs)


class AlertGenerator:
    def __init__(self, parent: tk.Widget) -> None:
        self._parent = parent

    def send(self, text: str, type: AlertType, anchor: str, duration: int | None = 2, margin: int | None = 15, **kwargs) -> None:
        alert = Alert(self._parent, text, type, anchor, margin, **kwargs)
        alert.place_alert()

        # Wait duration and destroy
        alert.after(duration * 1000, alert.destroy)
