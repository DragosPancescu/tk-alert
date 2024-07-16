from ..src import AlertType, AlertGenerator

import tkinter as tk
import pytest


@pytest.fixture(scope="module")
def root():
    root = tk.Tk()
    yield root
    root.destroy()


def generate_params():
    pass

@pytest.mark.parametrize("text,width,height", [
    ("Button 1", 10, 2),
    ("Button 2", 15, 3),
    ("Button 3", 20, 4),
])
def test_grid_search_parameters():