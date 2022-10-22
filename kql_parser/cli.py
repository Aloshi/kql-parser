import click
import sys
from arpeggio import visit_parse_tree
from pprint import pprint
from .parser import KQLParseError, Parser
from .visitor import ExpressionNode


@click.group()
def cli():
    pass


@cli.command('parse',
             help='Parse a KQL query and print it back out in a normalized form.\n\n'
                  "$ kql-parser parse 'test:   ((a   or  b) and c) or \"quoted   value\"'\n\n"
                  "test: ((a or b) and c) or \"quoted   value\"")
@click.argument('expr', type=str)
@click.option('--print-input/--no-print-input', 'print_input',
              help='Print the input argument (useful for debugging shell escape-related issues).',
              type=bool, default=False)
@click.option('--tree/--no-tree', 'print_tree',
              help='Print the repr of the tree of parsed nodes.',
              type=bool, default=False)
@click.option('--debug/--no-debug', 'debug',
              help='Enable arpeggio\'s debug output (prints parse rule logs, the final arpeggio parse tree, generates graphviz .dot files of the parse tree, and prints parse tree visitor logs).',
              type=bool, default=False)
def parse(expr: str, print_input: bool, print_tree: bool, debug: bool):
    if print_input:
        click.echo(expr)

    parser = Parser(debug=debug)

    try:
        tree = parser.parse(expr)
        if print_tree:
            pprint(tree)
        
        click.echo(str(tree))
    except KQLParseError as e:
        click.echo(str(e))
        sys.exit(1)


if __name__ == '__main__':
    cli()
