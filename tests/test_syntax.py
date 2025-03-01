# tests/test_parser.py
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from src.compiler import perform_syntax_analysis


class TestSyntax(unittest.TestCase):
    def test_parser_correct(self):
        file =  "./tests/syntax_inputs/correct.gr"
        perform_syntax_analysis(file, True)

    def test_parser_false(self):
        file = "./tests/syntax_inputs/false.gr"
        with self.assertRaises(SyntaxError):
            perform_syntax_analysis(file, True)
