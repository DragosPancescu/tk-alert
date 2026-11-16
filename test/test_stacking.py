import tkinter as tk
import pytest

from tk_alert import Alert, AlertGenerator, AlertType
from tk_alert.constants import STACK_SPACING

MARGIN = 15


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


def send(generator, text, anchor):
    generator.send(text, AlertType.INFO, anchor, 60, MARGIN, 0.33)
    return [child for child in generator.parent.winfo_children() if isinstance(child, Alert)][-1]


@pytest.mark.parametrize("anchor", [tk.NW, tk.N, tk.NE, tk.W, tk.CENTER, tk.E])
def test_alerts_on_the_same_anchor_stack_downwards(root, anchor):
    """Regression: alerts sent to the same anchor were placed on the same coordinates."""
    generator = AlertGenerator(root)
    first, second, third = (send(generator, text, anchor) for text in ("first", "second", "third"))
    root.update()

    assert second.winfo_y() == first.winfo_y() + first.winfo_height() + STACK_SPACING
    assert third.winfo_y() == second.winfo_y() + second.winfo_height() + STACK_SPACING
    assert first.winfo_x() == second.winfo_x() == third.winfo_x()


@pytest.mark.parametrize("anchor", [tk.SW, tk.S, tk.SE])
def test_alerts_on_a_bottom_anchor_stack_upwards(root, anchor):
    generator = AlertGenerator(root)
    first, second = send(generator, "first", anchor), send(generator, "second", anchor)
    root.update()

    assert first.winfo_y() + first.winfo_height() == root.winfo_height() - MARGIN
    assert second.winfo_y() + second.winfo_height() == first.winfo_y() - STACK_SPACING


def test_alerts_on_different_anchors_do_not_affect_each_other(root):
    generator = AlertGenerator(root)
    top_left, top_right = send(generator, "left", tk.NW), send(generator, "right", tk.NE)
    root.update()

    assert top_left.winfo_y() == top_right.winfo_y() == MARGIN


def test_remaining_alerts_close_the_gap_when_one_is_dismissed(root):
    generator = AlertGenerator(root)
    first, second, third = (send(generator, text, tk.NW) for text in ("first", "second", "third"))
    root.update()

    second.invoke()  # The user clicks the alert in the middle
    root.update()

    assert first.winfo_y() == MARGIN
    assert third.winfo_y() == first.winfo_y() + first.winfo_height() + STACK_SPACING
    assert root.callback_errors == []


def test_next_alert_takes_the_first_spot_after_all_alerts_are_gone(root):
    generator = AlertGenerator(root)
    for alert in [send(generator, "first", tk.NW), send(generator, "second", tk.NW)]:
        alert.destroy()
    root.update()

    alert = send(generator, "third", tk.NW)
    root.update()

    assert alert.winfo_y() == MARGIN
    assert root.callback_errors == []


def test_stacked_alerts_keep_their_spacing_when_the_window_is_resized(root):
    generator = AlertGenerator(root)
    first, second = send(generator, "first", tk.SE), send(generator, "second", tk.SE)

    root.geometry("900x500")
    root.update()

    assert first.winfo_y() + first.winfo_height() == root.winfo_height() - MARGIN
    assert second.winfo_y() + second.winfo_height() == first.winfo_y() - STACK_SPACING
    assert root.callback_errors == []