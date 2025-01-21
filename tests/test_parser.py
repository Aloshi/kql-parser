import unittest

from kql_parser.parser import Parser
from kql_parser.visitor import (AndQueryNode, ExpressionQueryNode, FieldValueExpressionNode,
                                NestedQueryNode, QuotedLiteralNode, UnquotedLiteralNode, ValueExpressionNode)


class ParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser(debug=False)
        return super().setUp()

    def test_quoted_string(self):
        self.assertEqual(self.parser.parse('"test"'), ExpressionQueryNode(expression=ValueExpressionNode(value=QuotedLiteralNode('test'))))
        # TODO we should strip out the backslash here :/
        self.assertEqual(self.parser.parse('"te\\"st"'), ExpressionQueryNode(expression=ValueExpressionNode(value=QuotedLiteralNode('te\\"st'))))

    def test_field_value_expression(self):
        self.assertEqual(self.parser.parse('fieldname: fieldval'),
                         ExpressionQueryNode(expression=FieldValueExpressionNode(
                                            field=UnquotedLiteralNode('fieldname'),
                                            value=UnquotedLiteralNode('fieldval'))))
    
    def test_unquoted_literal(self):
        self.assertEqual(self.parser.parse('aword'),
                         ExpressionQueryNode(expression=ValueExpressionNode(value=UnquotedLiteralNode('aword'))))
        self.assertEqual(self.parser.parse('words with spaces'),
                         ExpressionQueryNode(expression=ValueExpressionNode(value=UnquotedLiteralNode('words with spaces'))))

    def test_nested_query(self):
        self.assertEqual(self.parser.parse('user.names:{ first: "Alice" and last: "White" }'),
                         NestedQueryNode(field=UnquotedLiteralNode('user.names'),
                                         query=AndQueryNode(children=[
                                             ExpressionQueryNode(expression=FieldValueExpressionNode(
                                                 field=UnquotedLiteralNode('first'),
                                                 value=QuotedLiteralNode('Alice'),
                                             )),
                                             ExpressionQueryNode(expression=FieldValueExpressionNode(
                                                 field=UnquotedLiteralNode('last'),
                                                 value=QuotedLiteralNode('White'),
                                             )),
                                         ])))


if __name__ == '__main__':
    unittest.main()
