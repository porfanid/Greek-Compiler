# tests/test_lexer.py
import unittest
from lexer import Lexer, TokenType


class TestLexer(unittest.TestCase):
    def test_lexer(self):
        lexer = Lexer("./tests/correct.gr")
        tokens = lexer.tokenize()

        expected_tokens = [
            (TokenType.KEYWORD, 'πρόγραμμα', 1),
            (TokenType.IDENTIFIER, 'τεστ', 2),
            (TokenType.KEYWORD, 'δήλωση', 2),
            (TokenType.IDENTIFIER, 'α', 2),
            (TokenType.SEPARATOR, ',', 2),
            (TokenType.IDENTIFIER, 'β', 3),
            (TokenType.KEYWORD, 'δήλωση', 3),
            (TokenType.IDENTIFIER, 'γ', 4),
            (TokenType.KEYWORD, 'συνάρτηση', 4),
            (TokenType.IDENTIFIER, 'αύξηση', 4),
            (TokenType.GROUPING, '(', 4),
            (TokenType.IDENTIFIER, 'α', 4),
            (TokenType.SEPARATOR, ',', 4),
            (TokenType.IDENTIFIER, 'β', 4),
            (TokenType.GROUPING, ')', 4),
            (TokenType.KEYWORD, 'διαπροσωπεία', 6),
            (TokenType.KEYWORD, 'είσοδος', 6),
            (TokenType.IDENTIFIER, 'α', 7),
            (TokenType.KEYWORD, 'έξοδος', 7),
            (TokenType.IDENTIFIER, 'β', 8),
            (TokenType.KEYWORD, 'αρχή_συνάρτησης', 9),
            (TokenType.IDENTIFIER, 'β', 9),
            (TokenType.ASSIGNMENT, ':=', 9),
            (TokenType.IDENTIFIER, 'α', 9),
            (TokenType.OPERATOR, '+', 9),
            (TokenType.NUMBER, '1', 9),
            (TokenType.SEPARATOR, ';', 9),
            (TokenType.IDENTIFIER, 'αύξηση', 10),
            (TokenType.ASSIGNMENT, ':=', 10),
            (TokenType.IDENTIFIER, 'α', 10),
            (TokenType.OPERATOR, '+', 10),
            (TokenType.NUMBER, '1', 11),
            (TokenType.KEYWORD, 'τέλος_συνάρτησης', 11),
            (TokenType.EOF, 'EOF', 11)
        ]

        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()