"""Entry point for executing Pyrite source files."""

from __future__ import annotations

import sys

from .nodes import Call, FuncDef
from .parser import parse
from .runtime import *


def run_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()
    program = parse(code)
    functions: dict[str, FuncDef] = {}
    calls: list[Call] = []
    for node in program.body:
        if isinstance(node, FuncDef):
            functions[node.name] = node
        elif isinstance(node, Call):
            calls.append(node)

    widgets = [build_widget(n, functions) for n in calls]

    if not widgets:
        return

    if len(widgets) == 1 and isinstance(widgets[0], App):
        widgets[0].run()
    else:
        app = App(Column(*widgets))
        app.run()


def build_widget(node: Call, funcs: dict[str, FuncDef]):
    if node.name == "App":
        child = build_widget(node.children[0], funcs) if node.children else None
        return App(child)
    if node.name == "Column":
        children = [build_widget(c, funcs) for c in node.children]
        return Column(*children, **node.kwargs)
    if node.name == "Row":
        children = [build_widget(c, funcs) for c in node.children]
        return Row(*children, **node.kwargs)
    if node.name == "Text":
        return Text(*node.args, **node.kwargs)
    if node.name == "Button":
        on_click = None
        if "on_click" in node.kwargs:
            handler_name = node.kwargs["on_click"]

            def handler(_=None, name=handler_name):
                func = funcs.get(name)
                if func:
                    execute_func(func, funcs)
                else:
                    print(f"{name} triggered")

            on_click = handler
        return Button(*node.args, on_click=on_click)
    return None


def execute_func(func: FuncDef, funcs: dict[str, FuncDef]):
    for stmt in func.body:
        execute_call(stmt, funcs)


def execute_call(call: Call, funcs: dict[str, FuncDef]):
    if call.name == "print":
        print(*call.args)
    elif call.name in funcs:
        execute_func(funcs[call.name], funcs)


def main(argv: list[str] | None = None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: pyrite <file.pyr>")
        return
    run_file(argv[0])


if __name__ == "__main__":
    main()
