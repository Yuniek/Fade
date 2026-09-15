# Fade

Fade is a small interpreted programming language built from scratch in Python.

The project focuses on understanding the core components of a programming language, including **lexical analysis, parsing, abstract syntax trees, interpretation, variables, and runtime environments**.

Fade is currently under active development, with new language features being added incrementally.

---

## Current Version

**V1.4 — Control Flow**

Fade currently supports:

- Integers and floating-point numbers
- Addition, Subtraction, Multiplication, and Division
- Operator precedence
- Parentheses and nested parentheses
- Unary `+`, `-` and `not` operators
- Comparison operators: `<`, `<=`, `>`, `>=`, `==`, `!=`
- Boolean operations: `and`, and `or`
- Variable assignment
- A runtime environment for storing variables
- Multiple Statement execution in single line by separating via  semicolon `;`
- Control Flow using: `if`, `else if`  and `else`
- Lexical, Syntax, and Runtime error handling
- An interactive REPL

### Example

```text
fade > 12   
12
fade > 12.3
12.3
fade > 1+2-3*4/5
0.6000000000000001
fade > +4
4
fade > -5
-5
fade > not true
false
fade > not false
true
fade > 5<=5
true
fade > 5<5
false
fade > 5<5 or 5==5
true
fade > 5<5 and 5==5
false
fade > x=10
fade > y=20
fade > x+15
25
fade > x*2;y*3
20
60
fade > if(x<y){x+y}else if (x==y){0} else {x-y}
30
fade > 
```

---

## How Fade Works

Fade processes source code through a simple interpreter pipeline:

```text
Source Code
↓
Lexer
↓
Tokens
↓
Parser
↓
AST
↓
Interpreter ----> Environment
↓
Result
```

Each stage has a specific responsibility:

- **Lexer** — Converts source code into a sequence of tokens.
- **Parser** — Converts tokens into an Abstract Syntax Tree (AST) while enforcing the language's grammar and operator precedence.
- **AST** — Represents the structure of the program as a tree of language constructs.
- **Interpreter** — Evaluates the AST according to Fade's semantics.
- **Environment** — Stores and retrieves variables during execution.
- **Result** — Produces the final evaluated value or an appropriate error.

### Lexer

The lexer reads the source code and converts it into **tokens** such as numbers, identifiers, operators, parentheses, etc.

### Parser

The parser processes those tokens according to Fade's syntax rules and builds an **Abstract Syntax Tree (AST)**.

The AST represents the structure of the code rather than the original text.

### Interpreter

The interpreter evaluates the AST and produces the result.

### Environment

The environment stores variables and their values during execution, allowing values to be reused in later expressions.

This structure gives Fade a foundation for adding more programming-language features over time.

---

## Project Structure

# Project Structure

# Project Structure

```
Fade/
├── fade/
│   ├── __init__.py
│   ├── ast.py
│   ├── environment.py
│   ├── errors.py
│   ├── interpreter.py
│   ├── lexer.py
│   └── parser.py
├── README.md
└── shell.py
```

### `fade/`

Contains the core implementation of the Fade language:

* Lexer
* Parser
* AST nodes
* Interpreter
* Environment
* Error handling
* `run()` function

### `shell.py`

Provides a simple **REPL (Read-Eval-Print Loop)** for interacting with Fade from the terminal.

---

## How to Use

### Requirements

* Python 3.10 or newer

### Run Fade

Open a terminal in the project directory and run:

```bash
python shell.py
```

You will see:

```text
fade >
```

You can then enter Fade code:

```text
fade > 10 + 5
15
```

To exit the REPL:

```text
fade > bye()
```

---

## Version History

### V1 — Arithmetic Language

The first working version established Fade's core language pipeline.

Introduced:

* Integer and floating-point numbers
* Basic arithmetic operators
* Operator precedence
* Parentheses
* Lexer
* Recursive-descent parser
* Abstract Syntax Tree
* Tree-walk interpreter
* Basic error handling
* Interactive REPL
---
##### V1.1 — Unary Operators

V1.1 extended the arithmetic system with **unary operators**.

Added:

* Unary `+`
* Unary `-`
* Chained unary operators
* Unary operators with parentheses
* Unary operators combined with binary expressions
* Improved REPL error handling
---
### V1.2 — Variable Language

V1.2 introduces the foundation for storing and reusing values through **variables**.

Added:

* Identifiers
* Variable assignment
* Variable environment
* Variable-based expressions
---
### V1.3 — Boolean Language

V1.3 introduces the foundation for storing and reusing values through **variables**.

Added:

* keywords (true, false)
* comparison operations
* and, or and not
* new boolean Node
---
### V1.3.1 — Boolean Language Patch.

V1.3.1 extended the foundation for storing and reusing values through **variables**.

This update completely focussed:
* Returning Fade Nodes as output instead of Python outputs.
* Fixing Bugs

---
### V1.4 — Control Flow

V1.4 introduces **control flow**, allowing Fade programs to make decisions based on conditions.

Added:

* keywords: `if`, `else`
* ast nodes: `BlockNode`, `StatementNode`, `IfNode`
* parser: `parse_block`, `parse_statements`, `parse_statement`, `parse_if`
* interpreter support for: `BlockNode`, `StatementNode`, `IfNode`
---

## Development

Fade is still an evolving project. New language features will be added as development continues.

The language design and implementation may change as Fade grows.

---

## License

This project is currently being developed as a personal educational project.