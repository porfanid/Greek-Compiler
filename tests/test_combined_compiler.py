import subprocess
import unittest
import os

from src.final import generate_risc_v_code
from src.intermediate import generate_intermediate_code
from src.lexer import Lexer
from src.symboltable import build_symbol_table
from src.syntaxAST import Syntax


class TestCombinedCompiler(unittest.TestCase):


    def setUp(self):
        self.input_file = 'tests/syntax_inputs/correct.gr'
        self.original_output = 'original_output.txt'
        self.combined_output = 'combined_output.txt'
        # Check if the combined compiler file exists
        if not os.path.exists('combined_compiler.py'):
            # Run the combine script
            subprocess.run(['python', 'scripts/combine.py'])


    def run_compiler(self, compiler_path, input_file, output_file):
        with open(output_file, 'w') as out:
            subprocess.run(['python', compiler_path, "-d", input_file], stdout=out, stderr=subprocess.PIPE)


    def test_combined_compiler(self):
            # Setup test paths
            source_file = "./tests/syntax_inputs/correct.gr"

            # Step 1: Perform lexical analysis
            lexer = Lexer(source_file)
            # Tokenize the source code
            tokens = lexer.tokenize()

            # Step 2: Perform syntax analysis
            syntax = Syntax(tokens)
            # Parse the tokens to perform syntax analysis
            ast = syntax.parse()

            # Step 3: Generate symbol table
            symbol_table = build_symbol_table(ast.to_dict())

            # Step 4: Generate intermediate code
            code_gen = generate_intermediate_code(ast.to_dict(), symbol_table)
            quads = code_gen.get_quads()

            # Step 5: Generate RISC-V code
            risc_v_code = generate_risc_v_code(code_gen.quads, symbol_table)

            # Add assertions here to verify the output
            self.assertIsNotNone(quads)
            self.assertIsNotNone(risc_v_code)


    def tearDown(self):
        # Delete the output files
        if os.path.exists(self.original_output):
            os.remove(self.original_output)
        if os.path.exists(self.combined_output):
            os.remove(self.combined_output)
        if os.path.exists('combined_compiler.py'):
            os.remove('combined_compiler.py')
