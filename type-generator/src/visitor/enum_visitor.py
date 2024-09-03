import textwrap
from typing import List

from tree_sitter import Node, Tree
from ..generator.enum_generator import EnumGenerator
from .visitor import Visitor
from ..models import EnumProperty
from ..util import to_enum_case


class EnumVisitor(Visitor):
    _encoding = "utf-8"
    _number_type = "long"

    enum_name = ""
    _types: List[EnumProperty] = []

    def __init__(self, tree: Tree):
        self.tree = tree
        self.enum_name = ""
        self._types = []

    def _generate(self) -> str:
        return EnumGenerator(self.enum_name, self._types).build()

    def visit_type_alias_declaration(self, node: Node):
        self.enum_name = node.child_by_field_name("name").text.decode(self._encoding)
        self._accept_list(node.children)

    def visit_string_fragment(self, node: Node):
        name = node.text.decode(self._encoding)
        self._types.append(EnumProperty(
            name,
            to_enum_case(name)
        ))
