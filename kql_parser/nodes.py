
from dataclasses import dataclass
from typing import Union, List, Literal


@dataclass
class LiteralNode:
    """A literal value, either quoted or unquoted."""
    value: str

@dataclass
class UnquotedLiteralNode(LiteralNode):
    """
    An unquoted literal.

    KQL examples:
    * `some words`
    * `oneword`
    * `something*withawildcard`
    """
    def __str__(self) -> str:
        return self.value

@dataclass
class QuotedLiteralNode(LiteralNode):
    """
    A quoted literal.
    `value` does not include the leading or trailing quotes (they
    are implied by the fact that this is a QuotedLiteralNode).

    KQL examples:
    * `"oneword"
    * `"some words"`
    * `"with \" escaped quote"`
    """
    def __str__(self) -> str:
        return f'"{self.value}"'


@dataclass
class ListOfValuesNode:
    """
    A list of literals combined with some operator.
    
    Note that when operator=not, there is always a single value in children.
    """
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
    """
    An expression. This is generally the meat of a query.
    ExpressionNodes are chained together with or/and/not using QueryNode's subclasses.
    """
    pass

@dataclass
class ValueExpressionNode(ExpressionNode):
    """
    Just a literal, which typically searches all fields defined for the "index.query.default_field" setting
    for the index (unless this expression is inside a SubQueryNode).
    """
    value: LiteralNode

    def __str__(self) -> str:
        return str(self.value)

@dataclass
class FieldValueExpressionNode(ExpressionNode):
    """
    Expression for searching a particular field.

    KQL examples:
    * `field: *`
    * `field: value`
    * `field: (a or b)`
    """
    field: LiteralNode
    value: ListOfValuesNode

    def __str__(self) -> str:
        return f'{self.field}: {self.value}'

@dataclass
class FieldRangeExpressionNode(ExpressionNode):
    """
    Expression for filtering a field by some range.

    KQL examples:
    * `field > 500`
    * `field <= 100`
    """
    field: LiteralNode
    operator: Union[Literal['<='], Literal['>='], Literal['<'], Literal['>']]
    value: LiteralNode

    def __str__(self) -> str:
        return f'{self.field} {self.operator} {self.value}'


@dataclass
class QueryNode:
    """These nodes are the top level/root of the tree."""
    pass

@dataclass
class ExpressionQueryNode(QueryNode):
    """Any expression. This is generally the meat of a query."""
    expression: ExpressionNode

    def __str__(self) -> str:
        return str(self.expression)

@dataclass
class OrQueryNode(QueryNode):
    """A list of queries/expressions or'd together."""
    children: List[QueryNode]

    def __str__(self) -> str:
        return ' or '.join(str(c) for c in self.children)

@dataclass
class AndQueryNode(QueryNode):
    """A list of queries/expressions and'd together."""
    children: List[QueryNode]

    def __str__(self) -> str:
        return ' and '.join(str(c) for c in self.children)

@dataclass
class NotQueryNode(QueryNode):
    """Inversion of a query/expression."""
    query: QueryNode

    def __str__(self) -> str:
        return f'not {self.query}'

@dataclass
class SubQueryNode(QueryNode):
    """
    Query/expression in parenthesis.

    KQL examples:
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
    """
    Special query for searching nested fields.

    KQL examples:
    * `field: { nested_field: value }`
    """
    field: LiteralNode
    query: QueryNode

    def __str__(self) -> str:
        return f'{self.field}: {self.query}'
