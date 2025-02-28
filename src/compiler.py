import argparse
from lexer import Lexer
from syntaxAST import Syntax


def perform_syntax_analysis(file, debug):
    # Initialize the lexer with the provided source code file
    lexer = Lexer(file)
    # Tokenize the source code
    tokens = lexer.tokenize()
    if debug:
        print(tokens)
    # Initialize the parser with the generated tokens
    syntax = Syntax(tokens)

    # Parse the tokens to perform syntax analysis
    ast = syntax.parse()
    if debug:
        print(ast.to_dict())
    return tokens


if __name__ == '__main__':
    # Create an argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description='Process a source code file.')
    # Add a positional argument for the source code file to process
    parser.add_argument('file', type=str, help='The source code file to process')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    # Parse the command-line arguments
    args = parser.parse_args()
    # Perform syntax analysis on the provided source code file
    tokens = perform_syntax_analysis(args.file, args.debug)
