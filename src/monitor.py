import sys
import os
import psutil
import argparse
import time
from functools import wraps
from lexer import Lexer
from parser import Parser

# Add the src directory to the Python path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
print(path)
sys.path.insert(0, path)

def monitor_resources(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        memory_usage = []
        cpu_usage = []
        timestamps = []

        def collect_data():
            memory_usage.append(process.memory_info().rss/(8*1024))
            cpu_usage.append(process.cpu_percent(interval=None))
            timestamps.append(time.time() - start_time)
            print("memory: ",memory_usage,"cpu: ",cpu_usage,"timestamps: ",timestamps)

        start_time = time.time()
        collect_data()  # Collect initial data

        result = func(*args, **kwargs)

        collect_data()  # Collect final data

        return result

    return wrapper

@monitor_resources
def perform_syntax_analysis(file):
    # Initialize the lexer with the provided source code file
    lexer = Lexer(file)
    # Tokenize the source code
    tokens = lexer.tokenize()
    # Initialize the parser with the generated tokens
    parser = Parser(tokens)

    # Parse the tokens to perform syntax analysis
    parser.parse()

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