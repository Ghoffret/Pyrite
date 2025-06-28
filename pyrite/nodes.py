"""Simple AST node definitions for Pyrite."""

from dataclasses import dataclass, field
from typing import List, Any, Optional

@dataclass
class Node:
    pass

@dataclass
class Program(Node):
    body: List[Node] = field(default_factory=list)

@dataclass
class Call(Node):
    name: str
    args: List[Any] = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)
    children: List[Node] = field(default_factory=list)

@dataclass
class FuncDef(Node):
    name: str
    body: List[Node] = field(default_factory=list)
