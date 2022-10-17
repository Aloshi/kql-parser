from arpeggio import ParserPython, ParseTreeNode, NoMatch, PTNodeVisitor

from .grammar import root


class KQLParseError(Exception):
    pass


class Parser:
    def __init__(self, debug: bool=False) -> None:
        self._parser = ParserPython(root, debug=debug)
    
    def parse(self, expr: str) -> ParseTreeNode:
        try:
            return self._parser.parse(expr)
        except NoMatch as e:
            raise KQLParseError(str(e))
