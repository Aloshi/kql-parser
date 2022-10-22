from arpeggio import ParserPython, NoMatch, visit_parse_tree
from typing import cast, Union

from kql_parser.nodes import QueryNode, ExpressionNode
from kql_parser.grammar import start
from kql_parser.visitor import KQLVisitor


class KQLParseError(Exception):
    pass


class Parser:
    def __init__(self, debug: bool=False) -> None:
        self._parser = ParserPython(start, debug=debug)

    def _parse_to_arpeggio_tree(self, expr: str):
        parse_tree = self._parser.parse(expr)
        if self._parser.debug:
            print(parse_tree.tree_str())
        return parse_tree
    
    def _clean_tree(self, arpeggio_tree) -> Union[QueryNode, ExpressionNode]:
        return cast(ExpressionNode, visit_parse_tree(arpeggio_tree, KQLVisitor(debug=self._parser.debug)))

    def parse(self, expr: str) -> ExpressionNode:
        try:
            parse_tree = self._parse_to_arpeggio_tree(expr)
            return self._clean_tree(parse_tree)
        except NoMatch as e:
            raise KQLParseError(str(e))
