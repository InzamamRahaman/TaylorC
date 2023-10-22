from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF, PTNodeVisitor, visit_parse_tree
from arpeggio import RegExMatch as _
from arpeggio import ParserPython

class TaylorCTranspilerVisitor(PTNodeVisitor):
    def visit_program(self, node, children):
        body = children.body
        return body

    def visit_body(self, node, children):
        return '\n'.join([str(x) for x in children])

    def visit_variable_name(self, node, children):
        return str(node.value)

    def visit_string_literal(self, node, children):
        return str(f'{node.value}')

    def visit_int_literal(self, node, children):
        return str(node.value)

    def visit_float_literal(self, node, children):
        return str(node.value)

    def visit_literal(self, node, children):
        return children[0]

    def visit_print_statement(self, node, children):
        return f'print({children[0]})'

    def visit_variable_creation(self, node, children):
        return f'{children[0]} = {children[1]}'

    def visit_statement(self, node, children):
        return children[0]

    def visit_increment(self, node, children):
        return f'+= {children[0]}'

    def visit_decrement(self, node, children):
        return f'-= {children[0]}'

    def visit_multiplication(self, node, children):
        return f'*= {children[0]}'

    def visit_division(self, node, children):
        return f'/= {children[0]}'

    def visit_operation(self, node, children):
        return children[0]

    def visit_variable_assignment(self, node, children):
        res = [f'{children[0]} = {children[1]}']
        for child in children[2:]:
            res.append(f'{children[0]} {child}')
        return '\n'.join(res)



def start(): return "ARE WE OUT OF THE WOODS"
def end(): return "ALL TOO WELL TIME FLIES"
def variable_name(): return _(r'[a-zA-Z_][a-zA-Z0-9]*')
def string_literal(): return _(r'"(.*)"')
def int_literal(): return _(r'-?[1-9][0-9]*')
def float_literal(): return _(r'-?[1-9][0-9]*\.[0-9]+')

def number_literal(): return [float_literal, int_literal]
def literal(): return [string_literal, float_literal, int_literal]
def print_statement(): return 'SPEAK NOW OR FOREVER HOLD YOUR PEACE', [variable_name, literal]
def variable_creation(): return 'BLANK SPACE, WRITE YOUR NAME', variable_name, "IT'S A NEW SOUNDTRACK", literal

def increment(): return "UP IN LIGHTS, NOW WE'RE SHINING BRIGHT", number_literal

def decrement(): return 'SHAKE IT OFF, SHAKE IT OFF', number_literal

def multiplication(): return 'OUR LOVE WAS MULTIPLIED', number_literal

def division(): return 'WE ARE NEVER EVER GETTING BACK TOGETHER', number_literal

def operation(): return [increment, decrement, multiplication, division]

def variable_assignment():
    return 'BEGIN AGAIN, STARTING OVER', variable_name, \
        'ONCE UPON A TIME, A FEW MISTAKES AGO', number_literal, ZeroOrMore(operation), \
        "AND THE STORY'S GOT DUST ON EVERY PAGE"
def statement(): return [print_statement, variable_creation, variable_assignment]
def body(): return [ZeroOrMore(statement), '']

def program(): return start, body, end


test = """
ARE WE OUT OF THE WOODS
SPEAK NOW OR FOREVER HOLD YOUR PEACE "Hello"
BLANK SPACE, WRITE YOUR NAME foobar
IT'S A NEW SOUNDTRACK 23
BEGIN AGAIN, STARTING OVER foobar
ONCE UPON A TIME, A FEW MISTAKES AGO 20
OUR LOVE WAS MULTIPLIED 10
SHAKE IT OFF, SHAKE IT OFF 2
UP IN LIGHTS, NOW WE'RE SHINING BRIGHT 5.5
WE ARE NEVER EVER GETTING BACK TOGETHER 3.4
AND THE STORY'S GOT DUST ON EVERY PAGE
SPEAK NOW OR FOREVER HOLD YOUR PEACE foobar
ALL TOO WELL TIME FLIES
"""

# parser_ind = ParserPython(number_literal)
# parse_tree = parser_ind.parse('2')
# print(parse_tree)
#
# parser_ind = ParserPython(decrement)
# parse_tree = parser_ind.parse('SHAKE IT OFF, SHAKE IT OFF 2')
# print(parse_tree)

parser = ParserPython(program)
parse_tree = parser.parse(test.strip())
print(parse_tree)
result = visit_parse_tree(parse_tree, TaylorCTranspilerVisitor())[0]
with open('temp.py', 'w') as fp:
    fp.write(result)



