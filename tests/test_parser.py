import unittest

from kql_parser.parser import Parser
from kql_parser.visitor import FieldValueExpressionNode, QuotedLiteralNode, UnquotedLiteralNode


class ParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = Parser(debug=False)
        return super().setUp()

    def test_quoted_string(self):
        self.assertEqual(self.parser.parse('"test"'), QuotedLiteralNode('test'))
        self.assertEqual(self.parser.parse('"te\\"st"'), QuotedLiteralNode('te\"st'))

    def test_field_value_expression(self):
        self.assertEqual(self.parser.parse('fieldname: fieldval'),
                         FieldValueExpressionNode(field=UnquotedLiteralNode('fieldname'),
                                                  value=UnquotedLiteralNode('fieldval')))
    
    def test_unquoted_literal(self):
        self.assertEqual(self.parser.parse('aword'), UnquotedLiteralNode('aword'))
        self.assertEqual(self.parser.parse('words with spaces'), UnquotedLiteralNode('words with spaces'))

if __name__ == '__main__':
    unittest.main()
