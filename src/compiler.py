import argparse
from lexer import Lexer
from intermediate import generate_intermediate_code
from syntaxAST import Syntax


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


def compile_file(file, debug):
    # Perform lexical analysis on the provided source code file
    tokens = perform_lexical_analysis(file, debug)
    # Perform syntax analysis on the generated tokens
    tokens, ast = perform_syntax_analysis(tokens, debug)
    # Generate intermediate code from the parsed AST
    quads = get_intermediate_code(ast.to_dict(), file.replace('.gr', '.int'), debug)
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
