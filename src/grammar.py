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

    def visit_modulo(self, node, children):
        return f'%= {children[0]}'

    def visit_operation(self, node, children):
        return children[0]

    def visit_variable_assignment(self, node, children):
        res = [f'{children[0]} = {children[1]}']
        for child in children[2:]:
            if type(child) == str:
                res.append(f'{children[0]} {child}')
            else:
                if child[0] == 1:
                    bool_op = child[1]
                    res.append(f'{children[0]} = int({children[0]} {bool_op} {child[2]})')
                if child[0] == 2:
                    bool_op = child[1]
                    component = f'{children[0]} = int(bool({children[0]}) {bool_op} bool({child[2]}))'
        return '\n'.join(res)

    def visit_operand(self, node, children):
        return children[0]

    def visit_equal_to(self, node, children):
        return (1, '==', str(children[0]))

    def visit_greater_than(self, node, children):
        return (1, '>', str(children[0]))

    def visit_or_oper(self, node, children):
        return (2, 'or', str(children[0]))

    def visit_and_oper(self, node, children):
        return (2, 'and', str(children[0]))

    def visit_if_body(self, node, children):
        #return children
        return '\n'.join(map(lambda x: f'    {x}', children))

    def visit_if_stmnt(self, node, children):
        body = '\n'.join(map(lambda x: f'    {x}', children[1].split('\n')))
        res = f'if {children[0]}:\n'
        res += body
        return res

    def visit_if_else_stmnt(self, node, children):
        body = '\n'.join(map(lambda x: f'{x}', children[1].split('\n')))
        res = f'if {children[0]}:\n'
        res += body
        res += '\nelse:\n'
        res += children[2]
        return res

    def visit_while_body(self, node, children):
        res = 'pass'
        if len(children) > 0:
            res = '\n'.join(map(lambda x: f'{x}', children))
        return res


    def visit_while_block(self, node, children):
        body = ''
        if len(children) > 1:
            body = '\n'.join(map(lambda x: f'    {x}', children[1].split('\n')))
        res = f'while {children[0]}:\n'
        res += body
        return res

    def visit_argument_list(self, node, children):
        return ', '.join(children)

    def visit_argument(self, node, children):
        return children

    def visit_non_void_function(self, node, children):
        argument_listing = children[1]
        function_name = children[0]
        header = f'def {function_name}({argument_listing}):\n'
        body = '    pass'
        if len(children) > 2:
            body = map(lambda x: f'    {x}', children[2:])
            body = '\n'.join(body)
        func_def = f'{header}\n{body}'
        return func_def

    def visit_void_function(self, node, children):
        function_name = children[0]
        header = f'def {function_name}():\n'
        body = '    pass'
        if len(children) > 1:
            body = map(lambda x: f'    {x}', children[1:])
            body = '\n'.join(body)
        func_def = f'{header}\n{body}'
        return func_def



def start(): return "ARE WE OUT OF THE WOODS"
def end(): return "ALL TOO WELL TIME FLIES"
def variable_name(): return _(r'[a-zA-Z_][a-zA-Z0-9]*')
def string_literal(): return _(r'"(.*)"')
def int_literal(): return _(r'(-?[1-9][0-9]*)|0')
def float_literal(): return _(r'((-?[1-9][0-9]*)|0)\.[0-9]+')

def number_literal(): return [float_literal, int_literal]
def literal(): return [string_literal, float_literal, int_literal]
def print_statement(): return 'SPEAK NOW OR FOREVER HOLD YOUR PEACE', [variable_name, literal]
def variable_creation(): return 'BLANK SPACE, WRITE YOUR NAME', variable_name, "IT'S A NEW SOUNDTRACK", literal

def operand(): return [number_literal, variable_name]
def increment(): return "UP IN LIGHTS, NOW WE'RE SHINING BRIGHT", operand

def decrement(): return 'SHAKE IT OFF, SHAKE IT OFF', operand

def multiplication(): return 'OUR LOVE WAS MULTIPLIED', operand

def division(): return 'WE ARE NEVER EVER GETTING BACK TOGETHER', operand

def modulo(): return 'AND THE PIECES OF ME THAT YOU GOT', operand

def equal_to(): return "YOU'RE THE ONLY ONE OF YOU", operand

def greater_than(): return "I'M SHINING LIKE FIREWORKS OVER YOUR SAD, EMPTY TOWN", operand

def or_oper(): return 'WE LEARN TO LIVE WITH THE PAIN, MOSAIC BROKEN HEARTS', operand

def and_oper(): return "BAND-AIDS DON'T FIX BULLET HOLES", operand

def if_body():
    return ZeroOrMore(statement)

def if_stmnt():
    return 'IF THE HIGH WAS WORTH THE PAIN', operand, if_body, 'BUT WE HAD TO END IT'

def if_else_stmnt():
    return 'IF THE HIGH WAS WORTH THE PAIN', operand, if_body, 'BUT DREAMS COME TRUE', if_body,\
        'BUT WE HAD TO END IT'

def while_body():
    return ZeroOrMore(statement)

def while_block():
    return "AND WE'LL NEVER GO OUT OF STYLE", operand, while_body, 'JUST TAKE A DEEP BREATH AND LET IT GO'


def argument():
    return "ALL I KNOW IS THAT YOU'RE MINE", variable_name
def argument_list():
    return OneOrMore(argument)


def operation():
    return [increment, decrement, multiplication, division, modulo, equal_to,
            greater_than, or_oper, and_oper, if_stmnt, if_else_stmnt]

def variable_assignment():
    return 'BEGIN AGAIN, STARTING OVER', variable_name, \
        'ONCE UPON A TIME, A FEW MISTAKES AGO', number_literal, ZeroOrMore(operation), \
        "AND THE STORY'S GOT DUST ON EVERY PAGE"
def statement(): return [print_statement, variable_creation, variable_assignment, if_stmnt, if_else_stmnt, while_block]

def void_function():
    return "ARE YOU READY FOR IT?", variable_name, ZeroOrMore(statement), 'WE ARE NEVER EVER GETTING BACK TOGETHER'

def non_void_function():
    return "ARE YOU READY FOR IT?", variable_name, argument_list, ZeroOrMore(statement), 'WE ARE NEVER EVER GETTING BACK TOGETHER'

def function():
    return [non_void_function, void_function]

def body_elems():
    return [statement, if_else_stmnt, if_stmnt, while_block, function]

def body(): return [ZeroOrMore(body_elems), '']

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
YOU'RE THE ONLY ONE OF YOU 20
I'M SHINING LIKE FIREWORKS OVER YOUR SAD, EMPTY TOWN 0
AND THE STORY'S GOT DUST ON EVERY PAGE
SPEAK NOW OR FOREVER HOLD YOUR PEACE foobar
IF THE HIGH WAS WORTH THE PAIN 1
BLANK SPACE, WRITE YOUR NAME bar
IT'S A NEW SOUNDTRACK 23
BUT DREAMS COME TRUE
BLANK SPACE, WRITE YOUR NAME bar
IT'S A NEW SOUNDTRACK 12
BUT WE HAD TO END IT
AND WE'LL NEVER GO OUT OF STYLE 0
SPEAK NOW OR FOREVER HOLD YOUR PEACE "Hello"
SPEAK NOW OR FOREVER HOLD YOUR PEACE "Hello"
SPEAK NOW OR FOREVER HOLD YOUR PEACE "Hello"
IF THE HIGH WAS WORTH THE PAIN 1
BLANK SPACE, WRITE YOUR NAME bar
IT'S A NEW SOUNDTRACK 23
BUT DREAMS COME TRUE
BLANK SPACE, WRITE YOUR NAME bar
IT'S A NEW SOUNDTRACK 12
BUT WE HAD TO END IT
JUST TAKE A DEEP BREATH AND LET IT GO
ARE YOU READY FOR IT? sayhello
SPEAK NOW OR FOREVER HOLD YOUR PEACE "Hello"
WE ARE NEVER EVER GETTING BACK TOGETHER
ALL TOO WELL TIME FLIES
"""

#"ARE YOU READY FOR IT?", variable_name, ZeroOrMore(statement), 'WE ARE NEVER EVER GETTING BACK TOGETHER'

#'IF THE HIGH WAS WORTH THE PAIN', operand, if_body, 'BUT WE HAD TO END IT'

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



