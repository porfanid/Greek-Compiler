import argparse
from lexer import Lexer
from parser import Parser

if __name__ == '__main__':
    # Create an argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description='Process a source code file.')

    # Add a positional argument for the source code file to process
    parser.add_argument('file', type=str, help='The source code file to process')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Initialize the lexer with the provided source code file
    lexer = Lexer(args.file)

    # Tokenize the source code
    tokens = lexer.tokenize()

    # Initialize the parser with the generated tokens
    parser = Parser(tokens)

    # Parse the tokens to perform syntax analysis
    parser.parse()