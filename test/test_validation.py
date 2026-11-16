import tkinter as tk
import pytest

from tk_alert import Alert, AlertGenerator, AlertType


@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()


def test_alert_rejects_unsupported_parent_with_clear_message(root):
    """Regression: the `type` argument shadowed the builtin, so building the error
    message itself failed with "'AlertType' object is not callable"."""
    label = tk.Label(root)

    with pytest.raises(TypeError, match=r"Unsupported parent type: <class 'tkinter\.Label'>"):
        Alert(label, "Test", AlertType.INFO, tk.NW, 15, 0.33)

    assert label.winfo_children() == []


def test_generator_rejects_unsupported_parent_with_clear_message(root):
    with pytest.raises(TypeError, match=r"Unsupported parent type: <class 'tkinter\.Label'>"):
        AlertGenerator(tk.Label(root))


@pytest.mark.parametrize(
    "kwargs,error,message",
    [
        ({"duration": None}, TypeError, "not supported between"),
        ({"duration": "2"}, TypeError, "not supported between"),
        ({"duration": -1}, ValueError, "Negative duration value"),
        ({"margin": None}, TypeError, "not supported between"),
        ({"margin": -1}, ValueError, "Negative margin value"),
        ({"width_percentage": None}, TypeError, "not supported between"),
        ({"width_percentage": 0}, ValueError, "Out of bounds width_percentage value"),
        ({"width_percentage": -0.5}, ValueError, "Out of bounds width_percentage value"),
        ({"width_percentage": 1.01}, ValueError, "Out of bounds width_percentage value"),
        ({"anchor": "bogus"}, ValueError, "Unsupported anchor: 'bogus'"),
        ({"anchor": None}, ValueError, "Unsupported anchor: None"),
        ({"type": "info"}, TypeError, "Unsupported alert type: 'info'"),
        ({"type": None}, TypeError, "Unsupported alert type: None"),
    ],
)
def test_send_rejects_invalid_arguments_without_leaving_a_widget(root, kwargs, error, message):
    """Regression: these either crashed with an unrelated error or were silently accepted,
    and some left an alert on screen that never went away."""
    arguments = {"text": "Test", "type": AlertType.INFO, **kwargs}

    with pytest.raises(error, match=message):
        AlertGenerator(root).send(**arguments)

    assert root.winfo_children() == []


@pytest.mark.parametrize(
    "kwargs",
    [
        {"duration": 0.5},
        {"margin": 0},
        {"margin": 7.5},
        {"width_percentage": 1},
    ],
)
def test_send_accepts_boundary_values(root, kwargs):
    AlertGenerator(root).send("Test", AlertType.INFO, **kwargs)
    root.update()

    assert len(root.winfo_children()) == 1


def test_zero_duration_is_accepted_and_removes_the_alert_immediately(root):
    AlertGenerator(root).send("Test", AlertType.INFO, duration=0)
    root.update()

    assert root.winfo_children() == []


def test_float_duration_destroys_the_alert_on_time(root):
    """Regression: a float duration reached Tk as "500.0" milliseconds and raised TclError."""
    AlertGenerator(root).send("Test", AlertType.INFO, duration=0.2)
    root.update()
    assert len(root.winfo_children()) == 1

    root.after(600, root.quit)
    root.mainloop()
    assert root.winfo_children() == []
