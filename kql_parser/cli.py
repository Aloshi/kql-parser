import click
import sys
from arpeggio import visit_parse_tree
from pprint import pprint
from .parser import KQLParseError, Parser
from .visitor import ExpressionNode


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('expr', type=str)
@click.option('--tree/--no-tree', 'print_tree', type=bool, default=False)
@click.option('--debug/--no-debug', 'debug', type=bool, default=False)
def parse(expr: str, print_tree: bool, debug: bool):
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
