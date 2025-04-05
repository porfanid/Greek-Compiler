import sys
import os
# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from src.intermediate import IntermediateCodeGenerator
from src.compiler import get_intermediate_code
from src.symboltable import build_symbol_table

class TestIntermediateCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.code_gen = IntermediateCodeGenerator()

    def test_gen_quad(self):
        self.code_gen.gen_quad('ADD', 'x', 'y', 'z')
        expected_quad = (0, 'ADD', 'x', 'y', 'z')
        self.assertEqual(self.code_gen.quads[0], expected_quad)

    def test_new_temp(self):
        temp1 = self.code_gen.new_temp()
        temp2 = self.code_gen.new_temp()
        self.assertEqual(temp1, 'T_0')
        self.assertEqual(temp2, 'T_1')

    def test_backpatch(self):
        self.code_gen.gen_quad('jump', '_', '_', '_')
        self.code_gen.backpatch([0], 10)
        expected_quad = (0, 'jump', '_', '_', 10)
        self.assertEqual(self.code_gen.quads[0], expected_quad)

    def test_quad_to_string(self):
        self.code_gen.gen_quad('ADD', 'x', 'y', 'z')
        quad_str = self.code_gen.quad_to_string((0, 'ADD', 'x', 'y', 'z'))
        self.assertEqual(quad_str, '0: (ADD, x, y, z)')

    def test_get_quads(self):
        self.code_gen.gen_quad('ADD', 'x', 'y', 'z')
        quads_str = self.code_gen.get_quads()
        self.assertEqual(quads_str, '0: (ADD, x, y, z)\n')

    def test_generate_intermediate_code_function(self):
        ast = {
            'type': 'PROGRAM',
            'children': [
                {'type': 'IDENTIFIER', 'value': 'test_program'},
                {'type': 'BLOCK', 'children': [
                    {'type': 'SUBPROGRAMS', 'children': [
                        {'type': 'FUNCTION', 'children': [
                            {'type': 'IDENTIFIER', 'value': 'increase'},
                            {'type': 'FORMAL_PARAMETERS', 'children': [
                                {'type': 'VAR_LIST', 'children': [
                                    {'type': 'IDENTIFIER', 'value': 'a'},
                                    {'type': 'IDENTIFIER', 'value': 'b'}
                                ]}
                            ]},
                            {'type': 'FUNCTION_BLOCK', 'children': [
                                {'type': 'SEQUENCE', 'children': [
                                    {'type': 'ASSIGNMENT', 'children': [
                                        {'type': 'IDENTIFIER', 'value': 'b'},
                                        {'type': 'EXPRESSION', 'children': [
                                            {'type': 'TERM', 'children': [
                                                {'type': 'NUMBER', 'value': '1'}
                                            ]}
                                        ]}
                                    ]}
                                ]}
                            ]}
                        ]}
                    ]}
                ]}
            ]
        }
        symbol_table = build_symbol_table(ast)
        quads = get_intermediate_code(ast, "test_program.int", symbol_table, True)
        expected_quads = [
            (0, 'begin_block', 'test_program', '_', '_'),
            (1, 'begin_block', 'increase', '_', '_'),
            (2, ':=', '1', '_', 'b'),
            (3, 'end_block', 'increase', '_', '_'),
            (4, 'halt', '_', '_', '_'),
            (5, 'end_block', 'test_program', '_', '_')
        ]
        self.assertEqual(quads, expected_quads)

class TestIntermediateCodeGeneration(unittest.TestCase):
    def test_generate_intermediate_code(self):
        ast = {
            'type': 'PROGRAM',
            'children': [
                {'type': 'IDENTIFIER', 'value': 'test_program'},
                {'type': 'BLOCK', 'children': [
                    {'type': 'SEQUENCE', 'children': [
                        {'type': 'ASSIGNMENT', 'children': [
                            {'type': 'IDENTIFIER', 'value': 'a'},
                            {'type': 'EXPRESSION', 'children': [
                                {'type': 'TERM', 'children': [
                                    {'type': 'NUMBER', 'value': '5'}
                                ]}
                            ]}
                        ]}
                    ]}
                ]}
            ]
        }
        symbol_table = build_symbol_table(ast)
        quads = get_intermediate_code(ast, "test_program.int", symbol_table, True)
        expected_quads = [
            (0, 'begin_block', 'test_program', '_', '_'),
            (1, ':=', '5', '_', 'a'),
            (2, 'halt', '_', '_', '_'),
            (3, 'end_block', 'test_program', '_', '_')
        ]
        self.assertEqual(quads, expected_quads)


    def test_generate_intermediate_code_function(self):
        ast = {
            'type': 'PROGRAM',
            'children': [
                {'type': 'IDENTIFIER', 'value': 'test_program'},
                {'type': 'BLOCK', 'children': [
                    {'type': 'SUBPROGRAMS', 'children': [
                        {'type': 'FUNCTION', 'children': [
                            {'type': 'IDENTIFIER', 'value': 'increase'},
                            {'type': 'FORMAL_PARAMETERS', 'children': [
                                {'type': 'VAR_LIST', 'children': [
                                    {'type': 'IDENTIFIER', 'value': 'a'},
                                    {'type': 'IDENTIFIER', 'value': 'b'}
                                ]}
                            ]},
                            {'type': 'FUNCTION_BLOCK', 'children': [
                                {'type': 'SEQUENCE', 'children': [
                                    {'type': 'ASSIGNMENT', 'children': [
                                        {'type': 'IDENTIFIER', 'value': 'b'},
                                        {'type': 'EXPRESSION', 'children': [
                                            {'type': 'TERM', 'children': [
                                                {'type': 'NUMBER', 'value': '1'}
                                            ]}
                                        ]}
                                    ]}
                                ]}
                            ]}
                        ]}
                    ]}
                ]}
            ]
        }
        symbol_table = build_symbol_table(ast)
        quads = get_intermediate_code(ast, "test_program.int", symbol_table, True)
        expected_quads = [
            (0, 'begin_block', 'test_program', '_', '_'),
            (1, 'begin_block', 'increase', '_', '_'),
            (2, ':=', '1', '_', 'b'),
            (3, 'end_block', 'increase', '_', '_'),
            (4, 'halt', '_', '_', '_'),
            (5, 'end_block', 'test_program', '_', '_')
        ]
        self.assertEqual(quads, expected_quads)
