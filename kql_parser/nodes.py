
from dataclasses import dataclass
from typing import Union, List, Literal


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

    def __str__(self) -> str:
        return str(self.value)

@dataclass
class FieldValueExpressionNode(ExpressionNode):
    field: LiteralNode
    value: ListOfValuesNode

    def __str__(self) -> str:
        return f'{self.field}: {self.value}'


@dataclass
class QueryNode:
    pass

@dataclass
class OrQueryNode(QueryNode):
    children: List[QueryNode]

    def __str__(self) -> str:
        return ' or '.join(str(c) for c in self.children)

@dataclass
class AndQueryNode(QueryNode):
    children: List[QueryNode]

    def __str__(self) -> str:
        return ' and '.join(str(c) for c in self.children)

@dataclass
class NotQueryNode(QueryNode):
    query: QueryNode

    def __str__(self) -> str:
        return f'not {self.query}'

@dataclass
class SubQueryNode(QueryNode):
    """
    Query in parenthesis.

    Examples:
    (a)
    (a: value)
    (a or b)
    ( a or field1: value or field2: (value1 or value2) )
    """
    query: QueryNode

    def __str__(self) -> str:
        return f'({self.query})'

@dataclass
class NestedQueryNode(QueryNode):
    """field: { ... }"""
    field: LiteralNode
    query: QueryNode

    def __str__(self) -> str:
        return f'{self.field}: {self.query}'
