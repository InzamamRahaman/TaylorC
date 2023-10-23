from arpeggio import PTNodeVisitor

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
        return str(children[0])

    def visit_return_stmnt(self, node, children):
        return 'return ' + children[0]


    def visit_function_body(self, node, children):
        res = 'pass'
        if len(children) > 0:
            res = '\n'.join(map(lambda x: f'{x}', children))
        return res

    def visit_void_function(self, node, children):
        function_name = children[0]
        header = f'def {function_name}():\n'
        body = '    pass'
        if len(children) > 1:
            processed_children = map(lambda x: x.split('\n'), children[1:])
            processed_children = [item for sublist in processed_children for item in sublist]
            #print(processed_children)
            body = map(lambda x: f'    {x}', processed_children)
            body = '\n'.join(body)
        func_def = f'{header}\n{body}'
        return func_def


    def visit_non_void_function(self, node, children):
        argument_listing = children[1]
        function_name = children[0]
        header = f'def {function_name}({argument_listing}):\n'
        body = '    pass'
        if len(children) > 2:
            processed_children = map(lambda x: x.split('\n'), children[2:])
            processed_children = [item for sublist in processed_children for item in sublist]
            body = map(lambda x: f'    {x}', processed_children)
            body = '\n'.join(body)
        func_def = f'{header}\n{body}'
        return func_def

    def visit_function_invoke(self, node, children):
        arguments = []
        if len(children) > 1:
            for child in children[1:]:
                arguments.append(child)
        res = f'{children[0]}({",".join(arguments)})'
        return res

    def visit_function_invoke_with_return(self, node, children):
        arguments = []
        if len(children) > 2:
            for child in children[1:-1]:
                arguments.append(child)
        res = f'{children[-1]} = {children[0]}({",".join(arguments)})'
        return res