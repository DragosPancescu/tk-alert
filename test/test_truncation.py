import tkinter as tk
import pytest

from tkinter import font

from tk_alert import Alert, AlertGenerator, AlertType

TEXT = "Alert information: Lorem Ipsum Dolor Sit Amet consectetur adipiscing"


@pytest.fixture
def root():
    root = tk.Tk()
    root.geometry("600x400")
    root.update()
    yield root
    root.destroy()


def send(root, text, width_percentage=0.33):
    AlertGenerator(root).send(text, AlertType.INFO, tk.NW, 60, 15, width_percentage)
    root.update()
    return [child for child in root.winfo_children() if isinstance(child, Alert)][-1]


@pytest.mark.parametrize("geometry", ["300x400", "600x400", "900x400", "1200x400"])
def test_truncated_text_fits_and_uses_the_available_width(root, geometry):
    """Regression: the ellipsis width was subtracted twice and the text was cut back a
    second time, so a 198px alert showed 'Alert information:...' with 77px left unused."""
    root.geometry(geometry)
    root.update()
    alert = send(root, TEXT)
    shown = alert.cget("text")

    assert shown.endswith("...")
    assert TEXT.startswith(shown[:-3])

    # The text fits, the alert does not need more room than it has
    assert alert.winfo_reqwidth() <= alert.winfo_width()

    # ...and it is not shorter than needed: the next word would not fit anymore
    next_word = TEXT[len(shown) - 3:].split()[0]
    text_font = font.Font(font=alert.cget("font"))
    free_width = alert.winfo_width() - alert.winfo_reqwidth()
    assert text_font.measure(" " + next_word) > free_width


def test_text_that_fits_is_left_untouched(root):
    assert send(root, "Short").cget("text") == "Short"


def test_whitespace_is_kept_and_cut_text_always_gets_an_ellipsis(root):
    """Regression: textwrap.shorten() collapsed repeated spaces, the collapsed text then
    fitted and was returned cut in the middle of a word without an ellipsis."""
    text = "Alert     information:      Lorem      Ipsum Dolor"
    shown = send(root, text, width_percentage=0.45).cget("text")

    assert shown != text
    assert shown.endswith("...")
    assert text.startswith(shown[:-3])


def test_words_are_not_cut_in_half(root):
    shown = send(root, TEXT).cget("text")

    assert TEXT[len(shown) - 3:].startswith(" ")


def test_single_long_word_is_cut_by_character(root):
    text = "Supercalifragilisticexpialidocious" * 3
    alert = send(root, text)
    shown = alert.cget("text")

    assert shown.endswith("...")
    assert len(shown) > 3
    assert alert.winfo_reqwidth() <= alert.winfo_width()
