import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from src.lexer import Lexer, TokenType


class TestLexer(unittest.TestCase):
    def test_lexer_tokenizes_keywords_correctly(self):
        lexer = Lexer("./tests/keywords.gr")
        tokens = lexer.tokenize()
        expected_tokens = [
            ('KEYWORD', 'πρόγραμμα', 1), ('KEYWORD', 'δήλωση', 2),
            ('KEYWORD', 'εάν', 3), ('KEYWORD', 'τότε', 4),
            ('KEYWORD', 'αλλιώς', 5), ('KEYWORD', 'εάν_τέλος', 6)
        ]
        self.assertEqual(tokens[:6], expected_tokens)

    def test_lexer_tokenizes_operators_correctly(self):
        lexer = Lexer("./tests/operators.gr")
        tokens = lexer.tokenize()
        expected_tokens = [
            ('OPERATOR', '+', 1), ('OPERATOR', '-', 1),
            ('OPERATOR', '*', 1), ('OPERATOR', '/', 1)
        ]
        self.assertEqual(tokens[:4], expected_tokens)

    def test_lexer_tokenizes_numbers_correctly(self):
        lexer = Lexer("./tests/numbers.gr")
        tokens = lexer.tokenize()
        expected_tokens = [
            ('NUMBER', '123', 1), ('NUMBER', '45.67', 2)
        ]
        self.assertEqual(tokens[:2], expected_tokens)

    def test_lexer_handles_unexpected_characters(self):
        lexer = Lexer("./tests/unexpected.gr")
        with self.assertRaises(SyntaxError):
            lexer.tokenize()

    def test_lexer_tokenizes_identifiers_correctly(self):
        lexer = Lexer("./tests/identifiers.gr")
        tokens = lexer.tokenize()
        expected_tokens = [
            ('IDENTIFIER', 'variable1', 1), ('IDENTIFIER', 'var_2', 2)
        ]
        self.assertEqual(tokens[:2], expected_tokens)

    def test_lexer_tokenizes_grouping_symbols_correctly(self):
        lexer = Lexer("./tests/grouping.gr")
        tokens = lexer.tokenize()
        expected_tokens = [
            ('GROUPING', '(', 1), ('GROUPING', ')', 1),
            ('GROUPING', '[', 1), ('GROUPING', ']', 1)
        ]
        self.assertEqual(tokens[:4], expected_tokens)

    def test_lexer_tokenizes_relational_operators_correctly(self):
        lexer = Lexer("./tests/relational_operators.gr")
        tokens = lexer.tokenize()
        expected_tokens = [
            ('RELATIONAL_OPERATOR', '<=', 1), ('RELATIONAL_OPERATOR', '>=', 1),
            ('RELATIONAL_OPERATOR', '<>', 1), ('RELATIONAL_OPERATOR', '<', 1),
            ('RELATIONAL_OPERATOR', '>', 1), ('RELATIONAL_OPERATOR', '=', 1)
        ]
        self.assertEqual(tokens[:6], expected_tokens)

    def test_lexer_tokenizes_assignment_correctly(self):
        lexer = Lexer("./tests/assignment.gr")
        tokens = lexer.tokenize()
        expected_tokens = [
            ('ASSIGNMENT', ':=', 1)
        ]
        self.assertEqual(tokens[:1], expected_tokens)

    def test_lexer_tokenizes_comments_correctly(self):
        lexer = Lexer("./tests/comments.gr")
        tokens = lexer.tokenize()
        expected_tokens = [
            ('KEYWORD', 'πρόγραμμα', 1), ('COMMENT', 'This is a comment', 2),
            ('KEYWORD', 'δήλωση', 3)
        ]
        self.assertEqual(tokens[:3], expected_tokens)

    def test_lexer_tokenizes_separators_correctly(self):
        lexer = Lexer("./tests/separators.gr")
        tokens = lexer.tokenize()
        expected_tokens = [
            ('SEPARATOR', ';', 1), ('SEPARATOR', ',', 2), ('SEPARATOR', ':', 3)
        ]
        self.assertEqual(tokens[:3], expected_tokens)

    def test_lexer_tokenizes_equal_sign_correctly(self):
        lexer = Lexer("./tests/equal_sign.gr")
        tokens = lexer.tokenize()
        expected_tokens = [
            ('RELATIONAL_OPERATOR', '=', 1)
        ]
        self.assertEqual(tokens[:1], expected_tokens)


if __name__ == '__main__':
    unittest.main()