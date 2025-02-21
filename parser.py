# Define the states
from lexer import TokenType
class State:
    START = 'START'
    DECLARATION = 'DECLARATION'
    FUNCTION = 'FUNCTION'
    PROCEDURE = 'PROCEDURE'
    PROGRAM_BLOCK = 'PROGRAM_BLOCK'
    STATEMENT = 'STATEMENT'
    PARAMETERS = 'PARAMETERS'
    FUNCTION_BODY = 'FUNCTION_BODY'
    REPEAT_LOOP = 'REPEAT_LOOP'
    FOR_LOOP = 'FOR_LOOP'
    END = 'END'

# Define the state transitions
state_matrix = {
    State.START: {
        'πρόγραμμα': State.PROGRAM_BLOCK,
    },
    State.PROGRAM_BLOCK: {
        'IDENTIFIER': State.DECLARATION,  # Handle the program name
        'δήλωση': State.DECLARATION,
        'συνάρτηση': State.FUNCTION,
        'διαδικασία': State.PROCEDURE,
        'αρχή_προγράμματος': State.STATEMENT,
        'τέλος_προγράμματος': State.END,
    },
    State.DECLARATION: {
        'IDENTIFIER': State.DECLARATION,  # Handle multiple identifiers
        'δήλωση': State.DECLARATION,
        'συνάρτηση': State.FUNCTION,
        'διαδικασία': State.PROCEDURE,
        'αρχή_προγράμματος': State.STATEMENT,
        'τέλος_προγράμματος': State.END,
        'SEPARATOR': State.DECLARATION,  # Handle separators
    },
    State.FUNCTION: {
        'IDENTIFIER': State.FUNCTION,  # Handle the function name
        '(': State.PARAMETERS,  # Transition to PARAMETERS state
    },
    State.PARAMETERS: {
        'IDENTIFIER': State.PARAMETERS,  # Handle parameter names
        'SEPARATOR': State.PARAMETERS,  # Handle separators
        ')': State.FUNCTION_BODY,  # Transition to FUNCTION_BODY state
    },
    State.FUNCTION_BODY: {
        'διαπροσωπεία': State.FUNCTION_BODY,
        'είσοδος': State.FUNCTION_BODY,
        'έξοδος': State.FUNCTION_BODY,
        'IDENTIFIER': State.STATEMENT,  # Allow identifiers as statements
        ':=': State.STATEMENT,  # Allow assignments
        'αρχή_συνάρτησης': State.STATEMENT,
        'τέλος_συνάρτησης': State.PROGRAM_BLOCK,
    },
    State.PROCEDURE: {
        'IDENTIFIER': State.STATEMENT,  # Correct transition for procedure name
        '(': State.PARAMETERS,  # Transition to PARAMETERS state
    },
    State.STATEMENT: {
        'IDENTIFIER': State.STATEMENT,
        ':=': State.STATEMENT,
        'επανάλαβε': State.REPEAT_LOOP,
        'για': State.FOR_LOOP,
        'τέλος_προγράμματος': State.END,
        'τέλος_συνάρτησης': State.PROGRAM_BLOCK,  # Allow function end inside statements
        'τέλος_διαδικασίας': State.PROGRAM_BLOCK,  # Ensure procedures end correctly
    },
    State.REPEAT_LOOP: {
        'IDENTIFIER': State.STATEMENT,
        ':=': State.STATEMENT,
        'μέχρι': State.STATEMENT,  # Ensure repeat loops require an exit condition
    },
    State.FOR_LOOP: {
        'IDENTIFIER': State.STATEMENT,
        ':=': State.STATEMENT,
        'έως': State.STATEMENT,
        'με_βήμα': State.STATEMENT,
        'επαναλαβε': State.STATEMENT,
        'για_τέλος': State.STATEMENT,
    },
    State.END: {}
}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.current_state = State.START

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.current_token_index += 1
            if self.current_token_index < len(self.tokens):
                self.current_token = self.tokens[self.current_token_index]
        else:
            raise SyntaxError(f'Unexpected token: {self.tokens[self.current_token_index-1]}')

    def transition(self, token_value):
        if token_value in state_matrix[self.current_state]:
            self.current_state = state_matrix[self.current_state][token_value]
        elif self.current_state == State.PROGRAM_BLOCK and self.current_token[0] == TokenType.IDENTIFIER:
            self.current_state = State.DECLARATION
        elif self.current_state == State.DECLARATION and self.current_token[0] in {TokenType.IDENTIFIER, TokenType.SEPARATOR}:
            self.current_state = State.DECLARATION
        elif self.current_state == State.FUNCTION and self.current_token[0] == TokenType.IDENTIFIER:
            self.current_state = State.FUNCTION
        elif self.current_state == State.FUNCTION and self.current_token[0] == TokenType.GROUPING and token_value == '(':
            self.current_state = State.PARAMETERS
        elif self.current_state == State.PROCEDURE and self.current_token[0] == TokenType.IDENTIFIER:
            self.current_state = State.STATEMENT  # Ensure procedure name transitions correctly
        elif self.current_state == State.FOR_LOOP and token_value in {'έως', 'με_βήμα', 'επαναλαβε', 'για_τέλος'}:
            self.current_state = State.STATEMENT
        elif self.current_state == State.PARAMETERS and self.current_token[0] in {TokenType.IDENTIFIER, TokenType.SEPARATOR, TokenType.GROUPING}:
            self.current_state = State.PARAMETERS
            if token_value == ')':
                self.current_state = State.FUNCTION_BODY
        elif self.current_state == State.FUNCTION_BODY:
            if token_value in {'διαπροσωπεία', 'είσοδος', 'έξοδος'}:
                self.current_state = State.FUNCTION_BODY
            elif self.current_token[0] == TokenType.IDENTIFIER or token_value == ':=':
                self.current_state = State.STATEMENT  # Transition to statement handling inside function body
            elif token_value == 'αρχή_συνάρτησης':
                self.current_state = State.STATEMENT
        elif self.current_state == State.REPEAT_LOOP:
            if token_value == 'μέχρι':
                self.current_state = State.STATEMENT
        else:
            raise SyntaxError(f'Unexpected token: {token_value} in state: {self.current_state}')

    def parse(self):
        while self.current_state != State.END:
            token_type, token_value, _ = self.current_token
            self.transition(token_value)
            self.eat(token_type)
            print(self.current_token)
        print("Parsing completed successfully.")
