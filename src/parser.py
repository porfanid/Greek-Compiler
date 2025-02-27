#################################################################################################################
# This part of the code contains the Parser class that implements the syntax analyzer of the language.          #
# The syntax analyzer checks if the program provided by the lexical analyzer is syntactically correct.          #
# If the program is syntactically correct, it displays the message "Parsing completed successfully."            #
# If the program is not syntactically correct, it displays the message "Parsing failed: {error_message}"        #
# Finally, the parse method returns True if the program is syntactically correct, otherwise it returns False.   #
#################################################################################################################

from lexer import TokenType

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.errors = []

    def error(self, message):
        _, token_value, line = self.current_token
        error_msg = f"Error at line {line}: {message}, got '{token_value}'"
        self.errors.append(error_msg)
        print(error_msg)
        raise SyntaxError(error_msg)

    def advance(self):
        self.current_token_index += 1
        # ignore comments
        while self.tokens[self.current_token_index][0] == TokenType.COMMENT:
            self.current_token_index += 1

        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        return self.current_token

    def eat(self, token_type=None, token_value=None):
        if token_type and self.current_token[0] != token_type:
            self.error(f"Expected token type {token_type}")
        elif token_value and self.current_token[1] != token_value:
            self.error(f"Expected '{token_value}'")
        else:
            return self.advance()

    def parse(self):
        """Parse the program according to the grammar."""
        self.program()
        print("Parsing completed successfully.")

    # Κανόνες γραμματικής

    def program(self):
        """program : 'πρόγραμμα' ID programblock"""
        self.eat(token_value='πρόγραμμα')
        self.eat(TokenType.IDENTIFIER)
        self.programblock()

    def programblock(self):
        """programblock : declarations subprograms 'αρχή_προγράμματος' sequence 'τέλος_προγράμματος'"""
        self.declarations()
        self.subprograms()
        self.eat(token_value='αρχή_προγράμματος')
        self.sequence()
        self.eat(token_value='τέλος_προγράμματος')

    def declarations(self):
        """declarations : ('δήλωση' varlist)* | """
        while self.current_token[1] == 'δήλωση':
            self.eat(token_value='δήλωση')
            self.varlist()

    def varlist(self):
        """varlist : ID (',' ID)*"""
        self.eat(TokenType.IDENTIFIER)
        while self.current_token[1] == ',':
            self.eat(token_value=',')
            self.eat(TokenType.IDENTIFIER)

    def subprograms(self):
        """subprograms : (func | proc)*"""
        while self.current_token[1] in ['συνάρτηση', 'διαδικασία']:
            if self.current_token[1] == 'συνάρτηση':
                self.func()
            else:
                self.proc()

    def func(self):
        """func : 'συνάρτηση' ID '(' formalparlist ')' funcblock"""
        self.eat(token_value='συνάρτηση')
        self.eat(TokenType.IDENTIFIER)
        self.eat(token_value='(')
        self.formalparlist()
        self.eat(token_value=')')
        self.funcblock()

    def proc(self):
        """proc : 'διαδικασία' ID '(' formalparlist ')' procblock"""
        self.eat(token_value='διαδικασία')
        self.eat(TokenType.IDENTIFIER)
        self.eat(token_value='(')
        self.formalparlist()
        self.eat(token_value=')')
        self.procblock()

    def formalparlist(self):
        """formalparlist : varlist | """
        if self.current_token[0] == TokenType.IDENTIFIER:
            self.varlist()

    def funcblock(self):
        """funcblock : 'διαπροσωπεία' funcinput funcoutput declarations subprograms
         'αρχή_συνάρτησης' sequence 'τέλος_συνάρτησης'"""
        self.eat(token_value='διαπροσωπεία')
        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()  # Added this line to implement nested subprograms
        self.eat(token_value='αρχή_συνάρτησης')
        self.sequence()
        self.eat(token_value='τέλος_συνάρτησης')

    def procblock(self):
        """procblock : 'διαπροσωπεία' funcinput funcoutput declarations subprograms
         'αρχή_διαδικασίας' sequence 'τέλος_διαδικασίας'"""
        self.eat(token_value='διαπροσωπεία')
        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()  # Added this line to implement nested subprograms
        self.eat(token_value='αρχή_διαδικασίας')
        self.sequence()
        self.eat(token_value='τέλος_διαδικασίας')

    def funcinput(self):
        """funcinput : 'είσοδος' varlist | """
        if self.current_token[1] == 'είσοδος':
            self.eat(token_value='είσοδος')
            self.varlist()

    def funcoutput(self):
        """funcoutput : 'έξοδος' varlist | """
        if self.current_token[1] == 'έξοδος':
            self.eat(token_value='έξοδος')
            self.varlist()

    def sequence(self):
        """sequence : statement (';' statement)*"""
        self.statement()
        while self.current_token[1] == ';':
            self.eat(token_value=';')
            self.statement()

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
            self.assignment_stat()
        elif self.current_token[1] == 'εάν':
            self.if_stat()
        elif self.current_token[1] == 'όσο':
            self.while_stat()
        elif self.current_token[1] == 'επανάλαβε':
            self.do_stat()
        elif self.current_token[1] == 'για':
            self.for_stat()
        elif self.current_token[1] == 'διάβασε':
            self.input_stat()
        elif self.current_token[1] == 'γράψε':
            self.print_stat()
        elif self.current_token[1] == 'εκτέλεσε':
            self.call_stat()
        else:
            self.error(f"Expected statement, got {self.current_token[1]}")

    def assignment_stat(self):
        """assignment_stat : ID ':=' expression"""
        self.eat(TokenType.IDENTIFIER)
        self.eat(token_value=':=')
        self.expression()

    def if_stat(self):
        """if_stat : 'εάν' condition 'τότε' sequence elsepart 'εάν_τέλος'"""
        self.eat(token_value='εάν')
        self.condition()
        self.eat(token_value='τότε')
        self.sequence()
        self.elsepart()
        self.eat(token_value='εάν_τέλος')

    def elsepart(self):
        """elsepart : 'αλλιώς' sequence | """
        if self.current_token[1] == 'αλλιώς':
            self.eat(token_value='αλλιώς')
            self.sequence()

    def while_stat(self):
        """while_stat : 'όσο' condition 'επανάλαβε' sequence 'όσο_τέλος'"""
        self.eat(token_value='όσο')
        self.condition()
        self.eat(token_value='επανάλαβε')
        self.sequence()
        self.eat(token_value='όσο_τέλος')

    def do_stat(self):
        """do_stat : 'επανάλαβε' sequence 'μέχρι' condition"""
        self.eat(token_value='επανάλαβε')
        self.sequence()
        self.eat(token_value='μέχρι')
        self.condition()

    def for_stat(self):
        """for_stat : 'για' ID ':=' expression 'έως' expression step 'επανάλαβε' sequence 'για_τέλος'"""
        self.eat(token_value='για')
        self.eat(TokenType.IDENTIFIER)
        self.eat(token_value=':=')
        self.expression()
        self.eat(token_value='έως')
        self.expression()
        self.step()
        self.eat(token_value='επανάλαβε')
        self.sequence()
        self.eat(token_value='για_τέλος')

    def step(self):
        """step : 'με_βήμα' expression | """
        if self.current_token[1] == 'με_βήμα':
            self.eat(token_value='με_βήμα')
            self.expression()

    def print_stat(self):
        """print_stat : 'γράψε' expression"""
        self.eat(token_value='γράψε')
        self.expression()

    def input_stat(self):
        """input_stat : 'διάβασε' ID"""
        self.eat(token_value='διάβασε')
        self.eat(TokenType.IDENTIFIER)

    def call_stat(self):
        """call_stat : 'εκτέλεσε' ID idtail"""
        self.eat(token_value='εκτέλεσε')
        self.eat(TokenType.IDENTIFIER)
        self.idtail()

    def idtail(self):
        """idtail : actualpars | """
        if self.current_token[1] == '(':
            self.actualpars()

    def actualpars(self):
        """actualpars : '(' actualparlist ')'"""
        self.eat(token_value='(')
        self.actualparlist()
        self.eat(token_value=')')

    def actualparlist(self):
        """actualparlist : actualparitem (',' actualparitem)* | """
        if self.current_token[1] != ')':
            self.actualparitem()
            while self.current_token[1] == ',':
                self.eat(token_value=',')
                self.actualparitem()

    def actualparitem(self):
        """actualparitem : expression | '%' ID"""
        if self.current_token[1] == '%':
            self.eat(token_value='%')
            self.eat(TokenType.IDENTIFIER)
        else:
            self.expression()

    def condition(self):
        """condition : boolterm ('ή' boolterm)*"""
        self.boolterm()
        while self.current_token[1] == 'ή':
            self.eat(token_value='ή')
            self.boolterm()

    def boolterm(self):
        """boolterm : boolfactor ('και' boolfactor)*"""
        self.boolfactor()
        while self.current_token[1] == 'και':
            self.eat(token_value='και')
            self.boolfactor()

    def boolfactor(self):
        """
        boolfactor : 'όχι' '[' condition ']'
                   | '[' condition ']'
                   | expression relational_oper expression
        """
        if self.current_token[1] == 'όχι':
            self.eat(token_value='όχι')
            self.eat(token_value='[')
            self.condition()
            self.eat(token_value=']')
        elif self.current_token[1] == '[':
            self.eat(token_value='[')
            self.condition()
            self.eat(token_value=']')
        else:
            self.expression()
            self.relational_oper()
            self.expression()

    def expression(self):
        """expression : optional_sign term (add_oper term)*"""
        self.optional_sign()
        self.term()
        while self.current_token[1] in ['+', '-']:
            self.add_oper()
            self.term()

    def term(self):
        """term : factor (mul_oper factor)*"""
        self.factor()
        while self.current_token[1] in ['*', '/']:
            self.mul_oper()
            self.factor()

    def factor(self):
        """
        factor : INTEGER
               | '(' expression ')'
               | ID idtail
        """
        if self.current_token[0] == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
        elif self.current_token[1] == '(':
            self.eat(token_value='(')
            self.expression()
            self.eat(token_value=')')
        elif self.current_token[0] == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            self.idtail()
        else:
            self.error(f"Expected factor, got {self.current_token[1]}")

    def relational_oper(self):
        """relational_oper : '=' | '<=' | '>=' | '<>' | '<' | '>'"""
        if self.current_token[0] == TokenType.RELATIONAL_OPERATOR:
            self.eat(TokenType.RELATIONAL_OPERATOR)
        else:
            self.error("Expected relational operator")

    def add_oper(self):
        """add_oper : '+' | '-'"""
        if self.current_token[1] in ['+', '-']:
            self.eat(TokenType.OPERATOR)
        else:
            self.error("Expected '+' or '-'")

    def mul_oper(self):
        """mul_oper : '*' | '/'"""
        if self.current_token[1] in ['*', '/']:
            self.eat(TokenType.OPERATOR)
        else:
            self.error("Expected '*' or '/'")

    def optional_sign(self):
        """optional_sign : add_oper | """
        if self.current_token[1] in ['+', '-']:
            self.add_oper()


#############################################################################################################
# End of Parser class.                                                                                      #
#############################################################################################################
