"""Minimal UI primitives using Tkinter for demonstration purposes."""

import tkinter as tk
from typing import Callable, Any

class Widget:
    def __init__(self):
        self.widget = None

    def build(self, parent):
        raise NotImplementedError

class App(Widget):
    def __init__(self, child: Widget):
        super().__init__()
        self.child = child
        self.root = tk.Tk()

    def run(self):
        self.build(None)
        self.root.mainloop()

    def build(self, parent):
        if self.child:
            self.child.build(self.root)

class Column(Widget):
    def __init__(self, *children, spacing: int = 0):
        super().__init__()
        self.children = list(children)
        self.spacing = spacing

    def build(self, parent):
        frame = tk.Frame(parent)
        frame.pack()
        for child in self.children:
            child.build(frame)
            if self.spacing:
                tk.Frame(frame, height=self.spacing).pack()

class Row(Widget):
    def __init__(self, *children, spacing: int = 0):
        super().__init__()
        self.children = list(children)
        self.spacing = spacing

    def build(self, parent):
        frame = tk.Frame(parent)
        frame.pack()
        for child in self.children:
            child.build(frame)
            if self.spacing:
                tk.Frame(frame, width=self.spacing).pack(side=tk.LEFT)

class Text(Widget):
    def __init__(self, text: str, color: str = None):
        super().__init__()
        self.text = text
        self.color = color

    def build(self, parent):
        label = tk.Label(parent, text=self.text, fg=self.color)
        label.pack()

class Button(Widget):
    def __init__(self, text: str, on_click: Callable[[Any], None] = None):
        super().__init__()
        self.text = text
        self.on_click = on_click

    def build(self, parent):
        btn = tk.Button(parent, text=self.text)
        if self.on_click:
            btn.config(command=lambda: self.on_click(None))
        btn.pack()
