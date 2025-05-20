#########################################################################
# Intermediate Code Generator                                           #
# This part of the code generates intermediate code after lex           #
# and syntax analysis.                                                  #
#########################################################################

class IntermediateCodeGenerator:
    """
    Class to generate intermediate code in the form of quadruples.
    """
    def __init__(self):
        self.quads = []  # List to store the generated quadruples
        self.temp_counter = 0  # Counter for temporary variables
        self.next_quad = 0  # Starting quad number (can be adjusted)
        self.quad_increment = 1  # Increment value for quad numbers

    def next_quad_label(self):
        """Return the label of the next quadruple to be generated."""
        return self.next_quad

    def gen_quad(self, op, x, y, z):
        """Generate a new quadruple and add it to the list."""
        quad = (self.next_quad, op, x, y, z)
        self.quads.append(quad)
        self.next_quad += self.quad_increment  # Increment by 10 to allow for insertions if needed
        return self.next_quad - self.quad_increment  # Return the label of the generated quad

    def new_temp(self):
        """Generate a new temporary variable name."""
        temp = f"T_{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def empty_list(self):
        """Create an empty list of labels."""
        return []

    def make_list(self, x):
        """Create a list containing only the label x."""
        return [x]

    def merge(self, list1, list2):
        """Merge two lists into a new list."""
        return list1 + list2

    def backpatch(self, quad_list, z):
        """Complete the quadruples in the list with the label z."""
        for quad_label in quad_list:
            for i, quad in enumerate(self.quads):
                if quad[0] == quad_label:
                    # Replace the fourth element (destination) with z
                    self.quads[i] = (quad[0], quad[1], quad[2], quad[3], z)
                    break

    def quad_to_string(self, quad):
        label, op, arg1, arg2, result = quad
        max_label = max(self.quads, key=lambda q: q[0])[0] if self.quads else 0
        num_digits = len(str(max_label))
        formatted_label = f"{label:0{num_digits}d}"  # Format label with leading zeros
        return f"{formatted_label}: ({op}, {arg1}, {arg2}, {result})"

    def print_quads(self):
        """Print all generated quadruples in a readable format."""
        print("\nGenerated Quadruples:")
        for quad in self.quads:
            print(self.quad_to_string(quad))

    def get_quads(self):
        str_quads = ""
        for quad in self.quads:
            str_quads +=self.quad_to_string(quad) + "\n"
        return str_quads


class ExpressionProcessor:
    """
    Class to process expressions and generate intermediate code.
    It processes expressions, terms, and conditions based on the AST structure.
    """

    def __init__(self, code_gen):
        self.code_gen = code_gen

    def process_expression(self, expr_node):
        """Process an expression node based on the AST structure."""
        if expr_node['type'] == 'EXPRESSION':
            # Process children nodes
            #Example of object: {'type': 'PROGRAM', 'children': [{'type': 'IDENTIFIER', 'value': 'τεστ', 'line': 1},...]}
            if 'children' in expr_node and expr_node['children']:
                for child in expr_node['children']:
                    if child['type'] == 'BINARY_OPERATION':
                        return self.process_binary_operation(child)
                    elif child['type'] == 'TERM':
                        return self.process_term(child)
                    elif child['type'] == 'OPTIONAL_SIGN':
                        sign = self.process_sign(child)
                        term = self.process_term(expr_node['children'][1])
                        if sign == '-':
                            temp = self.code_gen.new_temp()
                            self.code_gen.gen_quad('-', '0', term, temp)
                            return temp
                        return term

        # Default case (unexpected structure)
        return None

    def process_sign(self, sign_node):
        """Process a sign node."""
        if 'children' in sign_node and sign_node['children']:
            for child in sign_node['children']:
                if child['type'] == 'ADD_OPERATOR':
                    return child['value']
        return '+'  # Default to positive if no sign found

    def process_binary_operation(self, op_node):
        """Process a binary operation node."""
        if 'value' not in op_node:
            return None

        op = op_node['value']
        left = None
        right = None

        # Extract the operands
        if 'children' in op_node and len(op_node['children']) >= 2:
            left = self.process_term(op_node['children'][0])
            right = self.process_term(op_node['children'][1])

        # Generate intermediate code for the operation
        if left and right:
            result = self.code_gen.new_temp()
            self.code_gen.gen_quad(op, left, right, result)
            return result

        return None

    def process_term(self, term_node):
        """Process a term node."""
        if term_node['type'] == 'TERM':
            if 'children' in term_node and term_node['children']:
                child = term_node['children'][0]

                if child['type'] == 'NUMBER':
                    return child['value']

                elif child['type'] == 'IDENTIFIER':
                    if 'children' in child and child['children']:
                        identifier_node = child['children'][0]

                        # Check if there's a function call (ID_TAIL)
                        if len(child['children']) > 1 and child['children'][1]['type'] == 'ID_TAIL':
                            func_name = identifier_node['value']
                            params = []

                            # Extract parameters
                            id_tail = child['children'][1]
                            if 'children' in id_tail and id_tail['children']:
                                actual_params = id_tail['children'][0]
                                if 'children' in actual_params and actual_params['children']:
                                    param_list = actual_params['children'][0]
                                    if 'children' in param_list:
                                        for param in param_list['children']:
                                            if param['type'] == 'VALUE_PARAMETER':
                                                param_expr = self.process_expression(param['children'][0])
                                                params.append(param_expr)

                            # Generate function call code
                            for param in params:
                                self.code_gen.gen_quad("par", param, "cv", "_")

                            result_place = self.code_gen.new_temp()
                            self.code_gen.gen_quad("par", result_place, "ret", "_")
                            self.code_gen.gen_quad("call", func_name, "_", "_")
                            return result_place

                        return identifier_node['value']

                elif child['type'] == 'BINARY_OPERATION':
                    return self.process_binary_operation(child)

                elif child['type'] == 'PARENTHESIZED_EXPRESSION':
                    if 'children' in child and child['children']:
                        return self.process_expression(child['children'][0])

        return None

    def process_condition(self, condition_node):
        """Process a condition node and returns true and false lists."""
        if condition_node['type'] == 'CONDITION':
            if 'children' in condition_node and condition_node['children']:
                # For simplicity, focusing on the first child (could be complex in reality)
                child = condition_node['children'][0]

                if child['type'] == 'BOOL_TERM':
                    return self.process_bool_term(child)
                elif child['type'] == 'OR_OPERATOR':
                    left_true, left_false = self.process_condition(child['children'][0])
                    right_true, right_false = self.process_condition(child['children'][1])
                    self.code_gen.backpatch(left_false, self.code_gen.next_quad_label())
                    return self.code_gen.merge(left_true, right_true), right_false

        # Default case
        return self.code_gen.empty_list(), self.code_gen.empty_list()

    def process_bool_term(self, bool_term_node):
        """Process a boolean term node."""
        if 'children' in bool_term_node and bool_term_node['children']:
            child = bool_term_node['children'][0]

            if child['type'] == 'COMPARISON':
                return self.process_comparison(child)
            elif child['type'] == 'AND_OPERATOR':
                left_true, left_false = self.process_bool_term(child['children'][0])
                self.code_gen.backpatch(left_true, self.code_gen.next_quad_label())
                right_true, right_false = self.process_bool_term(child['children'][1])
                return right_true, self.code_gen.merge(left_false, right_false)
            elif child['type'] == 'PARENTHESIZED_CONDITION':
                return self.process_condition(child['children'][0])

        # Default case
        return self.code_gen.empty_list(), self.code_gen.empty_list()

    def process_comparison(self, comparison_node):
        """Process a comparison node."""
        if 'children' in comparison_node and len(comparison_node['children']) >= 3:
            left_expr = self.process_expression(comparison_node['children'][0])
            op_node = comparison_node['children'][1]
            right_expr = self.process_expression(comparison_node['children'][2])

            if op_node['type'] == 'RELATIONAL_OPERATOR':
                op = op_node['value']
                true_list = self.code_gen.make_list(self.code_gen.gen_quad(op, left_expr, right_expr, "_"))
                false_list = self.code_gen.make_list(self.code_gen.gen_quad("jump", "_", "_", "_"))

                return true_list, false_list

        # Default case
        return self.code_gen.empty_list(), self.code_gen.empty_list()


class StatementProcessor:
    def __init__(self, code_gen, expr_processor):
        self.code_gen = code_gen
        self.expr_processor = expr_processor

    def process_sequence(self, sequence_node):
        """Process a sequence of statements."""
        if sequence_node['type'] == 'SEQUENCE' and 'children' in sequence_node:
            for stmt in sequence_node['children']:
                self.process_statement(stmt)

    def process_statement(self, stmt_node):
        """Process a statement based on its type."""
        if 'type' not in stmt_node:
            return

        stmt_type = stmt_node['type']

        if stmt_type == 'ASSIGNMENT':
            self.process_assignment(stmt_node)
        elif stmt_type == 'IF_STATEMENT':
            self.process_if_statement(stmt_node)
        elif stmt_type == 'WHILE_STATEMENT':
            self.process_while_statement(stmt_node)
        elif stmt_type == 'DO_WHILE_STATEMENT':
            self.process_do_while_statement(stmt_node)
        elif stmt_type == 'FOR_STATEMENT':
            self.process_for_statement(stmt_node)
        elif stmt_type == 'CALL_STATEMENT':
            self.process_call_statement(stmt_node)
        elif stmt_type == 'INPUT_STATEMENT':
            self.process_input_statement(stmt_node)
        elif stmt_type == 'PRINT_STATEMENT':
            self.process_print_statement(stmt_node)
        elif stmt_type == 'RETURN_STATEMENT':
            self.process_return_statement(stmt_node)
        elif stmt_type == 'SEQUENCE':
            self.process_sequence(stmt_node)

    def process_assignment(self, assignment_node):
        """Process an assignment statement."""
        if 'children' in assignment_node and len(assignment_node['children']) >= 2:
            identifier = assignment_node['children'][0]['value']
            expr_node = assignment_node['children'][1]
            expr_place = self.expr_processor.process_expression(expr_node)

            if expr_place:
                self.code_gen.gen_quad(":=", expr_place, "_", identifier)

    def process_if_statement(self, if_node):
        """Process an if statement."""
        if 'children' in if_node and len(if_node['children']) >= 2:
            condition_node = if_node['children'][0]
            then_block = if_node['children'][1]

            # Process condition
            true_list, false_list = self.expr_processor.process_condition(condition_node)

            # Backpatch true condition to execute 'then' part
            self.code_gen.backpatch(true_list, self.code_gen.next_quad_label())

            # Process 'then' statements
            if then_block['type'] == 'THEN_BLOCK' and 'children' in then_block:
                for child in then_block['children']:
                    self.process_statement(child)

            # Check if there's an 'else' block
            if len(if_node['children']) > 2:
                else_block = if_node['children'][2]

                # Generate jump for 'then' part to skip 'else' part
                if_end = self.code_gen.make_list(self.code_gen.gen_quad("jump", "_", "_", "_"))

                # Backpatch false condition to execute 'else' part
                self.code_gen.backpatch(false_list, self.code_gen.next_quad_label())

                # Process 'else' statements
                if else_block['type'] == 'ELSE_BLOCK' and 'children' in else_block:
                    for child in else_block['children']:
                        self.process_statement(child)

                # Backpatch end of 'then' to jump here (after 'else')
                self.code_gen.backpatch(if_end, self.code_gen.next_quad_label())
            else:
                # If no 'else', false condition jumps to the end
                self.code_gen.backpatch(false_list, self.code_gen.next_quad_label())

    def process_while_statement(self, while_node):
        """Process a while statement."""
        if 'children' in while_node and len(while_node['children']) >= 2:
            condition_node = while_node['children'][0]
            body = while_node['children'][1]

            # Remember the quad where condition evaluation begins
            cond_quad = self.code_gen.next_quad_label()

            # Process the condition
            true_list, false_list = self.expr_processor.process_condition(condition_node)

            # Backpatch true condition to execute loop body
            self.code_gen.backpatch(true_list, self.code_gen.next_quad_label())

            # Process loop body
            self.process_statement(body)

            # Generate jump back to condition
            self.code_gen.gen_quad("jump", "_", "_", cond_quad)

            # Backpatch false condition to exit loop
            self.code_gen.backpatch(false_list, self.code_gen.next_quad_label())

    def process_do_while_statement(self, do_while_node):
        """Process a repeat-until/do-while statement."""
        if 'children' in do_while_node and len(do_while_node['children']) >= 2:
            body = do_while_node['children'][0]
            condition_node = do_while_node['children'][1]

            # Remember the quad where the body starts
            body_quad = self.code_gen.next_quad_label()

            # Process the body
            self.process_statement(body)

            # Process the condition
            true_list, false_list = self.expr_processor.process_condition(condition_node)

            # If condition is false, jump back to body
            self.code_gen.backpatch(false_list, body_quad)

            # If condition is true, continue execution
            self.code_gen.backpatch(true_list, self.code_gen.next_quad_label())

    def process_for_statement(self, for_node):
        """Process a for statement."""
        if 'children' in for_node and len(for_node['children']) >= 5:
            counter_var = for_node['children'][0]['value']
            start_expr = for_node['children'][1]
            end_expr = for_node['children'][2]
            step_expr = for_node['children'][3]
            body = for_node['children'][4]

            # Initialize counter variable
            if 'children' in start_expr:
                start_value = self.expr_processor.process_expression(start_expr['children'][0])
                self.code_gen.gen_quad(":=", start_value, "_", counter_var)

            # Start of the loop
            loop_start = self.code_gen.next_quad_label()

            # Generate the condition check (counter <= end_value)
            if 'children' in end_expr:
                end_value = self.expr_processor.process_expression(end_expr['children'][0])
                condition_temp = self.code_gen.new_temp()
                self.code_gen.gen_quad("<=", counter_var, end_value, condition_temp)

                # If condition is false, exit loop
                exit_jump = self.code_gen.gen_quad("jumpz", condition_temp, "_", "_")

                # Process loop body
                self.process_statement(body)

                # Increment counter
                if 'children' in step_expr:
                    step_value = self.expr_processor.process_expression(step_expr['children'][0])
                    temp = self.code_gen.new_temp()
                    self.code_gen.gen_quad("+", counter_var, step_value, temp)
                    self.code_gen.gen_quad(":=", temp, "_", counter_var)

                # Jump back to condition check
                self.code_gen.gen_quad("jump", "_", "_", loop_start)

                # Next quad is the exit point
                self.code_gen.backpatch(self.code_gen.make_list(exit_jump), self.code_gen.next_quad_label())

    def process_call_statement(self, call_node):
        """Process a procedure call statement."""
        if 'children' in call_node and len(call_node['children']) >= 2:
            proc_name = call_node['children'][0]['value']
            params = []

            # Extract parameters
            id_tail = call_node['children'][1]
            if 'children' in id_tail and id_tail['children']:
                actual_params = id_tail['children'][0]
                if 'children' in actual_params and actual_params['children']:
                    param_list = actual_params['children'][0]
                    if 'children' in param_list:
                        for param in param_list['children']:
                            if param['type'] == 'VALUE_PARAMETER' and 'children' in param:
                                param_expr = self.expr_processor.process_expression(param['children'][0])
                                params.append(param_expr)

            # Generate procedure call code
            for param in params:
                self.code_gen.gen_quad("par", param, "cv", "_")

            self.code_gen.gen_quad("call", proc_name, "_", "_")

    def process_input_statement(self, input_node):
        """Process an input statement."""
        if 'children' in input_node and input_node['children']:
            var_node = input_node['children'][0]
            var_name = var_node['value']
            self.code_gen.gen_quad("in", "_", "_", var_name)

    def process_print_statement(self, print_node):
        """Process a print statement."""
        if 'children' in print_node and print_node['children']:
            expr_node = print_node['children'][0]
            expr_place = self.expr_processor.process_expression(expr_node)

            if expr_place:
                self.code_gen.gen_quad("out", expr_place, "_", "_")

    def process_return_statement(self, return_node):
        """Process a return statement."""
        if 'children' in return_node and return_node['children']:
            expr_node = return_node['children'][0]
            expr_place = self.expr_processor.process_expression(expr_node)

            if expr_place:
                self.code_gen.gen_quad("retv", expr_place, "_", "_")
            else:
                self.code_gen.gen_quad("ret", "_", "_", "_")


class ProgramProcessor:
    def __init__(self, code_gen, stmt_processor, symbol_table=None):
        self.code_gen = code_gen
        self.stmt_processor = stmt_processor
        self.symbol_table = symbol_table

    def process_program(self, ast):
        """Process a complete program AST."""
        if ast['type'] == 'PROGRAM':
            program_name = ast['children'][0]['value']
            program_block = ast['children'][1]

            # Get declarations, subprograms, and statements
            declarations_block = None
            subprograms_block = None
            statements_block = None

            if 'children' in program_block:
                for child in program_block['children']:
                    if child['type'] == 'DECLARATIONS':
                        declarations_block = child
                    elif child['type'] == 'SUBPROGRAMS':
                        subprograms_block = child
                    elif child['type'] == 'SEQUENCE':
                        statements_block = child

            # Generate program start
            self.code_gen.gen_quad("begin_block", program_name, "_", "_")

            # Process functions and procedures
            if subprograms_block and 'children' in subprograms_block:
                for subprogram in subprograms_block['children']:
                    if subprogram['type'] == 'FUNCTION':
                        self.process_function(subprogram)
                    elif subprogram['type'] == 'PROCEDURE':
                        self.process_procedure(subprogram)

            # Process statements in the main program
            if statements_block:
                self.stmt_processor.process_sequence(statements_block)

            # Generate program end
            self.code_gen.gen_quad("halt", "_", "_", "_")
            self.code_gen.gen_quad("end_block", program_name, "_", "_")

    def process_function(self, function_node):
        """Process a function."""
        if 'children' in function_node and len(function_node['children']) >= 3:
            function_name = function_node['children'][0]['value']
            block = function_node['children'][2]

            # Generate function start
            self.code_gen.gen_quad("begin_block", function_name, "_", "_")

            # Process function body
            if 'children' in block:
                for child in block['children']:
                    if child['type'] == 'SEQUENCE':
                        self.stmt_processor.process_sequence(child)

            # Generate function end
            self.code_gen.gen_quad("end_block", function_name, "_", "_")

    def process_procedure(self, procedure_node):
        """Process a procedure."""
        if 'children' in procedure_node and len(procedure_node['children']) >= 3:
            procedure_name = procedure_node['children'][0]['value']
            block = procedure_node['children'][2]

            # Generate procedure start
            self.code_gen.gen_quad("begin_block", procedure_name, "_", "_")

            # Process procedure body
            if 'children' in block:
                for child in block['children']:
                    if child['type'] == 'SEQUENCE':
                        self.stmt_processor.process_sequence(child)

            # Generate procedure end
            self.code_gen.gen_quad("end_block", procedure_name, "_", "_")


##################################################################################
# Function that uses the classes generated above to get the intermediate code    #
##################################################################################

def generate_intermediate_code(ast, symbol_table=None):
    """
    Generate intermediate code from an abstract syntax tree.

    Args:
        ast: The abstract syntax tree generated by the parser

    Returns:
        IntermediateCodeGenerator instance with the generated quads
        :param symbol_table: The symbol table that was generated
    """
    code_gen = IntermediateCodeGenerator()
    expr_processor = ExpressionProcessor(code_gen)
    stmt_processor = StatementProcessor(code_gen, expr_processor)
    program_processor = ProgramProcessor(code_gen, stmt_processor, symbol_table)
    # Process the AST and return the generated code
    program_processor.process_program(ast)
    return code_gen
