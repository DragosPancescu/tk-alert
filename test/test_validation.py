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
