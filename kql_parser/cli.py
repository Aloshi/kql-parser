import click
import sys
from arpeggio import visit_parse_tree
from .parser import KQLParseError, Parser
from .visitor import KQLVisitor


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('expr', type=str)
@click.option('--tree/--no-tree', 'print_tree', type=bool, default=False)
@click.option('--debug/--no-debug', 'debug', type=bool, default=False)
def parse(expr: str, print_tree: bool, debug: bool):
    print(expr)
    parser = Parser(debug=debug)

    try:
        parse_tree = parser.parse(expr)
        print('---visitor ---')
        visit_parse_tree(parse_tree, KQLVisitor(debug=debug))

        if print_tree:
            print(parse_tree.tree_str())
        else:
            print(parse_tree)
    except KQLParseError as e:
        click.echo(str(e))
        sys.exit(1)


if __name__ == '__main__':
    cli()
