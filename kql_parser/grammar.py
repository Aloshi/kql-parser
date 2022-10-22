from arpeggio import ZeroOrMore, OneOrMore, EOF, RegExMatch, Not, And, Sequence

# Porting the grammar from
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


def value_expression():
    return literal

def field_value_expression():
    return field, ':', list_of_values

def field_range_expression():
    return 'TODO'


def expression():
    #return [field_range_expression, field_value_expression, value_expression]
    return [field_value_expression, value_expression]

def root():
    return expression, EOF
