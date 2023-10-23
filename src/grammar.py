from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF
from arpeggio import RegExMatch as _


def start(): return "ARE WE OUT OF THE WOODS"
def end(): return "ALL TOO WELL TIME FLIES", EOF
def variable_name(): return _(r'[a-z][a-zA-Z0-9]*')
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

def statement(): return [print_statement, variable_creation,
                         variable_assignment, if_stmnt, if_else_stmnt,
                         while_block, function_invoke_with_return, function_invoke]
def return_stmnt():
    return "I'LL COME BACK STRONGER THAN A 90'S TREND", [variable_name, literal]

def function_body():
    return ZeroOrMore(statement)

def void_function():
    return "ARE YOU READY FOR IT?", variable_name, function_body, \
        Optional(return_stmnt), 'WE ARE NEVER EVER GETTING BACK TOGETHER'

def non_void_function():
    return "ARE YOU READY FOR IT?", variable_name, argument_list, function_body, \
        return_stmnt, 'WE ARE NEVER EVER GETTING BACK TOGETHER'

def function():
    return [non_void_function, void_function]

def body_elems():
    return [statement, function]

def function_invoke():
    return 'JUST SAY YES', variable_name, ZeroOrMore([variable_name, literal])

def function_invoke_with_return():
    return 'JUST SAY YES', variable_name, ZeroOrMore([variable_name, literal]), \
        'EVERYTHING HAS CHANGED', variable_name

def body(): return [ZeroOrMore(body_elems), '']

def program(): return start, body, end






