class TokenType:
    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    RELATIONAL_OPERATOR = 'RELATIONAL_OPERATOR'
    ASSIGNMENT = 'ASSIGNMENT'
    SEPARATOR = 'SEPARATOR'
    GROUPING = 'GROUPING'
    COMMENT = 'COMMENT'
    REFERENCE = 'REFERENCE'
    EOF = 'EOF'


KEYWORDS = {
    'πρόγραμμα', 'δήλωση', 'εάν', 'τότε', 'αλλιώς', 'εάν_τέλος',
    'επανάλαβε', 'μέχρι', 'όσο', 'όσο_τέλος', 'για', 'έως', 'με_βήμα',
    'για_τέλος', 'διάβασε', 'γράψε', 'συνάρτηση', 'διαδικασία', 'είσοδος',
    'έξοδος', 'διαπροσωπεία', 'αρχή_συνάρτησης', 'τέλος_συνάρτησης',
    'αρχή_διαδικασίας', 'τέλος_διαδικασίας', 'αρχή_προγράμματος', 'τέλος_προγράμματος',
    'ή', 'και', 'εκτέλεσε'
}

OPERATORS = {'+', '-', '*', '/'}
RELATIONAL_OPERATORS = {'<=', '>=', '<>', '<', '>', '='}
ASSIGNMENT = ':='
SEPARATORS = {';', ',', ':'}
GROUPING = {'(', ')', '[', ']', '"'}
REFERENCE = '%'

class Lexer:
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []
        self.current_char = None
        self.next_char = None
        self.file = None
        self.line_number = 1

    def open_file(self):
        try:
            self.file = open(self.filename, 'r', encoding='utf-8')
            self.advance()  # Load the first character
        except FileNotFoundError:
            print(f"File not found: {self.filename}")
            raise

    def advance(self):
        """Move to the next character in the file."""
        if self.next_char is None:
            self.current_char = self.file.read(1)
        else:
            self.current_char = self.next_char
        self.next_char = self.file.read(1)
        if self.current_char == '\n':
            self.line_number += 1

    def peek(self):
        """Look at the next character without advancing."""
        return self.next_char

    def skip_whitespace(self):
        """Skip spaces and newlines."""
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        """Skip over comments enclosed in `{}`."""
        while self.current_char and self.current_char != '}':
            self.advance()
        self.advance()  # Move past closing `}`

    def collect_number(self):
        """Collect a number (integer or float)."""
        number = self.current_char
        self.advance()
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            number += self.current_char
            self.advance()
        return (TokenType.NUMBER, number, self.line_number)

    def collect_identifier(self):
        """Collect an identifier or a keyword."""
        identifier = self.current_char
        self.advance()
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()
        if identifier in KEYWORDS:
            return (TokenType.KEYWORD, identifier, self.line_number)
        return (TokenType.IDENTIFIER, identifier, self.line_number)

    def tokenize(self):
        """Tokenize the input file character by character."""
        self.open_file()

        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '{':
                self.advance()
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                self.tokens.append(self.collect_number())
                continue

            if self.current_char.isalpha():
                self.tokens.append(self.collect_identifier())
                continue

            # Handling two-character operators
            if self.current_char == ':':
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append((TokenType.ASSIGNMENT, ':=', self.line_number))
                else:
                    self.tokens.append((TokenType.SEPARATOR, ':', self.line_number))
                self.advance()
                continue

            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append((TokenType.RELATIONAL_OPERATOR, '<=', self.line_number))
                elif self.peek() == '>':
                    self.advance()
                    self.tokens.append((TokenType.RELATIONAL_OPERATOR, '<>', self.line_number))
                else:
                    self.tokens.append((TokenType.RELATIONAL_OPERATOR, '<', self.line_number))
                self.advance()
                continue

            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.tokens.append((TokenType.RELATIONAL_OPERATOR, '>=', self.line_number))
                else:
                    self.tokens.append((TokenType.RELATIONAL_OPERATOR, '>', self.line_number))
                self.advance()
                continue

            if self.current_char == '=':
                self.tokens.append((TokenType.RELATIONAL_OPERATOR, '=', self.line_number))
                self.advance()
                continue

            # Single-character operators
            if self.current_char in OPERATORS:
                self.tokens.append((TokenType.OPERATOR, self.current_char, self.line_number))
                self.advance()
                continue

            if self.current_char in SEPARATORS:
                self.tokens.append((TokenType.SEPARATOR, self.current_char, self.line_number))
                self.advance()
                continue

            if self.current_char in GROUPING:
                self.tokens.append((TokenType.GROUPING, self.current_char, self.line_number))
                self.advance()
                continue

            if self.current_char == '%':
                self.tokens.append((TokenType.REFERENCE, self.current_char, self.line_number))
                self.advance()
                continue

            print(f'Unexpected character: {self.current_char}')
            raise SyntaxError(f'Unexpected character: {self.current_char}')

        self.tokens.append((TokenType.EOF, 'EOF', self.line_number))
        self.file.close()
        return self.tokens

if __name__ == '__main__':
    lexer = Lexer("./test.gr")
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)