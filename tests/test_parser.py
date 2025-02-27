# tests/test_parser.py
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from src.compiler import perform_syntax_analysis


class TestParser(unittest.TestCase):
    def test_parser_correct(self):
        file =  "./tests/correct.gr"
        perform_syntax_analysis(file)

    def test_parser_false(self):
        file = "./tests/false.gr"
        with self.assertRaises(SyntaxError):
            perform_syntax_analysis(file)


if __name__ == '__main__':
    unittest.main()
