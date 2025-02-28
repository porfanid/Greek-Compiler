import argparse
from lexer import Lexer
from syntaxAST import Syntax
from parser import Parser


def perform_syntax_analysis(file):
    # Initialize the lexer with the provided source code file
    lexer = Lexer(file)
    # Tokenize the source code
    tokens = lexer.tokenize()
    # Initialize the parser with the generated tokens
    syntax = Syntax(tokens)

    # Parse the tokens to perform syntax analysis
    ast = syntax.parse()
    print(ast.to_dict())
    return tokens


if __name__ == '__main__':
    # Create an argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description='Process a source code file.')
    # Add a positional argument for the source code file to process
    parser.add_argument('file', type=str, help='The source code file to process')
    # Parse the command-line arguments
    args = parser.parse_args()
    # Perform syntax analysis on the provided source code file
    tokens = perform_syntax_analysis(args.file)
