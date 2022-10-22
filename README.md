# What is this?

This is a parser for the Kibana Query Language (KQL), also known as Kuery.
This should pretty faithfully re-implement
[the grammar in Kibana's public repo](https://github.com/elastic/kibana/blob/153f65990ee614677a9c3b2beda634219b6eeee8/packages/kbn-es-query/grammar/grammar.peggy).

# What can I do with it?

You can parse KQL expressions into a tree which makes analysis and re-writing easier. It's kind of like the parse tree parts of [Luqum](https://github.com/jurismarches/luqum), but for KQL.

## How do I use it?

```python
from kql_parser.parser import KQLParseError, Parser

parser = Parser()
tree = parser.parse('a: b or c: (list or of or values) or "bare string"')

# print the parse tree (kind of ugly, sorry)
print(repr(tree))
# OrQueryNode(children=[ExpressionQueryNode(expression=FieldValueExpressionNode(field=UnquotedLiteralNode(value='a'), value=UnquotedLiteralNode(value='b'))), ExpressionQueryNode(expression=FieldValueExpressionNode(field=UnquotedLiteralNode(value='c'), value=ListOfValuesNode(operator='or', children=[UnquotedLiteralNode(value='list'), UnquotedLiteralNode(value='of'), UnquotedLiteralNode(value='values')]))), ExpressionQueryNode(expression=ValueExpressionNode(value=QuotedLiteralNode(value='bare string')))])

# convert the parse tree back to a query string, normalizing/prettifying it
print(tree)
# a: b or c: (list or of or values) or "bare string"
```

Also included is a little CLI tool, useful for testing:

```bash
kql-parser parse 'some: expression' --print-input --tree

some: expression
ExpressionQueryNode(expression=FieldValueExpressionNode(field=UnquotedLiteralNode(value='some'), value=UnquotedLiteralNode(value='expression')))
some: expression
```

# TODO
* Needs tests (!!!)
* Needs to support case insensitivity in keywords!
