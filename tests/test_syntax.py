# tests/test_parser.py
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from src.compiler import perform_syntax_analysis, perform_lexical_analysis

class TestSyntax(unittest.TestCase):
    def test_parser_correct(self):
        file = "./tests/syntax_inputs/correct.gr"
        tokens = perform_lexical_analysis(file, True)
        perform_syntax_analysis(tokens, True)

    def test_parser_false(self):
        file = "./tests/syntax_inputs/false.gr"
        with self.assertRaises(SyntaxError):
            tokens = perform_lexical_analysis(file, True)
            perform_syntax_analysis(tokens, True)

    def test_parser_missing_tokens(self):
        file = "./tests/syntax_inputs/missing_tokens.gr"
        with self.assertRaises(SyntaxError):
            tokens = perform_lexical_analysis(file, True)
            perform_syntax_analysis(tokens, True)

    def test_parser_incorrect_order(self):
        file = "./tests/syntax_inputs/incorrect_order.gr"
        with self.assertRaises(SyntaxError):
            tokens = perform_lexical_analysis(file, True)
            perform_syntax_analysis(tokens, True)

    def test_parser_nested_statements(self):
        file = "./tests/syntax_inputs/nested_statements.gr"
        tokens = perform_lexical_analysis(file, True)
        perform_syntax_analysis(tokens, True)
