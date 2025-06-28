"""Color utilities for Pyrite."""

from typing import Tuple


def rgb(r: int, g: int, b: int) -> str:
    """Return Tkinter color string from RGB integers."""
    return f"#{r:02x}{g:02x}{b:02x}"
