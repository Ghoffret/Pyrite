"""Entry point for executing Pyrite source files."""

import sys

from .nodes import Call
from .parser import parse
from .runtime import *


def run_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    program = parse(code)
    # For demonstration, just build widgets for top-level calls
    widgets = []
    for node in program.body:
        if isinstance(node, Call):
            widget = build_widget(node)
            if widget:
                widgets.append(widget)
    if widgets:
        app = App(Column(*widgets))
        app.run()


def build_widget(node):
    if node.name == "Text":
        return Text(*node.args, **node.kwargs)
    if node.name == "Button":
        return Button(*node.args)
    if node.name == "Column":
        children = [build_widget(c) for c in node.children]
        return Column(*children, **node.kwargs)
    return None


def main(argv: list[str] | None = None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: pyrite <file.pyr>")
        return
    run_file(argv[0])


if __name__ == "__main__":
    main()
