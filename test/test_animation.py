import tkinter as tk
import pytest

from tk_alert import Alert, AlertConfig, AlertGenerator, AlertType
from tk_alert.constants import STACK_SPACING

MARGIN = 15
SETTLE_MS = 800  # Comfortably longer than any slide in these tests


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


def alerts_of(root):
    return [child for child in root.winfo_children() if isinstance(child, Alert)]


def send(generator, text="Test", anchor=tk.NW, duration=60, **kwargs):
    generator.send(text, AlertType.INFO, anchor, duration, MARGIN, 0.33, **kwargs)
    generator.parent.update_idletasks()
    return alerts_of(generator.parent)[-1]


def run(root, milliseconds=SETTLE_MS):
    """Lets the event loop run, so the animation timers fire."""
    root.after(milliseconds, root.quit)
    root.mainloop()


def test_alerts_are_not_animated_by_default(root):
    alert = send(AlertGenerator(root))

    assert (alert.winfo_x(), alert.winfo_y()) == (MARGIN, MARGIN)

    alert.invoke()
    assert alerts_of(root) == []


def test_left_anchored_alert_slides_in_from_the_left(root):
    alert = send(AlertGenerator(root), animate=True)
    assert alert.winfo_x() < MARGIN

    run(root)
    assert (alert.winfo_x(), alert.winfo_y()) == (MARGIN, MARGIN)
    assert root.callback_errors == []


def test_right_anchored_alert_slides_in_from_the_right(root):
    alert = send(AlertGenerator(root), anchor=tk.NE, animate=True)
    assert alert.winfo_x() + alert.winfo_width() > root.winfo_width() - MARGIN

    run(root)
    assert alert.winfo_x() + alert.winfo_width() == root.winfo_width() - MARGIN


@pytest.mark.parametrize("anchor", [tk.N, tk.S])
def test_middle_column_alert_slides_in_vertically(root, anchor):
    alert = send(AlertGenerator(root), anchor=anchor, animate=True)
    start_x, start_y = alert.winfo_x(), alert.winfo_y()

    run(root)
    assert alert.winfo_x() == start_x
    assert alert.winfo_y() != start_y

    if anchor == tk.N:
        assert alert.winfo_y() == MARGIN
    else:
        assert alert.winfo_y() + alert.winfo_height() == root.winfo_height() - MARGIN


def test_center_alert_appears_in_place(root):
    alert = send(AlertGenerator(root), anchor=tk.CENTER, animate=True)
    start = (alert.winfo_x(), alert.winfo_y())

    run(root, 200)
    assert (alert.winfo_x(), alert.winfo_y()) == start


def test_clicked_alert_slides_out_before_it_is_destroyed(root):
    alert = send(AlertGenerator(root), animate=True)
    run(root)

    alert.invoke()
    root.update_idletasks()
    assert alert.winfo_exists()
    assert alert.winfo_x() < MARGIN

    run(root)
    assert alerts_of(root) == []
    assert root.callback_errors == []


def test_expired_alert_slides_out(root):
    send(AlertGenerator(root), duration=0.1, animate=True)

    run(root)
    assert alerts_of(root) == []
    assert root.callback_errors == []


def test_remaining_alerts_glide_to_close_the_gap(root):
    generator = AlertGenerator(root)
    first, second, third = (send(generator, text, animate=True) for text in ("first", "second", "third"))
    run(root)
    second_y = second.winfo_y()

    first.invoke()
    run(root)
    assert alerts_of(root) == [second, third]
    assert second.winfo_y() == MARGIN < second_y
    assert third.winfo_y() == second.winfo_y() + second.winfo_height() + STACK_SPACING
    assert root.callback_errors == []


def test_alert_that_is_sliding_out_is_not_pulled_back_by_a_new_alert(root):
    generator = AlertGenerator(root)
    first = send(generator, "first", animate=True)
    run(root)

    first.invoke()
    second = send(generator, "second", animate=True)

    run(root)
    assert alerts_of(root) == [second]
    assert second.winfo_y() == MARGIN


def test_destroying_an_alert_in_the_middle_of_a_slide_is_safe(root):
    alert = send(AlertGenerator(root), animate=True)

    alert.destroy()
    run(root, 200)
    assert root.callback_errors == []


def test_animation_can_be_enabled_in_the_config_and_overridden(root):
    generator = AlertGenerator(root, AlertConfig(animate=True))

    animated = send(generator)
    assert animated.winfo_x() < MARGIN

    still = send(generator, anchor=tk.NE, animate=False)
    assert still.winfo_x() + still.winfo_width() == root.winfo_width() - MARGIN