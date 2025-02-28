import subprocess
import filecmp
import unittest
import os


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
        # Run the original compiler
        self.run_compiler('src/compiler.py', self.input_file, self.original_output)
        # Run the combined compiler
        self.run_compiler('combined_compiler.py', self.input_file, self.combined_output)
        # Compare the outputs
        self.assertTrue(filecmp.cmp(self.original_output, self.combined_output), "Outputs do not match!")


    def tearDown(self):
        # Delete the output files
        if os.path.exists(self.original_output):
            os.remove(self.original_output)
        if os.path.exists(self.combined_output):
            os.remove(self.combined_output)
        if os.path.exists('combined_compiler.py'):
            os.remove('combined_compiler.py')
