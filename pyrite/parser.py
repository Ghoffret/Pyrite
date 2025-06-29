"""A simple recursive-descent parser for Pyrite with nested blocks."""

from __future__ import annotations

from typing import List, Iterator
from .lexer import lex, Token
from .nodes import Program, Call, FuncDef

class Parser:
    def __init__(self, tokens: Iterator[Token]):
        self.tokens = list(tokens)
        self.pos = 0

    def peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("EOF", "")

    def advance(self) -> Token:
        tok = self.peek()
        self.pos += 1
        return tok

    def parse(self) -> Program:
        prog = Program()
        while self.peek()[0] != "EOF":
            tok = self.peek()
            if tok[0] == "NEWLINE":
                self.advance()
                continue
            if tok[0] == "NAME" and tok[1] == "fun":
                prog.body.append(self.func_def())
            elif tok[0] == "NAME":
                prog.body.append(self.call())
            else:
                self.advance()  # Skip unknown tokens
        return prog

    def func_def(self) -> FuncDef:
        self.advance()  # consume 'fun'
        name = self.advance()[1]
        # consume until ':' then parse block
        while self.peek()[0] != "COLON" and self.peek()[0] != "NEWLINE":
            self.advance()
        if self.peek()[0] == "COLON":
            self.advance()
        self.expect("NEWLINE")
        self.expect("INDENT")
        body = []
        while self.peek()[0] != "DEDENT":
            if self.peek()[0] == "NEWLINE":
                self.advance()
                continue
            body.append(self.call())
        self.expect("DEDENT")
        return FuncDef(name=name, body=body)

    def call(self) -> Call:
        name = self.expect("NAME")[1]
        args: List[str] = []
        kwargs: dict[str, str] = {}
        children: List[Call] = []

        while True:
            tok = self.peek()
            if tok[0] in {"STRING", "NUMBER"}:
                val = self.advance()[1]
                args.append(val.strip('"').strip("'"))
            elif tok[0] == "NAME" and self._next_is("ASSIGN"):
                key = self.advance()[1]
                self.expect("ASSIGN")
                val = self.advance()[1]
                kwargs[key] = val.strip('"').strip("'")
            elif tok[0] == "NAME" and self._next_is("ARROW"):
                key = self.advance()[1]
                self.expect("ARROW")
                val = self.advance()[1]
                kwargs[key] = val
            elif tok[0] == "COLON":
                self.advance()
                self.expect("NEWLINE")
                self.expect("INDENT")
                while self.peek()[0] != "DEDENT":
                    if self.peek()[0] == "NEWLINE":
                        self.advance()
                        continue
                    children.append(self.call())
                self.expect("DEDENT")
                break
            else:
                break
        if self.peek()[0] == "NEWLINE":
            self.advance()
        return Call(name=name, args=args, kwargs=kwargs, children=children)

    def _next_is(self, token_type: str) -> bool:
        return (self.pos + 1 < len(self.tokens) and
                self.tokens[self.pos + 1][0] == token_type)

    def expect(self, token_type: str) -> Token:
        tok = self.advance()
        if tok[0] != token_type:
            raise SyntaxError(f"Expected {token_type} but got {tok}")
        return tok


def parse(code: str) -> Program:
    return Parser(lex(code)).parse()
