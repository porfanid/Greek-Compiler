# Define the states
class State:
    START = 'START'
    DECLARATION = 'DECLARATION'
    FUNCTION = 'FUNCTION'
    PROCEDURE = 'PROCEDURE'
    PROGRAM_BLOCK = 'PROGRAM_BLOCK'
    STATEMENT = 'STATEMENT'
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
        'δήλωση': State.DECLARATION,
        'συνάρτηση': State.FUNCTION,
        'διαδικασία': State.PROCEDURE,
        'αρχή_προγράμματος': State.STATEMENT,
        'τέλος_προγράμματος': State.END,
    },
    State.FUNCTION: {
        'αρχή_συνάρτησης': State.STATEMENT,
        'τέλος_συνάρτησης': State.PROGRAM_BLOCK,
    },
    State.PROCEDURE: {
        'αρχή_διαδικασίας': State.STATEMENT,
        'τέλος_διαδικασίας': State.PROGRAM_BLOCK,
    },
    State.STATEMENT: {
        'τέλος_προγράμματος': State.END,
        # Add other possible transitions for statements
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
        else:
            raise SyntaxError(f'Unexpected token: {token_value} in state: {self.current_state}')

    def parse(self):
        while self.current_state != State.END:
            token_type, token_value, _ = self.current_token
            self.transition(token_value)
            self.eat(token_type)
        print("Parsing completed successfully.")