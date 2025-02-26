import os

def combine_files(output_file, *input_files):
    combined_content = "import argparse\n"
    for file in input_files:
        with open(file, 'r') as f:
            content = f.read()
            # Remove local import statements
            content = '\n'.join(
                line for line in content.split('\n')
                if not line.startswith('import ') and not line.startswith('from ')
            )
            combined_content += content + "\n\n"

    with open(output_file, 'w') as f:
        f.write(combined_content)

combine_files('combined_compiler.py', 'src/lexer.py', 'src/parser.py', 'src/compiler.py')