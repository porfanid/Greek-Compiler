# tests/test_parser.py
import unittest
from lexer import Lexer
from parser import Parser

class TestParser(unittest.TestCase):
    def test_parser(self):
        lexer = Lexer("./tests/correct.gr")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            parser.parse()
            self.assertTrue(True)
        except SyntaxError as e:
            self.fail(e)

if __name__ == '__main__':
    unittest.main()