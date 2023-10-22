from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF
from arpeggio import RegExMatch as _
from arpeggio import ParserPython



def start(): return "ARE WE OUT OF THE WOODS"
def end(): return "ALL TOO WELL TIME FLIES"
def variable_name(): return _(r'[a-zA-Z_][a-zA-Z0-9]*')
def string_literal(): return _(r'"(.*)"')
def int_literal(): return _(r'-?[1-9][0-9]+')
def float_literal(): return _(r'-?[1-9][0-9]+\.[0-9]+')
def literal(): return [string_literal, float_literal, int_literal]
def print_statement(): return 'SPEAK NOW OR FOREVER HOLD YOUR PEACE', [variable_name, literal]
def statement(): return [print_statement]
def body(): return [ZeroOrMore(statement), '']

def program(): return start, body, end


test = """
ARE WE OUT OF THE WOODS
SPEAK NOW OR FOREVER HOLD YOUR PEACE "Hello"
ALL TOO WELL TIME FLIES
"""

parser = ParserPython(program)
result = parser.parse(test.strip())
print(result)

