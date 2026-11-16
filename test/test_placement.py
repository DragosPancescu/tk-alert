import tkinter as tk
import pytest

from tk_alert import Alert, AlertGenerator, AlertType

MARGIN = 15
WIDTH_PERCENTAGE = 0.33
ANCHORS = [tk.N, tk.NW, tk.NE, tk.CENTER, tk.S, tk.SW, tk.SE, tk.E, tk.W]


@pytest.fixture
def root():
    root = tk.Tk()
    root.geometry("600x400")
    root.update()

    # Tk swallows exceptions raised in callbacks, collect them so tests can assert on them
    root.callback_errors = []
    root.report_callback_exception = lambda exc, val, tb: root.callback_errors.append(val)

    yield root
    root.destroy()


def alerts_of(parent):
    return [child for child in parent.winfo_children() if isinstance(child, Alert)]


def expected_position(alert, parent, anchor):
    """Top-left corner the alert should have for the given anchor."""
    parent_w, parent_h = parent.winfo_width(), parent.winfo_height()
    alert_w, alert_h = alert.winfo_width(), alert.winfo_height()

    if anchor in (tk.NW, tk.W, tk.SW):
        x = MARGIN
    elif anchor in (tk.NE, tk.E, tk.SE):
        x = parent_w - MARGIN - alert_w
    else:
        x = (parent_w - alert_w) / 2

    if anchor in (tk.NW, tk.N, tk.NE):
        y = MARGIN
    elif anchor in (tk.SW, tk.S, tk.SE):
        y = parent_h - MARGIN - alert_h
    else:
        y = (parent_h - alert_h) / 2

    return x, y


@pytest.mark.parametrize("anchor", ANCHORS)
def test_alert_follows_parent_resize(root, anchor):
    AlertGenerator(root).send("Test", AlertType.INFO, anchor, 60, MARGIN, WIDTH_PERCENTAGE)
    alert = alerts_of(root)[0]

    for geometry in ("600x400", "900x500", "320x240"):
        root.geometry(geometry)
        root.update()

        x, y = expected_position(alert, root, anchor)
        # Tk rounds relative coordinates, allow 1px
        assert alert.winfo_x() == pytest.approx(x, abs=1)
        assert alert.winfo_y() == pytest.approx(y, abs=1)
        assert alert.winfo_width() == pytest.approx(root.winfo_width() * WIDTH_PERCENTAGE, abs=1)

    assert root.callback_errors == []


def test_resize_with_many_live_alerts_does_not_recurse(root, monkeypatch):
    """Regression: the <Configure> callback used to call update_idletasks(), re-entering
    itself once per live alert and overflowing the stack on a single resize."""
    depth = 0
    max_depth = 0
    original = Alert._configure_callback

    def tracked(self, event):
        nonlocal depth, max_depth
        depth += 1
        max_depth = max(max_depth, depth)
        try:
            return original(self, event)
        finally:
            depth -= 1

    monkeypatch.setattr(Alert, "_configure_callback", tracked)

    generator = AlertGenerator(root)
    for _ in range(300):
        generator.send("Test alert text", AlertType.INFO, tk.NW, 60, MARGIN, WIDTH_PERCENTAGE)
    root.update()

    root.geometry("900x500")
    root.update()

    assert max_depth == 1
    assert root.callback_errors == []


def test_text_is_refitted_on_resize(root):
    text = "Alert information: Lorem Ipsum Dolor Sit Amet"
    AlertGenerator(root).send(text, AlertType.INFO, tk.NW, 60, MARGIN, WIDTH_PERCENTAGE)
    alert = alerts_of(root)[0]
    root.update()
    assert alert.cget("text") != text  # does not fit in a third of 600px

    root.geometry("1800x400")
    root.update()
    assert alert.cget("text") == text

    root.geometry("600x400")
    root.update()
    assert alert.cget("text").endswith("...")
    assert root.callback_errors == []
