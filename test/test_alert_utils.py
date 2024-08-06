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
def root_frame(root_tk):
    frame = tk.Frame(root_tk)
    frame.pack()
    yield frame
    frame.destroy()


@pytest.fixture(scope="module")
def root_toplevel(root_tk):
    toplevel = tk.Toplevel(root_tk)
    yield toplevel
    toplevel.destroy()


def generate_params():
    root_fixture = ["root_tk", "root_frame", "root_toplevel"]
    text = ["Test"]
    types = [AlertType.INFO, AlertType.SUCCESS, AlertType.WARNING, AlertType.ERROR]
    anchors = [tk.N, tk.NW, tk.NE, tk.CENTER, tk.S, tk.SW, tk.SE, tk.E, tk.W]
    durations = [1, 2]
    margins = [1, 2]
    width_percentages = [0.33, 1]

    grid = [root_fixture, text, types, anchors, durations, margins, width_percentages]

    return [item for item in product(*grid)]


@pytest.mark.parametrize(
    "root_fixture,text,type,anchor,duration,margin,width_percentage", generate_params()
)
def test_gridsearch_happy_path(
    root_fixture, text, type, anchor, duration, margin, width_percentage, request
):
    try:
        root = request.getfixturevalue(root_fixture)
        alert_generator = AlertGenerator(root)
        alert_generator.send(text, type, anchor, duration, margin, width_percentage)

        # Ensure the alert generator works as expected
        assert alert_generator is not None

    except tk.TclError as e:
        pytest.fail(f"TclError occurred: {e}")

    finally:
        # Cleanup
        if "alert_generator" in locals():
            del alert_generator


# If running the test outside of a script, ensure Tkinter mainloop is running
if __name__ == "__main__":
    pytest.main()
