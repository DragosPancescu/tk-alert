from itertools import product

import tkinter as tk
import pytest

from src import AlertType, AlertGenerator


@pytest.fixture(scope="module")
def root_tk():
    root = tk.Tk()
    yield root
    root.destroy()


@pytest.fixture(scope="module")
def root_frame():
    root = tk.Frame()
    yield root
    root.destroy()


@pytest.fixture(scope="module")
def root_toplevel():
    root = tk.Toplevel()
    yield root
    root.destroy()


def generate_params():
    text = ["Test"]
    types = [AlertType.INFO, AlertType.SUCCESS, AlertType.WARNING, AlertType.ERROR]
    anchors = [tk.N, tk.NW, tk.NE, tk.CENTER, tk.S, tk.SW, tk.SE, tk.E, tk.W]
    durations = [0, 1, -1]
    margins = [0, 1, -1]
    width_percentages = [0, 0.33, 1, -1]

    grid = [text, types, anchors, durations, margins, width_percentages]

    return [item for item in product(*grid)]


@pytest.mark.parametrize(
    "text,type,anchor,duration,margin,width_percentage", generate_params()
)
def test_grid_search_parameters(
    root_tk, text, type, anchor, duration, margin, width_percentage
):
    alert_generator = AlertGenerator(root_tk)
    alert_generator.send(text, type, anchor, duration, margin, width_percentage)

    # Cleanup
    del alert_generator
