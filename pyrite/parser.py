"""A simple recursive-descent parser for Pyrite."""

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
        while self.pos < len(self.tokens):
            tok = self.peek()
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
        # consume '(' ')' ':'
        while self.peek()[0] != "COLON" and self.pos < len(self.tokens):
            self.advance()
        if self.peek()[0] == "COLON":
            self.advance()
        body = []
        while self.pos < len(self.tokens) and self.peek()[0] != "NAME":
            self.advance()
        return FuncDef(name=name, body=body)

    def call(self) -> Call:
        name = self.advance()[1]
        args = []
        kwargs = {}
        while self.pos < len(self.tokens):
            tok = self.peek()
            if tok[0] == "STRING" or tok[0] == "NUMBER":
                args.append(tok[1].strip('"'))
                self.advance()
            elif tok[0] == "NAME" and self._next_is("ASSIGN"):
                key = tok[1]
                self.advance()
                self.advance()  # consume '='
                value = self.advance()[1]
                kwargs[key] = value.strip('"')
            elif tok[0] == "NEWLINE":
                self.advance()
                break
            else:
                self.advance()
        return Call(name=name, args=args, kwargs=kwargs)

    def _next_is(self, token_type: str) -> bool:
        return (self.pos + 1 < len(self.tokens) and
                self.tokens[self.pos + 1][0] == token_type)


def parse(code: str) -> Program:
    return Parser(lex(code)).parse()
