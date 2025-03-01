import sys
import os
# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from src.compiler import perform_lexical_analysis



class TestLexer(unittest.TestCase):
    def test_lexer_tokenizes_keywords_correctly(self):

        tokens = perform_lexical_analysis("tests/lexer_inputs/keywords.gr", True)
        expected_tokens = [
            ('KEYWORD', 'πρόγραμμα', 1), ('KEYWORD', 'δήλωση', 2),
            ('KEYWORD', 'εάν', 3), ('KEYWORD', 'τότε', 4),
            ('KEYWORD', 'αλλιώς', 5), ('KEYWORD', 'εάν_τέλος', 6)
        ]
        self.assertEqual(tokens[:6], expected_tokens)

    def test_lexer_tokenizes_operators_correctly(self):
        tokens = perform_lexical_analysis("tests/lexer_inputs/operators.gr",True)
        expected_tokens = [
            ('OPERATOR', '+', 1), ('OPERATOR', '-',2),
            ('OPERATOR', '*', 3), ('OPERATOR', '/', 4)
        ]
        self.assertEqual(tokens[:4], expected_tokens)

    def test_lexer_tokenizes_numbers_correctly(self):
        tokens = perform_lexical_analysis("tests/lexer_inputs/numbers.gr",True)
        expected_tokens = [
            ('NUMBER', '123', 1), ('NUMBER', '45.67', 2)
        ]
        self.assertEqual(tokens[:2], expected_tokens)

    def test_lexer_handles_unexpected_characters(self):
        with self.assertRaises(SyntaxError):
            tokens = perform_lexical_analysis("tests/lexer_inputs/unexpected.gr",True)

    def test_lexer_tokenizes_identifiers_correctly(self):
        tokens = perform_lexical_analysis("tests/lexer_inputs/identifiers.gr", True)
        expected_tokens = [
            ('IDENTIFIER', 'variable1', 1), ('IDENTIFIER', 'var_2', 2)
        ]
        self.assertEqual(tokens[:2], expected_tokens)

    def test_lexer_tokenizes_grouping_symbols_correctly(self):
        tokens = perform_lexical_analysis("tests/lexer_inputs/grouping.gr", True)
        expected_tokens = [
            ('GROUPING', '(', 1), ('GROUPING', ')', 1),
            ('GROUPING', '[', 2), ('GROUPING', ']', 2)
        ]
        self.assertEqual(tokens[:4], expected_tokens)

    def test_lexer_tokenizes_relational_operators_correctly(self):
        tokens = perform_lexical_analysis("tests/lexer_inputs/relational_operators.gr", True)
        expected_tokens = [
            ('RELATIONAL_OPERATOR', '<=', 1), ('RELATIONAL_OPERATOR', '>=', 2),
            ('RELATIONAL_OPERATOR', '<>', 3), ('RELATIONAL_OPERATOR', '<', 4),
            ('RELATIONAL_OPERATOR', '>', 5), ('RELATIONAL_OPERATOR', '=', 6)
        ]
        self.assertEqual(tokens[:6], expected_tokens)

    def test_lexer_tokenizes_assignment_correctly(self):
        tokens = perform_lexical_analysis("tests/lexer_inputs/assignment.gr", True)
        expected_tokens = [
            ('ASSIGNMENT', ':=', 1)
        ]
        self.assertEqual(tokens[:1], expected_tokens)

    def test_lexer_tokenizes_comments_correctly(self):
        tokens = perform_lexical_analysis("tests/lexer_inputs/comments.gr", True)
        expected_tokens = [
            ('KEYWORD', 'πρόγραμμα', 1), ('COMMENT', 'This is a comment', 2),
            ('KEYWORD', 'δήλωση', 3)
        ]
        self.assertEqual(tokens[:3], expected_tokens)

    def test_lexer_tokenizes_separators_correctly(self):
        tokens = perform_lexical_analysis("tests/lexer_inputs/separators.gr", True)
        expected_tokens = [
            ('SEPARATOR', ';', 1), ('SEPARATOR', ',', 2), ('SEPARATOR', ':', 3)
        ]
        self.assertEqual(tokens[:3], expected_tokens)

    def test_lexer_tokenizes_equal_sign_correctly(self):
        tokens = perform_lexical_analysis("tests/lexer_inputs/equal_sign.gr", True)
        expected_tokens = [
            ('RELATIONAL_OPERATOR', '=', 1)
        ]
        self.assertEqual(tokens[:1], expected_tokens)

    def test_lexer_handles_wrong_path(self):
        with self.assertRaises(FileNotFoundError):
            tokens = perform_lexical_analysis("tests/lexer_inputs/non_existent_file.gr",True)
