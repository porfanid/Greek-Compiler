# tests/test_parser.py
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import unittest
from src.lexer import Lexer
from src.parser import Parser

class TestParser(unittest.TestCase):
    def test_parser_correct(self):
        lexer = Lexer("./tests/correct.gr")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            result = parser.parse()
            self.assertTrue(result)
        except SyntaxError as e:
            self.fail(e)

    def test_parser_false(self):
        lexer = Lexer("./tests/false.gr")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            result = parser.parse()
            self.assertFalse(result)
        except SyntaxError as e:
            self.fail(e)

if __name__ == '__main__':
    unittest.main()