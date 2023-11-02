from intbase import InterpreterBase, ErrorType
from brewparse import parse_program

class Interpreter(InterpreterBase):
    
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.variables = {}

    def run(self, program):
        ast = parse_program(program)
        main_function = self.get_main_function(ast)
        self.run_func(main_function)

    def get_main_function(self, ast):
        for function in ast.dict['functions']:
            if function.dict['name'] == 'main':
                return function
        
        super().error(
            ErrorType.NAME_ERROR,
            "No main() function was found",
        )

    def run_func(self, function):
        for statement in function.dict['statements']:
            self.run_statement(statement)

    def run_statement(self, statement):
        if statement.elem_type == '=':
            self.do_assignment(statement)
        elif statement.elem_type == 'fcall':
            self.do_function_call_statement(statement)
    
    def do_assignment(self, statement):
        
        expression = statement.dict['expression']
        result = self.evaluate_expression(expression)
        
        self.variables[statement.dict['name']] = result

    def evaluate_expression(self, expression):
        binaryOps = ['+', '-', '*', '/','==', '<', '<=', '>', '>=', '!=', '||', '&&']
        unaryOps = ['neg', '!']
        intAndint = False
        boolAndbool = False
        stringAndstring = False
        if expression.elem_type in binaryOps:
            op1, op2 = self.evaluate_expression(expression.dict['op1']), self.evaluate_expression(expression.dict['op2'])

            # Determine types of operands
            if type(op1) == int and type(op2) == int:
                intAndint = True
            elif type(op1) == bool and type(op2) == bool:
                boolAndbool = True
            elif type(op1) == str and type(op2) == str:
                stringAndstring = True

            # perform operations
            if expression.elem_type == '==':
                if type(op1) == type(op2) and op1 is not None:
                    return op1 == op2
                else:
                    return False
                
            if expression.elem_type == '!=':
                if type(op1) == type(op2) and op1 is not None:
                    return op1 != op2
                else:
                    return True
            
            if expression.elem_type == '+' and (intAndint or stringAndstring):
                return op1 + op2
            elif intAndint:
                if expression.elem_type == '-':
                    return op1 - op2
                elif expression.elem_type == '*':
                    return op1 * op2
                elif expression.elem_type == '/':
                    return op1 // op2
                elif expression.elem_type == '<':
                    return op1 < op2
                elif expression.elem_type == '<=':
                    return op1 <= op2
                elif expression.elem_type == '>':
                    return op1 > op2
                elif expression.elem_type == '>=':
                    return op1 >= op2
            elif boolAndbool:
                if expression.elem_type == '||':
                    return op1 or op2
                elif expression.elem_type == '&&':
                    return op1 and op2
            
            super().error(
                ErrorType.TYPE_ERROR,
                "Incompatible types for arithmetic operation",
            )

        elif expression.elem_type in unaryOps:
            op1 = self.evaluate_expression(expression.dict['op1'])

            if expression.elem_type == 'neg' and type(op1) == int:
                return -1 * op1
            elif expression.elem_type == '!' and type(op1) == bool:
                return not op1
            super().error(
                ErrorType.TYPE_ERROR,
                "Incompatible types for unary operation",
            )
        elif expression.elem_type == 'fcall':
            return self.do_function_call_expression(expression)
        
        elif expression.elem_type == 'var':
            try:
                return self.variables[expression.dict['name']]
            except:
                super().error(
                    ErrorType.NAME_ERROR,
                    f"Variable {expression.dict['name']} has not been defined",
                )
        elif expression.elem_type == 'int':
            return expression.dict['val']
        
        elif expression.elem_type == 'string':
            return expression.dict['val']
        elif expression.elem_type == 'bool':
            return expression.dict['val']
        elif expression.elem_type == 'nil':
            return None
    def do_function_call_expression(self, expression):
        
        if expression.dict['name'] == 'inputi':
            if len(expression.dict['args']) > 1:
                super().error(
                    ErrorType.NAME_ERROR,
                    f"No inputi() function found that takes > 1 parameter",
                )
            prompt = str(self.evaluate_expression(expression.dict['args'][0])) if len(expression.dict['args']) == 1 else ""
            if prompt:
                super().output(prompt)
            user_input = super().get_input()
            return int(user_input)

        if expression.dict['name'] == 'inputs':
            if len(expression.dict['args']) > 1:
                super().error(
                    ErrorType.NAME_ERROR,
                    f"No inputs() function found that takes > 1 parameter",
                )
            prompt = str(self.evaluate_expression(expression.dict['args'][0])) if len(expression.dict['args']) == 1 else ""
            if prompt:
                super().output(prompt)
            user_input = super().get_input()
            return str(user_input)

        if expression.dict['name'] == 'print':
            res = ""
            for expression in expression.dict['args']:
                expression_res = self.evaluate_expression(expression)
                if type(expression_res) == bool:
                    expression_res = 'true' if expression_res else 'false'
                res += str(expression_res)
            super().output(res)
        
        super().error(ErrorType.NAME_ERROR,
            f"Unknown function reference {expression.dict['name']}")
        
    def do_function_call_statement(self, statement):
        
        if statement.dict['name'] == 'print':
            res = ""
            for expression in statement.dict['args']:
                expression_res = self.evaluate_expression(expression)

                if type(expression_res) == bool:
                    expression_res = 'true' if expression_res else 'false'
                if expression_res is None:
                    expression_res = 'nil'
                res += str(expression_res)
            super().output(res)
        else:
            super().error(ErrorType.NAME_ERROR,
                f"Unknown function reference {statement.dict['name']}")



def main():
    program = 'func main() {a = nil; b = nil; print(a == b);}'
    interpreter = Interpreter()
    interpreter.run(program)
if __name__ == '__main__':
    main()