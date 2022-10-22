# What is this?

This is a parser for the Kibana Query Language (KQL), also known as Kuery.
This should pretty faithfully re-implement
[the grammar in Kibana's public repo](https://github.com/elastic/kibana/blob/153f65990ee614677a9c3b2beda634219b6eeee8/packages/kbn-es-query/grammar/grammar.peggy).

# What can I do with it?

You can parse KQL expressions into a tree which makes analysis and re-writing easier. It's kind of like the parse tree parts of [Luqum](https://github.com/jurismarches/luqum), but for KQL.

For example, when paired with the appropriate Kibana saved object data, you could use this to see what documents dashboards/visualizations/alerts are actually looking at.
(Particularly useful if you can't use the [field usage stats API](https://www.elastic.co/guide/en/elasticsearch/reference/current/field-usage-stats.html)
because you have a common set of fields across most documents, but documents are filtered by some `type: blah`-esque query.)

## How do I use it?

First, install the library (add to `requirements.txt` and/or `pip install kql-parser`).

```python
from kql_parser.parser import KQLParseError, Parser

parser = Parser()

try:
    tree = parser.parse('a: b or c: (list or of or values) or "bare string"')
except KQLParseError as e:
    print(e)

# print the parse tree (kind of ugly, sorry)
print(repr(tree))
# OrQueryNode(children=[ExpressionQueryNode(expression=FieldValueExpressionNode(field=UnquotedLiteralNode(value='a'), value=UnquotedLiteralNode(value='b'))), ExpressionQueryNode(expression=FieldValueExpressionNode(field=UnquotedLiteralNode(value='c'), value=ListOfValuesNode(operator='or', children=[UnquotedLiteralNode(value='list'), UnquotedLiteralNode(value='of'), UnquotedLiteralNode(value='values')]))), ExpressionQueryNode(expression=ValueExpressionNode(value=QuotedLiteralNode(value='bare string')))])

# convert the parse tree back to a query string, normalizing/prettifying it
print(tree)
# a: b or c: (list or of or values) or "bare string"
```

Also included is a little CLI tool, useful for testing:

```bash
$ kql-parser parse 'some:   expression' --print-input --tree

some:   expression  # input
ExpressionQueryNode(expression=FieldValueExpressionNode(field=UnquotedLiteralNode(value='some'), value=UnquotedLiteralNode(value='expression')))  # parse tree
some: expression  # stringified parse tree
```

# TODO
* Needs to support case insensitivity in keywords (this is a big one!)
* Needs tests (!!!)
* Add a nicer way to print the parse tree
* Move the CLI bit into something configurable so you can pull this project without installing click
