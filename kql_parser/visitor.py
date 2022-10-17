from arpeggio import PTNodeVisitor

from .grammar import *

class KQLVisitor(PTNodeVisitor):
    def visit_unquoted_literal(self, node, children):
        for child in children:
            print(child)
        
        return node


