"""A very small lexer for the Pyrite language with indentation support."""

from __future__ import annotations

import re
from typing import Iterator, Tuple, List

Token = Tuple[str, str]

TOKEN_REGEX = re.compile(
    r"(?P<NAME>[A-Za-z_][A-Za-z0-9_]*)"
    r"|(?P<NUMBER>\d+)"
    r"|(?P<STRING>\"[^\"]*\"|'[^']*')"
    r"|(?P<ASSIGN>=)"
    r"|(?P<ARROW>=\>)"
    r"|(?P<COLON>:)"
    r"|(?P<WS>[ \t]+)"
    r"|(?P<MISC>.)"
)

IGNORED = {"WS"}


def lex(code: str) -> Iterator[Token]:
    """Yield tokens from the source string including INDENT/DEDENT."""

    indent_levels: List[int] = [0]
    lines = code.splitlines()

    for raw_line in lines:
        if not raw_line.strip():
            yield ("NEWLINE", "\n")
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent > indent_levels[-1]:
            indent_levels.append(indent)
            yield ("INDENT", "")
        while indent < indent_levels[-1]:
            indent_levels.pop()
            yield ("DEDENT", "")

        line = raw_line.lstrip(" ")
        pos = 0
        while pos < len(line):
            m = TOKEN_REGEX.match(line, pos)
            if not m:
                raise SyntaxError(f"Unexpected character: {line[pos]!r}")
            kind = m.lastgroup
            value = m.group(kind)
            pos = m.end()
            if kind not in IGNORED:
                yield (kind, value)
        yield ("NEWLINE", "\n")

    while len(indent_levels) > 1:
        indent_levels.pop()
        yield ("DEDENT", "")
    yield ("EOF", "")
