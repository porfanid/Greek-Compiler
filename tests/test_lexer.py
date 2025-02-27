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

    def test_lexer(self):
        lexer = Lexer("./tests/correct.gr")
        tokens = lexer.tokenize()
        expected_tokens = [('KEYWORD', 'πρόγραμμα', 1), ('IDENTIFIER', 'τεστ', 1), ('KEYWORD', 'δήλωση', 3), ('IDENTIFIER', 'α', 3), ('SEPARATOR', ',', 3), ('IDENTIFIER', 'β', 3), ('KEYWORD', 'δήλωση', 4), ('IDENTIFIER', 'γ', 4), ('KEYWORD', 'συνάρτηση', 6), ('IDENTIFIER', 'αύξηση', 6), ('GROUPING', '(', 6), ('IDENTIFIER', 'α', 6), ('SEPARATOR', ',', 6), ('IDENTIFIER', 'β', 6), ('GROUPING', ')', 6), ('KEYWORD', 'διαπροσωπεία', 7), ('KEYWORD', 'είσοδος', 8), ('IDENTIFIER', 'α', 8), ('KEYWORD', 'έξοδος', 9), ('IDENTIFIER', 'β', 9), ('KEYWORD', 'αρχή_συνάρτησης', 10), ('IDENTIFIER', 'β', 11), ('ASSIGNMENT', ':=', 11), ('IDENTIFIER', 'α', 11), ('OPERATOR', '+', 11), ('NUMBER', '1', 11), ('SEPARATOR', ';', 11), ('IDENTIFIER', 'αύξηση', 12), ('ASSIGNMENT', ':=', 12), ('IDENTIFIER', 'α', 12), ('OPERATOR', '+', 12), ('NUMBER', '1', 12), ('COMMENT', 'δεν μπαίνει ερωτηματικό\n  είναι τέλος block', 13), ('KEYWORD', 'τέλος_συνάρτησης', 15), ('KEYWORD', 'διαδικασία', 17), ('IDENTIFIER', 'τύπωσε_συν_1', 17), ('GROUPING', '(', 17), ('IDENTIFIER', 'χ', 17), ('GROUPING', ')', 17), ('KEYWORD', 'διαπροσωπεία', 18), ('KEYWORD', 'είσοδος', 19), ('IDENTIFIER', 'χ', 19), ('KEYWORD', 'αρχή_διαδικασίας', 20), ('KEYWORD', 'γράψε', 21), ('IDENTIFIER', 'χ', 21), ('OPERATOR', '+', 21), ('NUMBER', '1', 21), ('KEYWORD', 'τέλος_διαδικασίας', 22), ('KEYWORD', 'αρχή_προγράμματος', 24), ('IDENTIFIER', 'α', 25), ('ASSIGNMENT', ':=', 25), ('NUMBER', '1', 25), ('SEPARATOR', ';', 25), ('IDENTIFIER', 'β', 26), ('ASSIGNMENT', ':=', 26), ('NUMBER', '2', 26), ('OPERATOR', '+', 26), ('IDENTIFIER', 'α', 26), ('OPERATOR', '*', 26), ('IDENTIFIER', 'α', 26), ('OPERATOR', '/', 26), ('GROUPING', '(', 26), ('NUMBER', '2', 26), ('OPERATOR', '-', 26), ('IDENTIFIER', 'α', 26), ('OPERATOR', '-', 26), ('GROUPING', '(', 26), ('NUMBER', '2', 26), ('OPERATOR', '*', 26), ('IDENTIFIER', 'α', 26), ('GROUPING', ')', 26), ('GROUPING', ')', 26), ('SEPARATOR', ';', 26), ('IDENTIFIER', 'γ', 27), ('ASSIGNMENT', ':=', 27), ('IDENTIFIER', 'αύξηση', 27), ('GROUPING', '(', 27), ('IDENTIFIER', 'α', 27), ('SEPARATOR', ',', 27), ('REFERENCE', '%', 27), ('IDENTIFIER', 'β', 27), ('GROUPING', ')', 27), ('SEPARATOR', ';', 27), ('KEYWORD', 'για', 29), ('IDENTIFIER', 'α', 29), ('ASSIGNMENT', ':=', 29), ('NUMBER', '1', 29), ('KEYWORD', 'έως', 29), ('NUMBER', '8', 29), ('KEYWORD', 'με_βήμα', 29), ('NUMBER', '2', 29), ('KEYWORD', 'επανάλαβε', 29), ('KEYWORD', 'εκτέλεσε', 30), ('IDENTIFIER', 'τύπωσε_συν_1', 30), ('GROUPING', '(', 30), ('IDENTIFIER', 'α', 30), ('GROUPING', ')', 30), ('KEYWORD', 'για_τέλος', 31), ('SEPARATOR', ';', 31), ('IDENTIFIER', 'β', 33), ('ASSIGNMENT', ':=', 33), ('NUMBER', '1', 33), ('SEPARATOR', ';', 33), ('KEYWORD', 'όσο', 34), ('IDENTIFIER', 'β', 34), ('RELATIONAL_OPERATOR', '<', 34), ('NUMBER', '10', 34), ('KEYWORD', 'επανάλαβε', 34), ('KEYWORD', 'εάν', 35), ('IDENTIFIER', 'β', 35), ('RELATIONAL_OPERATOR', '<>', 35), ('NUMBER', '22', 35), ('KEYWORD', 'ή', 35), ('GROUPING', '[', 35), ('IDENTIFIER', 'β', 35), ('RELATIONAL_OPERATOR', '>=', 35), ('NUMBER', '23', 35), ('KEYWORD', 'και', 35), ('IDENTIFIER', 'β', 35), ('RELATIONAL_OPERATOR', '<=', 35), ('NUMBER', '24', 35), ('GROUPING', ']', 35), ('KEYWORD', 'τότε', 35), ('IDENTIFIER', 'β', 36), ('ASSIGNMENT', ':=', 36), ('IDENTIFIER', 'β', 36), ('OPERATOR', '+', 36), ('NUMBER', '1', 36), ('KEYWORD', 'εάν_τέλος', 37), ('COMMENT', 'όχι ερωτηματικό, είναι τέλος block', 38), ('KEYWORD', 'όσο_τέλος', 39), ('SEPARATOR', ';', 39), ('KEYWORD', 'διάβασε', 41), ('IDENTIFIER', 'β', 41), ('SEPARATOR', ';', 41), ('KEYWORD', 'επανάλαβε', 42), ('IDENTIFIER', 'β', 43), ('ASSIGNMENT', ':=', 43), ('IDENTIFIER', 'β', 43), ('OPERATOR', '+', 43), ('NUMBER', '1', 43), ('KEYWORD', 'μέχρι', 44), ('IDENTIFIER', 'β', 44), ('RELATIONAL_OPERATOR', '<', 44), ('OPERATOR', '-', 44), ('NUMBER', '100', 44), ('KEYWORD', 'τέλος_προγράμματος', 46), ('EOF', 'EOF', 46)]
        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()