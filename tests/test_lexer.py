# tests/test_lexer.py
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from src.lexer import Lexer, TokenType


class TestLexer(unittest.TestCase):
    def test_lexer(self):
        lexer = Lexer("./tests/correct.gr")
        tokens = lexer.tokenize()

        expected_tokens = [('KEYWORD', 'πρόγραμμα', 1), ('IDENTIFIER', 'τεστ', 2), ('KEYWORD', 'δήλωση', 3), ('IDENTIFIER', 'α', 3), ('SEPARATOR', ',', 3), ('IDENTIFIER', 'β', 4), ('KEYWORD', 'δήλωση', 4), ('IDENTIFIER', 'γ', 5), ('KEYWORD', 'συνάρτηση', 6), ('IDENTIFIER', 'αύξηση', 6), ('GROUPING', '(', 6), ('IDENTIFIER', 'α', 6), ('SEPARATOR', ',', 6), ('IDENTIFIER', 'β', 6), ('GROUPING', ')', 6), ('KEYWORD', 'διαπροσωπεία', 8), ('KEYWORD', 'είσοδος', 8), ('IDENTIFIER', 'α', 9), ('KEYWORD', 'έξοδος', 9), ('IDENTIFIER', 'β', 10), ('KEYWORD', 'αρχή_συνάρτησης', 11), ('IDENTIFIER', 'β', 11), ('ASSIGNMENT', ':=', 11), ('IDENTIFIER', 'α', 11), ('OPERATOR', '+', 11), ('NUMBER', '1', 11), ('SEPARATOR', ';', 11), ('IDENTIFIER', 'αύξηση', 12), ('ASSIGNMENT', ':=', 12), ('IDENTIFIER', 'α', 12), ('OPERATOR', '+', 12), ('NUMBER', '1', 13), ('KEYWORD', 'τέλος_συνάρτησης', 16), ('KEYWORD', 'διαδικασία', 17), ('IDENTIFIER', 'τύπωσε_συν_1', 17), ('GROUPING', '(', 17), ('IDENTIFIER', 'χ', 17), ('GROUPING', ')', 17), ('KEYWORD', 'διαπροσωπεία', 19), ('KEYWORD', 'είσοδος', 19), ('IDENTIFIER', 'χ', 20), ('KEYWORD', 'αρχή_διαδικασίας', 21), ('KEYWORD', 'γράψε', 21), ('IDENTIFIER', 'χ', 21), ('OPERATOR', '+', 21), ('NUMBER', '1', 22), ('KEYWORD', 'τέλος_διαδικασίας', 23), ('KEYWORD', 'αρχή_προγράμματος', 25), ('IDENTIFIER', 'α', 25), ('ASSIGNMENT', ':=', 25), ('NUMBER', '1', 25), ('SEPARATOR', ';', 25), ('IDENTIFIER', 'β', 26), ('ASSIGNMENT', ':=', 26), ('NUMBER', '2', 26), ('OPERATOR', '+', 26), ('IDENTIFIER', 'α', 26), ('OPERATOR', '*', 26), ('IDENTIFIER', 'α', 26), ('OPERATOR', '/', 26), ('GROUPING', '(', 26), ('NUMBER', '2', 26), ('OPERATOR', '-', 26), ('IDENTIFIER', 'α', 26), ('OPERATOR', '-', 26), ('GROUPING', '(', 26), ('NUMBER', '2', 26), ('OPERATOR', '*', 26), ('IDENTIFIER', 'α', 26), ('GROUPING', ')', 26), ('GROUPING', ')', 26), ('SEPARATOR', ';', 26), ('IDENTIFIER', 'γ', 27), ('ASSIGNMENT', ':=', 27), ('IDENTIFIER', 'αύξηση', 27), ('GROUPING', '(', 27), ('IDENTIFIER', 'α', 27), ('SEPARATOR', ',', 27), ('REFERENCE', '%', 27), ('IDENTIFIER', 'β', 27), ('GROUPING', ')', 27), ('SEPARATOR', ';', 27), ('KEYWORD', 'για', 29), ('IDENTIFIER', 'α', 29), ('ASSIGNMENT', ':=', 29), ('NUMBER', '1', 29), ('KEYWORD', 'έως', 29), ('NUMBER', '8', 29), ('KEYWORD', 'με_βήμα', 29), ('NUMBER', '2', 29), ('KEYWORD', 'επανάλαβε', 30), ('KEYWORD', 'εκτέλεσε', 30), ('IDENTIFIER', 'τύπωσε_συν_1', 30), ('GROUPING', '(', 30), ('IDENTIFIER', 'α', 30), ('GROUPING', ')', 30), ('KEYWORD', 'για_τέλος', 31), ('SEPARATOR', ';', 31), ('IDENTIFIER', 'β', 33), ('ASSIGNMENT', ':=', 33), ('NUMBER', '1', 33), ('SEPARATOR', ';', 33), ('KEYWORD', 'όσο', 34), ('IDENTIFIER', 'β', 34), ('RELATIONAL_OPERATOR', '<', 34), ('NUMBER', '10', 34), ('KEYWORD', 'επανάλαβε', 35), ('KEYWORD', 'εάν', 35), ('IDENTIFIER', 'β', 35), ('RELATIONAL_OPERATOR', '<>', 35), ('NUMBER', '22', 35), ('KEYWORD', 'ή', 35), ('GROUPING', '[', 35), ('IDENTIFIER', 'β', 35), ('RELATIONAL_OPERATOR', '>=', 35), ('NUMBER', '23', 35), ('KEYWORD', 'και', 35), ('IDENTIFIER', 'β', 35), ('RELATIONAL_OPERATOR', '<=', 35), ('NUMBER', '24', 35), ('GROUPING', ']', 35), ('KEYWORD', 'τότε', 36), ('IDENTIFIER', 'β', 36), ('ASSIGNMENT', ':=', 36), ('IDENTIFIER', 'β', 36), ('OPERATOR', '+', 36), ('NUMBER', '1', 37), ('KEYWORD', 'εάν_τέλος', 38), ('KEYWORD', 'όσο_τέλος', 39), ('SEPARATOR', ';', 39), ('KEYWORD', 'διάβασε', 41), ('IDENTIFIER', 'β', 41), ('SEPARATOR', ';', 41), ('KEYWORD', 'επανάλαβε', 43), ('IDENTIFIER', 'β', 43), ('ASSIGNMENT', ':=', 43), ('IDENTIFIER', 'β', 43), ('OPERATOR', '+', 43), ('NUMBER', '1', 44), ('KEYWORD', 'μέχρι', 44), ('IDENTIFIER', 'β', 44), ('RELATIONAL_OPERATOR', '<', 44), ('OPERATOR', '-', 44), ('NUMBER', '100', 45), ('KEYWORD', 'τέλος_προγράμματος', 46), ('EOF', 'EOF', 46)]

        self.assertEqual(tokens, expected_tokens)


if __name__ == '__main__':
    unittest.main()