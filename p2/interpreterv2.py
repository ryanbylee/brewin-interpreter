from intbase import InterpreterBase, ErrorType
from brewparse import parse_program

class Interpreter(InterpreterBase):
    
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.functions = {}

    def run(self, program):
        ast = parse_program(program)
        self.define_functions(ast)
        main_function = self.get_main_function(ast)
        self.run_func(main_function, {})

    def define_functions(self, ast):
        for function in ast.dict['functions']:
            func_structure = {}
            func_structure['args'] = function.dict['args']
            func_structure['statements'] = function.dict['statements']
            self.functions[function.dict['name'] + str(len(function.dict['args']))] = func_structure

    
    def get_main_function(self, ast):
        for function in ast.dict['functions']:
            if function.dict['name'] == 'main':
                return function
        
        super().error(
            ErrorType.NAME_ERROR,
            "No main() function was found",
        )

    def run_func(self, function, variables):
        in_scope_variables = variables.copy()
        
        if function.dict['name'] == 'inputi':
            if len(function.dict['args']) > 1:
                super().error(
                    ErrorType.NAME_ERROR,
                    f"No inputi() function found that takes > 1 parameter",
                )
            prompt = str(self.evaluate_expression(function.dict['args'][0], in_scope_variables)) if len(function.dict['args']) == 1 else ""
            if prompt:
                super().output(prompt)
            user_input = super().get_input()
            return int(user_input)

        if function.dict['name'] == 'inputs':
            if len(function.dict['args']) > 1:
                super().error(
                    ErrorType.NAME_ERROR,
                    f"No inputs() function found that takes > 1 parameter",
                )
            prompt = str(self.evaluate_expression(function.dict['args'][0], in_scope_variables)) if len(function.dict['args']) == 1 else ""
            if prompt:
                super().output(prompt)
            user_input = super().get_input()
            return str(user_input)

        if function.dict['name'] == 'print':
            res = ""
            for expression in function.dict['args']:
                expression_res = self.evaluate_expression(expression, in_scope_variables)
                if type(expression_res) == bool:
                    expression_res = 'true' if expression_res else 'false'
                res += str(expression_res)
            super().output(res)
            return None
        
        if function.dict['name'] + str(len(function.dict['args'])) in self.functions:

            
            # number of argument check
            if len(function.dict['args']) != len(self.functions[function.dict['name'] + str(len(function.dict['args']))]['args']):
                super().error(ErrorType.NAME_ERROR,
                    f"Unknown function reference {function.dict['name']}")
            if len(function.dict['args']) > 0:
                for i in range(len(function.dict['args'])):
                    in_scope_variables[self.functions[function.dict['name'] + str(len(function.dict['args']))]['args'][i].dict['name']] = self.evaluate_expression(function.dict['args'][i], variables)
                    # print("storing value of: ", self.evaluate_expression(function.dict['args'][i], variables), "into key of: ", self.functions[function.dict['name'] + str(len(function.dict['args']))]['args'][i].dict['name'])
                    # print('\nin_scope_variable for function ', function.dict['name'], ": ", in_scope_variables)
            func_return_val = None
            for statement_inside in self.functions[function.dict['name'] + str(len(function.dict['args']))]['statements']:
                func_return_val = self.run_statement(statement_inside, in_scope_variables)
                if func_return_val is not None:
                    return func_return_val
                    
            return func_return_val
        
        super().error(ErrorType.NAME_ERROR,
            f"Unknown function reference {function.dict['name']}")

    def run_statement(self, statement, variables):
        # print('variables: ', variables)
        if statement.elem_type == '=':
            self.do_assignment(statement, variables)
        elif statement.elem_type == 'fcall':
            self.run_func(statement, variables)
        elif statement.elem_type == 'if':
            condition = self.evaluate_expression(statement.dict['condition'], variables)
            # print('condition:', statement.dict['condition'])
            if type(condition) != bool:
                super().error(
                    ErrorType.TYPE_ERROR,
                    "Incompatible types for if statement condition",
                )
            if condition:
                for statement_inside in statement.dict['statements']:
                    if_return_val = self.run_statement(statement_inside, variables)
                    if if_return_val is not None:
                        return if_return_val
            elif statement.dict['else_statements'] is not None:
                for statement_inside in statement.dict['else_statements']:
                    if_return_val = self.run_statement(statement_inside, variables)
                    if if_return_val is not None:
                        # print('returning:', if_return_val)
                        return if_return_val
        elif statement.elem_type == 'while':
            condition = self.evaluate_expression(statement.dict['condition'], variables)
            if type(condition) != bool:
                super().error(
                    ErrorType.TYPE_ERROR,
                    "Incompatible types for while loop condition",
            )
            while self.evaluate_expression(statement.dict['condition'], variables):
                condition = self.evaluate_expression(statement.dict['condition'], variables)
                if type(condition) != bool:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        "Incompatible types for while loop condition",
                )
                for statement_inside in statement.dict['statements']:
                    loop_return_val = self.run_statement(statement_inside, variables)
                    if loop_return_val is not None:
                        return loop_return_val
            
        elif statement.elem_type == 'return':
            # print('return expression:', statement.dict['expression'])
            return self.evaluate_expression(statement.dict['expression'], variables)
        return None
    def do_assignment(self, statement, variables):
        
        expression = statement.dict['expression']
        result = self.evaluate_expression(expression, variables)
        
        variables[statement.dict['name']] = result

    def evaluate_expression(self, expression, variables):
        binaryOps = ['+', '-', '*', '/','==', '<', '<=', '>', '>=', '!=', '||', '&&']
        unaryOps = ['neg', '!']
        intAndint = False
        boolAndbool = False
        stringAndstring = False
        if expression is None:
            return None
        elif expression.elem_type in binaryOps:
            op1, op2 = self.evaluate_expression(expression.dict['op1'], variables), self.evaluate_expression(expression.dict['op2'], variables)
            # Determine types of operands
            if type(op1) == int and type(op2) == int:
                intAndint = True
            elif type(op1) == bool and type(op2) == bool:
                boolAndbool = True
            elif type(op1) == str and type(op2) == str:
                stringAndstring = True

            # perform operations
            if expression.elem_type == '==':
                if type(op1) == type(op2):
                    return op1 == op2
                else:
                    return False
                
            if expression.elem_type == '!=':
                if type(op1) == type(op2):
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
            op1 = self.evaluate_expression(expression.dict['op1'], variables)

            if expression.elem_type == 'neg' and type(op1) == int:
                return -1 * op1
            elif expression.elem_type == '!' and type(op1) == bool:
                return not op1
            super().error(
                ErrorType.TYPE_ERROR,
                "Incompatible types for unary operation",
            )
        elif expression.elem_type == 'fcall':
            return self.run_func(expression, variables)
        
        elif expression.elem_type == 'var':
            try:
                return variables[expression.dict['name']]
            except:
                super().error(
                    ErrorType.NAME_ERROR,
                    f"Variable {expression.dict['name']} has not been defined",
                )
        primitive_types = ('int', 'string', 'bool')
        if expression.elem_type in primitive_types:
            return expression.dict['val']
        
        # nil type
        return None

def main():
    program = 'func foo() {i = 0;while (i < 3) {j = 0;while (j < 3) {k = 0;while (k < 3) {if (i * j * k == 1) {return ans;} else {ans = ans + 1;k = k + 1;}}j = j + 1;}i = i + 1;}}func main() {ans = 0;print(foo());print(ans);}'
    interpreter = Interpreter()
    interpreter.run(program)
if __name__ == '__main__':
    main()