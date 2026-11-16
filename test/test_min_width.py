import tkinter as tk
import pytest

from tkinter import font

from tk_alert import Alert, AlertConfig, AlertGenerator, AlertType

TEXT = "Alert information: Lorem Ipsum Dolor Sit Amet"
MARGIN = 15
WIDTH_PERCENTAGE = 0.33


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


def send(generator, text="Test", **kwargs):
    kwargs = {"anchor": tk.NW, "duration": 60, "margin": MARGIN, "width_percentage": WIDTH_PERCENTAGE, **kwargs}
    generator.send(text, AlertType.INFO, **kwargs)
    generator.parent.update()
    return [child for child in generator.parent.winfo_children() if isinstance(child, Alert)][-1]


def resize(root, geometry):
    root.geometry(geometry)
    root.update()
    root.update()  # The width correction is applied on the event after the resize


def test_without_min_width_the_alert_only_follows_the_parent(root):
    alert = send(AlertGenerator(root))
    resize(root, "300x400")

    assert alert.winfo_width() == pytest.approx(300 * WIDTH_PERCENTAGE, abs=1)


def test_alert_is_not_narrower_than_min_width(root):
    # A third of 600px is 198px, less than the minimum
    alert = send(AlertGenerator(root), min_width=250)
    root.update()

    assert alert.winfo_width() == 250
    assert root.callback_errors == []


def test_min_width_has_no_effect_when_the_alert_is_already_wider(root):
    alert = send(AlertGenerator(root), min_width=100)

    assert alert.winfo_width() == pytest.approx(600 * WIDTH_PERCENTAGE, abs=1)


@pytest.mark.parametrize("anchor", [tk.NW, tk.N, tk.NE, tk.SE])
def test_alert_width_follows_the_parent_across_the_minimum(root, anchor):
    alert = send(AlertGenerator(root), anchor=anchor, min_width=250)

    for geometry, expected in [("300x400", 250), ("1200x400", 396), ("450x400", 250), ("900x400", 297)]:
        resize(root, geometry)
        assert alert.winfo_width() == pytest.approx(expected, abs=1), geometry

    assert root.callback_errors == []


def test_right_anchored_alert_keeps_its_margin_at_min_width(root):
    alert = send(AlertGenerator(root), anchor=tk.NE, min_width=250)
    resize(root, "400x400")

    assert alert.winfo_width() == 250
    assert alert.winfo_x() + alert.winfo_width() == root.winfo_width() - MARGIN


def test_text_is_fitted_to_min_width_not_to_the_relative_width(root):
    narrow = send(AlertGenerator(root), TEXT)
    wide = send(AlertGenerator(root), TEXT, min_width=400)
    root.update()

    assert narrow.cget("text").endswith("...")
    assert wide.cget("text") == TEXT


def test_min_width_can_come_from_the_config(root):
    generator = AlertGenerator(root, AlertConfig(min_width=250))

    assert send(generator).winfo_width() == 250
    assert send(generator, min_width=300).winfo_width() == 300


def test_negative_min_width_is_rejected(root):
    with pytest.raises(ValueError, match="Negative min_width value: -1"):
        AlertGenerator(root).send("Test", AlertType.INFO, min_width=-1)

    assert root.winfo_children() == []