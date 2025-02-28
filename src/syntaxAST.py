#################################################################################################################
# This part of the code contains the Syntax class that implements the syntax analyzer of the language.          #
# The syntax analyzer checks if the program provided by the lexical analyzer is syntactically correct.          #
# If the program is syntactically correct, it displays the message "Parsing completed successfully."            #
# If the program is not syntactically correct, it displays the message "Parsing failed: {error_message}"        #
# Finally, the parse method returns True if the program is syntactically correct, otherwise it returns False.   #
#################################################################################################################

from lexer import TokenType


class ASTNode:
    def __init__(self, node_type, children=None, value=None, line=None):
        self.type = node_type
        self.children = children if children is not None else []
        self.value = value
        self.line = line

    def add_child(self, child):
        self.children.append(child)

    def to_dict(self):
        result = {'type': self.type}
        if self.value is not None:
            result['value'] = self.value
        if self.line is not None:
            result['line'] = self.line
        if self.children:
            result['children'] = [child.to_dict() for child in self.children]
        return result


class Syntax:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.errors = []
        self.ast = None

    def error(self, message):
        _, token_value, line = self.current_token
        error_msg = f"Error at line {line}: {message}, got '{token_value}'"
        self.errors.append(error_msg)
        print(error_msg)
        raise SyntaxError(error_msg)

    def advance(self):
        self.current_token_index += 1
        # ignore comments
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][
            0] == TokenType.COMMENT:
            self.current_token_index += 1

        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        return self.current_token

    def eat(self, token_type=None, token_value=None):
        current_token = self.current_token
        if token_type and self.current_token[0] != token_type:
            self.error(f"Expected token type {token_type}")
        elif token_value and self.current_token[1] != token_value:
            self.error(f"Expected '{token_value}' got '{self.current_token[0]}'")
        else:
            self.advance()
            return current_token

    def parse(self):
        return self.program()

    # Κανόνες γραμματικής

    def program(self):
        """program : 'πρόγραμμα' ID programblock"""
        node = ASTNode('PROGRAM')

        # Eat πρόγραμμα token
        program_token = self.eat(token_value='πρόγραμμα')

        # Get program name (ID)
        id_token = self.eat(TokenType.IDENTIFIER)
        id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
        node.add_child(id_node)

        # Parse program block
        program_block = self.programblock()
        node.add_child(program_block)

        return node

    def programblock(self):
        """programblock : declarations subprograms 'αρχή_προγράμματος' sequence 'τέλος_προγράμματος'"""
        node = ASTNode('PROGRAM_BLOCK')

        # Parse declarations
        declarations_node = self.declarations()
        node.add_child(declarations_node)

        # Parse subprograms
        subprograms_node = self.subprograms()
        node.add_child(subprograms_node)

        # Eat αρχή_προγράμματος token
        self.eat(token_value='αρχή_προγράμματος')

        # Parse sequence
        sequence_node = self.sequence()
        node.add_child(sequence_node)

        # Eat τέλος_προγράμματος token
        self.eat(token_value='τέλος_προγράμματος')

        return node

    def declarations(self):
        """declarations : ('δήλωση' varlist)* | """
        node = ASTNode('DECLARATIONS')

        while self.current_token[1] == 'δήλωση':
            self.eat(token_value='δήλωση')
            varlist_node = self.varlist()
            node.add_child(varlist_node)

        return node

    def varlist(self):
        """varlist : ID (',' ID)*"""
        node = ASTNode('VAR_LIST')

        # Add first ID
        id_token = self.eat(TokenType.IDENTIFIER)
        id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
        node.add_child(id_node)

        # Add remaining IDs if any
        while self.current_token[1] == ',':
            self.eat(token_value=',')
            id_token = self.eat(TokenType.IDENTIFIER)
            id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
            node.add_child(id_node)

        return node

    def subprograms(self):
        """subprograms : (func | proc)*"""
        node = ASTNode('SUBPROGRAMS')

        while self.current_token[1] in ['συνάρτηση', 'διαδικασία']:
            if self.current_token[1] == 'συνάρτηση':
                func_node = self.func()
                node.add_child(func_node)
            else:
                proc_node = self.proc()
                node.add_child(proc_node)

        return node

    def func(self):
        """func : 'συνάρτηση' ID '(' formalparlist ')' funcblock"""
        node = ASTNode('FUNCTION')

        # Eat συνάρτηση token
        self.eat(token_value='συνάρτηση')

        # Get function name (ID)
        id_token = self.eat(TokenType.IDENTIFIER)
        id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
        node.add_child(id_node)

        # Eat '('
        self.eat(token_value='(')

        # Parse formal parameter list
        params_node = self.formalparlist()
        node.add_child(params_node)

        # Eat ')'
        self.eat(token_value=')')

        # Parse function block
        func_block = self.funcblock()
        node.add_child(func_block)

        return node

    def proc(self):
        """proc : 'διαδικασία' ID '(' formalparlist ')' procblock"""
        node = ASTNode('PROCEDURE')

        # Eat διαδικασία token
        self.eat(token_value='διαδικασία')

        # Get procedure name (ID)
        id_token = self.eat(TokenType.IDENTIFIER)
        id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
        node.add_child(id_node)

        # Eat '('
        self.eat(token_value='(')

        # Parse formal parameter list
        params_node = self.formalparlist()
        node.add_child(params_node)

        # Eat ')'
        self.eat(token_value=')')

        # Parse procedure block
        proc_block = self.procblock()
        node.add_child(proc_block)

        return node

    def formalparlist(self):
        """formalparlist : varlist | """
        node = ASTNode('FORMAL_PARAMETERS')

        if self.current_token[0] == TokenType.IDENTIFIER:
            varlist_node = self.varlist()
            node.add_child(varlist_node)

        return node

    def funcblock(self):
        """funcblock : 'διαπροσωπεία' funcinput funcoutput declarations subprograms
         'αρχή_συνάρτησης' sequence 'τέλος_συνάρτησης'"""
        node = ASTNode('FUNCTION_BLOCK')

        # Eat διαπροσωπεία token
        self.eat(token_value='διαπροσωπεία')

        # Parse function input
        input_node = self.funcinput()
        node.add_child(input_node)

        # Parse function output
        output_node = self.funcoutput()
        node.add_child(output_node)

        # Parse declarations
        declarations_node = self.declarations()
        node.add_child(declarations_node)

        # Parse subprograms
        subprograms_node = self.subprograms()
        node.add_child(subprograms_node)

        # Eat αρχή_συνάρτησης token
        self.eat(token_value='αρχή_συνάρτησης')

        # Parse sequence
        sequence_node = self.sequence()
        node.add_child(sequence_node)

        # Eat τέλος_συνάρτησης token
        self.eat(token_value='τέλος_συνάρτησης')

        return node

    def procblock(self):
        """procblock : 'διαπροσωπεία' funcinput funcoutput declarations subprograms
         'αρχή_διαδικασίας' sequence 'τέλος_διαδικασίας'"""
        node = ASTNode('PROCEDURE_BLOCK')

        # Eat διαπροσωπεία token
        self.eat(token_value='διαπροσωπεία')

        # Parse function input
        input_node = self.funcinput()
        node.add_child(input_node)

        # Parse function output
        output_node = self.funcoutput()
        node.add_child(output_node)

        # Parse declarations
        declarations_node = self.declarations()
        node.add_child(declarations_node)

        # Parse subprograms
        subprograms_node = self.subprograms()
        node.add_child(subprograms_node)

        # Eat αρχή_διαδικασίας token
        self.eat(token_value='αρχή_διαδικασίας')

        # Parse sequence
        sequence_node = self.sequence()
        node.add_child(sequence_node)

        # Eat τέλος_διαδικασίας token
        self.eat(token_value='τέλος_διαδικασίας')

        return node

    def funcinput(self):
        """funcinput : 'είσοδος' varlist | """
        node = ASTNode('FUNCTION_INPUT')

        if self.current_token[1] == 'είσοδος':
            self.eat(token_value='είσοδος')
            varlist_node = self.varlist()
            node.add_child(varlist_node)

        return node

    def funcoutput(self):
        """funcoutput : 'έξοδος' varlist | """
        node = ASTNode('FUNCTION_OUTPUT')

        if self.current_token[1] == 'έξοδος':
            self.eat(token_value='έξοδος')
            varlist_node = self.varlist()
            node.add_child(varlist_node)

        return node

    def sequence(self):
        """sequence : statement (';' statement)*"""
        node = ASTNode('SEQUENCE')

        # Parse first statement
        statement_node = self.statement()
        node.add_child(statement_node)

        # Parse remaining statements
        while self.current_token[1] == ';':
            self.eat(token_value=';')
            # Check if we've reached the end of the sequence
            if self.current_token[1] in ['τέλος_προγράμματος', 'τέλος_συνάρτησης', 'τέλος_διαδικασίας',
                                         'αλλιώς', 'εάν_τέλος', 'όσο_τέλος', 'για_τέλος', 'μέχρι']:
                break
            statement_node = self.statement()
            node.add_child(statement_node)

        return node

    def statement(self):
        """
        statement : assignment_stat
                 | if_stat
                 | while_stat
                 | do_stat
                 | for_stat
                 | input_stat
                 | print_stat
                 | call_stat
        """
        if self.current_token[0] == TokenType.IDENTIFIER:
            return self.assignment_stat()
        elif self.current_token[1] == 'εάν':
            return self.if_stat()
        elif self.current_token[1] == 'όσο':
            return self.while_stat()
        elif self.current_token[1] == 'επανάλαβε':
            return self.do_stat()
        elif self.current_token[1] == 'για':
            return self.for_stat()
        elif self.current_token[1] == 'διάβασε':
            return self.input_stat()
        elif self.current_token[1] == 'γράψε':
            return self.print_stat()
        elif self.current_token[1] == 'εκτέλεσε':
            return self.call_stat()
        else:
            self.error(f"Expected statement")

    def assignment_stat(self):
        """assignment_stat : ID ':=' expression"""
        node = ASTNode('ASSIGNMENT')

        # Get identifier
        id_token = self.eat(TokenType.IDENTIFIER)
        id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
        node.add_child(id_node)

        # Eat ':=' token
        self.eat(token_value=':=')

        # Parse expression
        expr_node = self.expression()
        node.add_child(expr_node)

        return node

    def if_stat(self):
        """if_stat : 'εάν' condition 'τότε' sequence elsepart 'εάν_τέλος'"""
        node = ASTNode('IF_STATEMENT')

        # Eat εάν token
        self.eat(token_value='εάν')

        # Parse condition
        condition_node = self.condition()
        node.add_child(condition_node)

        # Eat τότε token
        self.eat(token_value='τότε')

        # Parse then-sequence
        then_node = self.sequence()
        then_block = ASTNode('THEN_BLOCK')
        then_block.add_child(then_node)
        node.add_child(then_block)

        # Parse else-part
        else_node = self.elsepart()
        node.add_child(else_node)

        # Eat εάν_τέλος token
        self.eat(token_value='εάν_τέλος')

        return node

    def elsepart(self):
        """elsepart : 'αλλιώς' sequence | """
        node = ASTNode('ELSE_BLOCK')

        if self.current_token[1] == 'αλλιώς':
            self.eat(token_value='αλλιώς')
            sequence_node = self.sequence()
            node.add_child(sequence_node)

        return node

    def while_stat(self):
        """while_stat : 'όσο' condition 'επανάλαβε' sequence 'όσο_τέλος'"""
        node = ASTNode('WHILE_STATEMENT')

        # Eat όσο token
        self.eat(token_value='όσο')

        # Parse condition
        condition_node = self.condition()
        node.add_child(condition_node)

        # Eat επανάλαβε token
        self.eat(token_value='επανάλαβε')

        # Parse sequence
        sequence_node = self.sequence()
        node.add_child(sequence_node)

        # Eat όσο_τέλος token
        self.eat(token_value='όσο_τέλος')

        return node

    def do_stat(self):
        """do_stat : 'επανάλαβε' sequence 'μέχρι' condition"""
        node = ASTNode('DO_WHILE_STATEMENT')

        # Eat επανάλαβε token
        self.eat(token_value='επανάλαβε')

        # Parse sequence
        sequence_node = self.sequence()
        node.add_child(sequence_node)

        # Eat μέχρι token
        self.eat(token_value='μέχρι')

        # Parse condition
        condition_node = self.condition()
        node.add_child(condition_node)

        return node

    def for_stat(self):
        """for_stat : 'για' ID ':=' expression 'έως' expression step 'επανάλαβε' sequence 'για_τέλος'"""
        node = ASTNode('FOR_STATEMENT')

        # Eat για token
        self.eat(token_value='για')

        # Get counter variable (ID)
        id_token = self.eat(TokenType.IDENTIFIER)
        id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
        node.add_child(id_node)

        # Eat ':=' token
        self.eat(token_value=':=')

        # Parse start expression
        start_expr = self.expression()
        start_node = ASTNode('START_EXPRESSION')
        start_node.add_child(start_expr)
        node.add_child(start_node)

        # Eat έως token
        self.eat(token_value='έως')

        # Parse end expression
        end_expr = self.expression()
        end_node = ASTNode('END_EXPRESSION')
        end_node.add_child(end_expr)
        node.add_child(end_node)

        # Parse step (if any)
        step_node = self.step()
        node.add_child(step_node)

        # Eat επανάλαβε token
        self.eat(token_value='επανάλαβε')

        # Parse sequence
        sequence_node = self.sequence()
        node.add_child(sequence_node)

        # Eat για_τέλος token
        self.eat(token_value='για_τέλος')

        return node

    def step(self):
        """step : 'με_βήμα' expression | """
        node = ASTNode('STEP')

        if self.current_token[1] == 'με_βήμα':
            self.eat(token_value='με_βήμα')
            expr_node = self.expression()
            node.add_child(expr_node)

        return node

    def print_stat(self):
        """print_stat : 'γράψε' expression"""
        node = ASTNode('PRINT_STATEMENT')

        # Eat γράψε token
        self.eat(token_value='γράψε')

        # Parse expression
        expr_node = self.expression()
        node.add_child(expr_node)

        return node

    def input_stat(self):
        """input_stat : 'διάβασε' ID"""
        node = ASTNode('INPUT_STATEMENT')

        # Eat διάβασε token
        self.eat(token_value='διάβασε')

        # Get identifier
        id_token = self.eat(TokenType.IDENTIFIER)
        id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
        node.add_child(id_node)

        return node

    def call_stat(self):
        """call_stat : 'εκτέλεσε' ID idtail"""
        node = ASTNode('CALL_STATEMENT')

        # Eat εκτέλεσε token
        self.eat(token_value='εκτέλεσε')

        # Get procedure/function name (ID)
        id_token = self.eat(TokenType.IDENTIFIER)
        id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
        node.add_child(id_node)

        # Parse parameters (if any)
        idtail_node = self.idtail()
        node.add_child(idtail_node)

        return node

    def idtail(self):
        """idtail : actualpars | """
        node = ASTNode('ID_TAIL')

        if self.current_token[1] == '(':
            actualpars_node = self.actualpars()
            node.add_child(actualpars_node)

        return node

    def actualpars(self):
        """actualpars : '(' actualparlist ')'"""
        node = ASTNode('ACTUAL_PARAMETERS')

        # Eat '(' token
        self.eat(token_value='(')

        # Parse parameter list
        actualparlist_node = self.actualparlist()
        node.add_child(actualparlist_node)

        # Eat ')' token
        self.eat(token_value=')')

        return node

    def actualparlist(self):
        """actualparlist : actualparitem (',' actualparitem)* | """
        node = ASTNode('ACTUAL_PARAMETER_LIST')

        if self.current_token[1] != ')':
            # Parse first parameter
            param_node = self.actualparitem()
            node.add_child(param_node)

            # Parse remaining parameters
            while self.current_token[1] == ',':
                self.eat(token_value=',')
                param_node = self.actualparitem()
                node.add_child(param_node)

        return node

    def actualparitem(self):
        """actualparitem : expression | '%' ID"""
        if self.current_token[1] == '%':
            node = ASTNode('REFERENCE_PARAMETER')

            # Eat '%' token
            self.eat(token_value='%')

            # Get identifier
            id_token = self.eat(TokenType.IDENTIFIER)
            id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
            node.add_child(id_node)
        else:
            node = ASTNode('VALUE_PARAMETER')

            # Parse expression
            expr_node = self.expression()
            node.add_child(expr_node)

        return node

    def condition(self):
        """condition : boolterm ('ή' boolterm)*"""
        node = ASTNode('CONDITION')

        # Parse first boolean term
        boolterm_node = self.boolterm()
        node.add_child(boolterm_node)

        # Parse remaining boolean terms (if any)
        while self.current_token[1] == 'ή':
            or_node = ASTNode('OR_OPERATOR', value='ή')

            # Eat 'ή' token
            self.eat(token_value='ή')

            # Parse boolean term
            boolterm_node = self.boolterm()

            # Add both to or_node
            or_node.add_child(node.children.pop())  # Remove last child from condition node
            or_node.add_child(boolterm_node)

            # Add or_node to condition node
            node.add_child(or_node)

        return node

    def boolterm(self):
        """boolterm : boolfactor ('και' boolfactor)*"""
        node = ASTNode('BOOL_TERM')

        # Parse first boolean factor
        boolfactor_node = self.boolfactor()
        node.add_child(boolfactor_node)

        # Parse remaining boolean factors (if any)
        while self.current_token[1] == 'και':
            and_node = ASTNode('AND_OPERATOR', value='και')

            # Eat 'και' token
            self.eat(token_value='και')

            # Parse boolean factor
            boolfactor_node = self.boolfactor()

            # Add both to and_node
            and_node.add_child(node.children.pop())  # Remove last child from bool_term node
            and_node.add_child(boolfactor_node)

            # Add and_node to bool_term node
            node.add_child(and_node)

        return node

    def boolfactor(self):
        """
        boolfactor : 'όχι' '[' condition ']'
                   | '[' condition ']'
                   | expression relational_oper expression
        """
        if self.current_token[1] == 'όχι':
            node = ASTNode('NOT_FACTOR')

            # Eat 'όχι' token
            self.eat(token_value='όχι')

            # Eat '[' token
            self.eat(token_value='[')

            # Parse condition
            condition_node = self.condition()
            node.add_child(condition_node)

            # Eat ']' token
            self.eat(token_value=']')

        elif self.current_token[1] == '[':
            node = ASTNode('PARENTHESIZED_CONDITION')

            # Eat '[' token
            self.eat(token_value='[')

            # Parse condition
            condition_node = self.condition()
            node.add_child(condition_node)

            # Eat ']' token
            self.eat(token_value=']')

        else:
            node = ASTNode('COMPARISON')

            # Parse left expression
            left_expr = self.expression()
            node.add_child(left_expr)

            # Parse relational operator
            op_token = self.current_token
            op_node = self.relational_oper()
            node.add_child(op_node)

            # Parse right expression
            right_expr = self.expression()
            node.add_child(right_expr)

        return node

    def expression(self):
        """expression : optional_sign term (add_oper term)*"""
        node = ASTNode('EXPRESSION')

        # Parse optional sign
        sign_node = self.optional_sign()
        if sign_node.children:  # If there's a sign
            node.add_child(sign_node)

        # Parse first term
        term_node = self.term()
        node.add_child(term_node)

        # Parse remaining terms (if any)
        while self.current_token[1] in ['+', '-']:
            op_token = self.current_token
            op_node = self.add_oper()

            # Parse term
            term_node = self.term()

            # Create binary operation node
            bin_op = ASTNode('BINARY_OPERATION', value=op_token[1])
            bin_op.add_child(node.children.pop())  # Remove last child from expression node
            bin_op.add_child(term_node)

            # Add binary operation to expression node
            node.add_child(bin_op)

        return node

    def term(self):
        """term : factor (mul_oper factor)*"""
        node = ASTNode('TERM')

        # Parse first factor
        factor_node = self.factor()
        node.add_child(factor_node)

        # Parse remaining factors (if any)
        while self.current_token[1] in ['*', '/']:
            op_token = self.current_token
            op_node = self.mul_oper()

            # Parse factor
            factor_node = self.factor()

            # Create binary operation node
            bin_op = ASTNode('BINARY_OPERATION', value=op_token[1])
            bin_op.add_child(node.children.pop())  # Remove last child from term node
            bin_op.add_child(factor_node)

            # Add binary operation to term node
            node.add_child(bin_op)
        return node

    def optional_sign(self):
        """optional_sign : add_oper | """
        node = ASTNode('OPTIONAL_SIGN')

        if self.current_token[1] in ['+', '-']:
            sign_node = self.add_oper()
            node.add_child(sign_node)

        return node

    def mul_oper(self):
        """mul_oper : '*' | '/'"""
        node = ASTNode('MUL_OPERATOR')

        if self.current_token[1] in ['*', '/']:
            token = self.eat(TokenType.OPERATOR)
            node.value = token[1]
            node.line = token[2]
        else:
            self.error("Expected '*' or '/'")

        return node

    def add_oper(self):
        """add_oper : '+' | '-'"""
        node = ASTNode('ADD_OPERATOR')

        if self.current_token[1] in ['+', '-']:
            token = self.eat(TokenType.OPERATOR)
            node.value = token[1]
            node.line = token[2]
        else:
            self.error("Expected '+' or '-'")

        return node

    def relational_oper(self):
        """relational_oper : '=' | '<=' | '>=' | '<>' | '<' | '>'"""
        node = ASTNode('RELATIONAL_OPERATOR')

        if self.current_token[0] == TokenType.RELATIONAL_OPERATOR:
            token = self.eat(TokenType.RELATIONAL_OPERATOR)
            node.value = token[1]
            node.line = token[2]
        else:
            self.error("Expected relational operator")

        return node

    def factor(self):
        """
        factor : INTEGER
               | '(' expression ')'
               | ID idtail
        """
        if self.current_token[0] == TokenType.NUMBER:
            node = ASTNode('NUMBER')

            # Get number
            num_token = self.eat(TokenType.NUMBER)
            node.value = num_token[1]
            node.line = num_token[2]

        elif self.current_token[1] == '(':
            node = ASTNode('PARENTHESIZED_EXPRESSION')

            # Eat '(' token
            self.eat(token_value='(')
            # Parse expression
            expr_node = self.expression()
            node.add_child(expr_node)
            # Eat ')' token
            self.eat(token_value=')')
        elif self.current_token[0] == TokenType.IDENTIFIER:
            node = ASTNode('IDENTIFIER')
            # Get identifier
            id_token = self.eat(TokenType.IDENTIFIER)
            id_node = ASTNode('IDENTIFIER', value=id_token[1], line=id_token[2])
            node.add_child(id_node)
            # Parse id tail (function/procedure call parameters, if any)
            idtail_node = self.idtail()
            if idtail_node.children:  # If there are parameters
                node.add_child(idtail_node)
        else:
            self.error(f"Expected factor, got {self.current_token[1]}")
        return node

