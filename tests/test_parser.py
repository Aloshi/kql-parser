import unittest

from kql_parser.parser import parse


class ParserTests(unittest.TestCase):
    def test_quoted_string(self):
        self.assertEqual(parse('"test"').expression.value_expression.quoted_string[0][1], ['test'])
        self.assertEqual(parse('"te\\"st"').expression.value_expression.quoted_string[0][1:-1], [['te'], ['\\"'], ['st']])

    def test_field_value_expression(self):
        expr = parse('fieldname: fieldval').expression.field_value_expression
        self.assertEqual(expr.field, ['fieldname'])

if __name__ == '__main__':
    unittest.main()
