from intbase import InterpreterBase, ErrorType
from brewparse import parse_program

class Interpreter(InterpreterBase):
    
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.variables = {}

    def run(self, program):
        ast = parse_program(program)
        print(ast)
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
        
        if expression.elem_type == '+' or expression.elem_type == '-':
            op1, op2 = self.evaluate_expression(expression.dict['op1']), self.evaluate_expression(expression.dict['op2'])

            try:
                return op1 + op2 if expression.elem_type == '+' else op1 - op2
            except:
                super().error(
                    ErrorType.TYPE_ERROR,
                    "Incompatible types for arithmetic operation",
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
            
    def do_function_call_expression(self, expression):
        
        if expression.dict['name'] == 'inputi':
            if len(expression.dict['args']) > 1:
                super().error(
                    ErrorType.NAME_ERROR,
                    f"No inputi() function found that takes > 1 parameter",
                )
            prompt = self.evaluate_expression(expression.dict['args'][0]) if len(expression.dict['args']) == 1 else ""
            super().output(prompt)
            user_input = super().get_input()
            return int(user_input)
        else:
            super().error(ErrorType.NAME_ERROR,
                f"Unknown function reference {expression.dict['name']}")
        
    def do_function_call_statement(self, statement):
        
        if statement.dict['name'] == 'print':
            res = ""
            for expression in statement.dict['args']:
                res += str(self.evaluate_expression(expression))
            super().output(res)
        else:
            super().error(ErrorType.NAME_ERROR,
                f"Unknown function reference {statement.dict['name']}")



def main():
    program = 'func main(){a = 12 + inputi("input a number:" );print(a);}'
    interpreter = Interpreter()
    interpreter.run(program)
if __name__ == '__main__':
    main()