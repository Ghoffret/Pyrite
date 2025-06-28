# Pyrite

Pyrite is a Python-based programming language focused on designers. It
provides a clean, readable syntax with built-in primitives for UI, layout,
color and motion. Pyrite applications compile to Python and can run on any
Python runtime.

This repository contains an experimental implementation consisting of a
simple lexer, parser and a small runtime library.

## Language Overview

Pyrite reimagines Python syntax with a more compact style aimed at UI-driven
applications. A Pyrite source file uses indentation for block structure, but
omits colons and parentheses whenever possible. Function calls and property
assignments use minimal punctuation, and the runtime provides primitives for
widgets, layout containers, color manipulation and animation.

Example:

```pyr
App:
    Column spacing=10:
        Text "Hello World" color=rgb(200, 100, 100)
        Button "Click" on_click => handle_click
```

## Components

- **UI**: basic widgets such as `Text`, `Button`, `Column` and `Row`.
- **Layout**: containers manage positioning and spacing automatically.
- **Color**: helper functions for RGB/HSV conversion.
- **Motion**: simple animation primitives like `animate`.

## Running

The `pyrite.main` module loads a `.pyr` source file, parses it and executes it
using the runtime. This implementation is intentionally small and incomplete,
but demonstrates how Pyrite code could be executed.

To run the example:

```bash
python -m pyrite examples/hello.pyr
```

## Status

This project is an experiment and not a complete language. It is intended as a
starting point for discussion and exploration of designer-focused
programming ideas.
