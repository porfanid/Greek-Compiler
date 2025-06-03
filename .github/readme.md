
# Greek Programming Language Compiler

This project is a compiler for a custom programming language with Greek keywords. It includes a lexer, parser, and unit tests to ensure the correctness of the implementation. Ypou can find the rules of the language in the language rules folder

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Lexer**: Tokenizes the source code into meaningful symbols.
- **Parser**: Analyzes the tokenized input to ensure it follows the language's grammar.
- **Unit Tests**: Ensures the correctness of the lexer and parser.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/porfanid/greek-compiler.git
    cd greek-compiler
    ```

2. Create a virtual environment and install dependencies:
    ```sh
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

To run the compiler on a Greek source file:
```sh
python compiler.py path/to/source.gr
```

## Testing

Unit tests are provided to ensure the correctness of the lexer and parser.

To run all tests:
```sh
python -m unittest discover -s tests
```

To run a specific test:
```sh
python -m unittest tests/test_lexer.py
```

## CI/CD

This project uses GitHub Actions for continuous integration and continuous deployment. Each unit test has its own workflow file.

- `test_lexer.yml`: Runs the lexer unit tests.
- `test_parser.yml`: Runs the parser unit tests.
- `test_main.yml`: Runs the main function tests.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
