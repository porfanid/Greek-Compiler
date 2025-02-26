import argparse
from lexer import Lexer
from parser import Parser

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process a source code file.')
    parser.add_argument('file', type=str, help='The source code file to process')
    args = parser.parse_args()


    lexer = Lexer(args.file)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    parser.parse()