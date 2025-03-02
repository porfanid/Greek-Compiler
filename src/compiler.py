import argparse
from lexer import Lexer
from intermediate import generate_intermediate_code
from final import generate_risc_v_code
from syntaxAST import Syntax
from os import path


def perform_lexical_analysis(file, debug):
    # Initialize the lexer with the provided source code file
    lexer = Lexer(file)
    # Tokenize the source code
    tokens = lexer.tokenize()
    if debug:
        print(tokens)
    return tokens


def perform_syntax_analysis(tokens, debug):
    # Initialize the parser with the generated tokens
    syntax = Syntax(tokens)
    # Parse the tokens to perform syntax analysis
    ast = syntax.parse()
    if debug:
        print(ast.to_dict())
    return tokens, ast


def get_intermediate_code(ast, int_file, debug):
    code_gen = generate_intermediate_code(ast)
    quads = code_gen.get_quads()
    if debug:
        print(quads)
    with open(int_file, 'w') as f:
        f.write(quads)
    return code_gen.quads

def get_riscv_code(quads, riscv_file, debug):
    risc_v_code = generate_risc_v_code(quads)
    # Output the code to a file
    with open(riscv_file, 'w', encoding='utf-8') as f:
        f.write(risc_v_code)

def get_file_extension(file_path):
    _, file_extension = path.splitext(file_path)
    return file_extension


def compile_file(file, debug):
    #Get the file extension
    file_extension = get_file_extension(file)
    # Perform lexical analysis on the provided source code file
    tokens = perform_lexical_analysis(file, debug)
    # Perform syntax analysis on the generated tokens
    tokens, ast = perform_syntax_analysis(tokens, debug)
    # Generate intermediate code from the parsed AST
    quads = get_intermediate_code(ast.to_dict(), file.replace(file_extension, '.int'), debug)
    # Generate RISC-V assembly code from the intermediate code
    get_riscv_code(quads, file.replace(file_extension, '.asm'), debug)
    return quads

if __name__ == '__main__':
    # Create an argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description='Process a source code file.')
    # Add a positional argument for the source code file to process
    parser.add_argument('file', type=str, help='The source code file to process')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    # Parse the command-line arguments
    args = parser.parse_args()
    # Compile the provided source code file
    compile_file(args.file, args.debug)
