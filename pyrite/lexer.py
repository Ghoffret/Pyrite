"""A very small lexer for the Pyrite language."""

import re
from typing import Iterator, Tuple

Token = Tuple[str, str]

TOKEN_REGEX = re.compile(
    r"(?P<NEWLINE>\n)|"
    r"(?P<NAME>[A-Za-z_][A-Za-z0-9_]*)|"
    r"(?P<NUMBER>\d+)|"
    r"(?P<STRING>\"[^\"]*\"|'[^']*')|"
    r"(?P<ASSIGN>=)|"
    r"(?P<ARROW>=\>)|"
    r"(?P<COLON>:)|"
    r"(?P<WS>[ \t]+)|"
    r"(?P<MISC>.)"
)

IGNORED = {"WS"}


def lex(code: str) -> Iterator[Token]:
    pos = 0
    while pos < len(code):
        m = TOKEN_REGEX.match(code, pos)
        if not m:
            raise SyntaxError(f"Unexpected character: {code[pos]!r}")
        kind = m.lastgroup
        value = m.group(kind)
        pos = m.end()
        if kind not in IGNORED:
            yield (kind, value)
