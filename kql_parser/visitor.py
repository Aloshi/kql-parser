from dataclasses import dataclass
from typing import Union, List, Literal
from arpeggio import PTNodeVisitor

from .grammar import *

_Not = object()

@dataclass
class LiteralNode:
    value: str

@dataclass
class UnquotedLiteralNode(LiteralNode):
    def __str__(self) -> str:
        return self.value

@dataclass
class QuotedLiteralNode(LiteralNode):
    def __str__(self) -> str:
        return f'"{self.value}"'


@dataclass
class ListOfValuesNode:
    operator: Union[Literal['or'], Literal['and'], Literal['not']]
    children: List[Union[LiteralNode, 'ListOfValuesNode']]

    def __str__(self) -> str:
        if len(self.children) == 1:
            if self.operator == 'not':
                return f'not {self.children[0]}'
            else:
                return str(self.children[0])

        return '(' + f' {self.operator} '.join(str(c) for c in self.children) + ')'


@dataclass
class ExpressionNode:
    pass

@dataclass
class ValueExpressionNode(ExpressionNode):
    value: LiteralNode

@dataclass
class FieldValueExpressionNode(ExpressionNode):
    field: LiteralNode
    value: ListOfValuesNode

    def __str__(self) -> str:
        return f'{self.field}: {self.value}'


class KQLVisitor(PTNodeVisitor):
    def visit_unquoted_literal(self, node, children):
        return UnquotedLiteralNode(''.join(children))
    
    def visit_quoted_string(self, node, children):
        return QuotedLiteralNode(''.join(children))
    
    def visit_list_of_values(self, node, children):
        if getattr(children, 'literal', None):
            assert len(children.literal) == 1
            return children.literal[0]
        else:
            assert len(children.or_list_of_values) == 1, children
            return children.or_list_of_values[0]

    def visit_or_list_of_values(self, node, children):
        if len(children) == 1:
            return children[0]
        return ListOfValuesNode(operator='or', children=children)
    
    def visit_and_list_of_values(self, node, children):
        if len(children) == 1:
            return children[0]
        return ListOfValuesNode(operator='and', children=children)
    
    def visit__not(self, node, children):
        # hack to keep the "not" string around when looking at the not_list_of_values node
        return _Not

    def visit_not_list_of_values(self, node, children):
        if len(children) == 1:
            return children[0]
        
        assert children[0] == _Not
        return ListOfValuesNode(operator='not', children=children[1:])

    def visit_field_value_expression(self, node, children):
        assert len(children.field) == 1
        assert len(children.list_of_values) == 1
        return FieldValueExpressionNode(children.field[0], children.list_of_values[0])

    def visit_value_expression(self, node, children):
        assert len(children) == 1
        return ValueExpressionNode(children[0])
