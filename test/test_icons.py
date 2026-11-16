import pathlib
import tkinter as tk
import pytest

from tk_alert import Alert, AlertConfig, AlertGenerator, AlertType
from tk_alert.constants import DESIGN_MAP

INFO_ICON = DESIGN_MAP[AlertType.INFO]["icon_path"]
ERROR_ICON = DESIGN_MAP[AlertType.ERROR]["icon_path"]
WARNING_ICON = DESIGN_MAP[AlertType.WARNING]["icon_path"]


@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()


def send(generator, type=AlertType.INFO, **kwargs):
    generator.send("Test", type, **kwargs)
    return [child for child in generator.parent.winfo_children() if isinstance(child, Alert)][-1]


def icon_file(alert):
    return alert.design["image"].cget("file")


def test_default_icon_of_the_type_is_used(root):
    generator = AlertGenerator(root)

    assert icon_file(send(generator, AlertType.INFO)) == INFO_ICON
    assert icon_file(send(generator, AlertType.ERROR)) == ERROR_ICON


@pytest.mark.parametrize("icon", [ERROR_ICON, pathlib.Path(ERROR_ICON)])
def test_icon_can_be_a_file_path(root, icon):
    alert = send(AlertGenerator(root), icon=icon)

    assert icon_file(alert) == ERROR_ICON
    assert alert.cget("image") == str(alert.design["image"])


def test_icon_can_be_a_ready_photo_image(root):
    photo = tk.PhotoImage(file=ERROR_ICON)
    alert = send(AlertGenerator(root), icon=photo)

    assert alert.cget("image") == str(photo)


def test_icon_false_shows_no_icon(root):
    alert = send(AlertGenerator(root), icon=False)

    assert alert.cget("image") == ""


def test_config_replaces_the_icon_of_a_type_only(root):
    generator = AlertGenerator(root, AlertConfig(icons={AlertType.INFO: ERROR_ICON}))

    assert icon_file(send(generator, AlertType.INFO)) == ERROR_ICON
    assert icon_file(send(generator, AlertType.WARNING)) == WARNING_ICON


def test_send_icon_overrides_the_config(root):
    generator = AlertGenerator(root, AlertConfig(icons={AlertType.INFO: ERROR_ICON}))

    assert icon_file(send(generator, icon=WARNING_ICON)) == WARNING_ICON
    assert send(generator, icon=False).cget("image") == ""


def test_config_can_remove_the_icon_of_a_type(root):
    generator = AlertGenerator(root, AlertConfig(icons={AlertType.INFO: False}))

    assert send(generator).cget("image") == ""


def test_icon_that_cannot_be_loaded_raises_and_leaves_no_widget(root):
    with pytest.raises(tk.TclError):
        AlertGenerator(root).send("Test", AlertType.INFO, icon="does-not-exist.png")

    assert root.winfo_children() == []


def test_unknown_button_option_raises_and_leaves_no_widget(root):
    with pytest.raises(tk.TclError):
        AlertGenerator(root).send("Test", AlertType.INFO, not_an_option=1)

    assert root.winfo_children() == []