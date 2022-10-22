from arpeggio import ZeroOrMore, OneOrMore, EOF, RegExMatch, Not, And, Sequence

# Port of the Peggy grammar in Kibana 8.4, with a few changes
# (mostly around unquoted_literal / unquoted_character to work with arpeggio's "eat whitespace by defaukt" behavior)
# https://github.com/elastic/kibana/blob/153f65990ee614677a9c3b2beda634219b6eeee8/packages/kbn-es-query/grammar/grammar.peggy


def special_character():
    return RegExMatch(r'[\\():<>"*{}]')

def escaped_special_character():
    return '\\', special_character

def escaped_whitespace():
    return ['\\t', '\\r', '\\n']

def escaped_unicode_sequence():
    return '\\', RegExMatch(r'u[0-9a-f]{4}')

def keyword():
    # make sure this ends on a word boundary so stuff like "ora" or "andy" doesn't match
    # (And does not consume input)
    return ['or ', 'and ', 'not '] #, And([' ', special_character, EOF])

def escaped_keyword():
    return '\\', keyword

def wildcard():
    return '*'

def _not():
    return 'not '

def _or():
    return 'or '

def _and():
    return 'and '

def range_operator():
    return ['<=', '>=', '<', '>']

def unquoted_character():
    return [escaped_whitespace, escaped_special_character, escaped_unicode_sequence, escaped_keyword, wildcard,
        (Not(keyword), RegExMatch(r'[^\\():<>"*{} ]+| +'))]  # ensure it's not a keyword, then consume input until the next boundary

def unquoted_literal():
    # some tricky stuff with 'skipws' here. arpeggio skips whitespace, but unquoted literals are whitespace-sensitive
    return Sequence(ZeroOrMore(' '), skipws=False, suppress=True), Sequence(OneOrMore(unquoted_character), skipws=False)


def quoted_character():
    return [escaped_whitespace, escaped_unicode_sequence, '\\"', RegExMatch(r'[^"\\]+')]

def quoted_string():
    return Sequence(ZeroOrMore(' ', suppress=True), '"', ZeroOrMore(quoted_character), '"', skipws=False)

def literal():
    return [quoted_string, unquoted_literal]


def field():
    return [quoted_string, unquoted_literal]

def not_list_of_values():
    return [(_not, list_of_values), list_of_values]

def and_list_of_values():
    return [(not_list_of_values, OneOrMore(('and ', not_list_of_values))), not_list_of_values]

def or_list_of_values():
    return [(and_list_of_values, OneOrMore(('or ', and_list_of_values))), and_list_of_values]

def list_of_values():
    return [('(', or_list_of_values, ')'), literal]


def nested_query():
    return [(field, ':', '{', or_query, '}'), expression]

def sub_query():
    return [('(', or_query, ')'), nested_query]

def not_query():
    return [(_not, sub_query), sub_query]

def and_query():
    return [(not_query, OneOrMore(_and, not_query)), not_query]

def or_query():
    return [(and_query, OneOrMore(_or, and_query)), and_query]


def value_expression():
    return literal

def field_value_expression():
    return field, ':', list_of_values

def field_range_expression():
    return field, range_operator, literal


def expression():
    return [field_range_expression, field_value_expression, value_expression]

def start():
    return or_query, EOF
