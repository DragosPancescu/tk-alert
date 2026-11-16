import tkinter as tk
import pytest

from tk_alert import Alert, AlertConfig, AlertGenerator, AlertType


@pytest.fixture
def root():
    root = tk.Tk()
    root.geometry("600x400")
    root.update()
    yield root
    root.destroy()


def send(generator, **kwargs):
    generator.send("Test", AlertType.INFO, **kwargs)
    generator.parent.update()
    return [child for child in generator.parent.winfo_children() if isinstance(child, Alert)][-1]


def test_generator_without_config_uses_the_library_defaults(root):
    generator = AlertGenerator(root)
    alert = send(generator)

    assert generator.config == AlertConfig()
    assert (alert.winfo_x(), alert.winfo_y()) == (15, 15)
    assert alert.winfo_width() == pytest.approx(root.winfo_width() * 0.33, abs=1)


def test_config_sets_the_defaults_for_every_alert(root):
    config = AlertConfig(anchor=tk.SE, duration=60, margin=20, width_percentage=0.5)
    alert = send(AlertGenerator(root, config))

    assert alert.winfo_width() == pytest.approx(root.winfo_width() * 0.5, abs=1)
    assert alert.winfo_x() + alert.winfo_width() == root.winfo_width() - 20
    assert alert.winfo_y() + alert.winfo_height() == root.winfo_height() - 20


def test_send_arguments_override_the_config_for_one_alert(root):
    generator = AlertGenerator(root, AlertConfig(anchor=tk.SE, margin=20, width_percentage=0.5))
    overridden = send(generator, anchor=tk.NW, margin=5, width_percentage=0.25)

    assert (overridden.winfo_x(), overridden.winfo_y()) == (5, 5)
    assert overridden.winfo_width() == pytest.approx(root.winfo_width() * 0.25, abs=1)

    # The next alert goes back to the config
    following = send(generator)
    assert following.winfo_y() + following.winfo_height() == root.winfo_height() - 20


def test_config_duration_is_used_and_can_be_overridden(root):
    generator = AlertGenerator(root, AlertConfig(duration=0.2))
    send(generator)
    send(generator, duration=60)

    root.after(600, root.quit)
    root.mainloop()

    # Only the alert with the overridden duration is still there
    assert len(root.winfo_children()) == 1


def test_button_options_are_applied_and_can_be_overridden(root):
    generator = AlertGenerator(root, AlertConfig(button_options={"background": "#222222", "foreground": "#FFFFFF"}))

    alert = send(generator)
    assert (alert.cget("background"), alert.cget("foreground")) == ("#222222", "#FFFFFF")

    alert = send(generator, background="#000000")
    assert (alert.cget("background"), alert.cget("foreground")) == ("#000000", "#FFFFFF")


def test_invalid_config_value_is_reported_when_sending(root):
    generator = AlertGenerator(root, AlertConfig(anchor="bogus"))

    with pytest.raises(ValueError, match="Unsupported anchor: 'bogus'"):
        generator.send("Test", AlertType.INFO)

    assert root.winfo_children() == []


def test_one_config_can_be_shared_between_generators(root):
    config = AlertConfig(anchor=tk.SW, margin=10)
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)
    root.update()

    for parent in (root, frame):
        alert = send(AlertGenerator(parent, config))
        assert alert.winfo_x() == 10