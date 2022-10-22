from arpeggio import PTNodeVisitor

from .nodes import *

# internal constant used to keep the "not" token around (since arpeggio stringifies by default)
_Not = object()


class KQLVisitor(PTNodeVisitor):
    """
    Cleans up the arpeggio parse tree into a cleaner tree defined with kql_parser.nodes.

    This gets rid of the "empty" intermediate nodes necessitated by the lack of left-recursive rules
    and is generally nicer to work with.
    """
    def visit_unquoted_literal(self, node, children):
        return UnquotedLiteralNode(''.join(children).strip())
    
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
    
    def visit_expression(self, node, children):
        assert len(children) == 1
        return ExpressionQueryNode(children[0])

    def visit_nested_query(self, node, children):
        if children.field:
            assert len(children.field) == 1
            assert len(children.expression) == 1
            return NestedQueryNode(field=children.field[0], query=children.expression[0])
        else:
            assert len(children) == 1
            return children[0]  # expression

    def visit_sub_query(self, node, children):
        assert len(children) == 1
        if children.or_query:
            return SubQueryNode(children[0])
        return children[0]

    def visit_not_query(self, node, children):
        if len(children) == 1:
            return children[0]  # sub_query
        
        assert children[0] == _Not
        assert len(children) == 2
        return NotQueryNode(query=children[1])

    def visit_and_query(self, node, children):
        if len(children) == 1:
            return children[0]  # not_query
        return AndQueryNode(children=children)

    def visit_or_query(self, node, children):
        if len(children) == 1:
            return children[0]  # and_query
        return OrQueryNode(children=children)
