# Fade

Fade is a small interpreted programming language built from scratch in Python.

The project focuses on understanding the core components of a programming language, including **lexical analysis, parsing, abstract syntax trees, interpretation, variables, control flow, loops, and runtime environments**.

Fade is currently under active development, with new language features being added incrementally.

---

## Current Version

**V1.5 — Loop Language**

Fade currently supports:

- Integers and floating-point numbers
- Addition, Subtraction, Multiplication, and Division
- Operator precedence
- Parentheses and nested parentheses
- Unary `+`, `-` and `not` operators
- Comparison operators: `<`, `<=`, `>`, `>=`, `==`, `!=`
- Boolean operations: `and`, `or` and `not`
- Variable assignment
- A runtime environment for storing variables
- Multiple statement execution on a single line using `;`
- Control flow using: `if`, `else if`  and `else`
- Loops using: `repeat (...) {...}`, `repeat until (...) {...}`, `repeat {...} until (...)`
- `break` and `continue`
- File execution through `.fade` source files
- Command-line interface with `--tokens` and `--ast` debugging options
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
- **Result** — Produces the evaluated result of each executable statement or an appropriate error.

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
```
Fade/
├── examples/
│   ├── 001.integer_test.fade
│   ├── 002.float_test.fade
│   ├── 003.arithmetic_operation_test.fade
│   ├── 004.unary_test.fade
│   ├── 005.comparison_test.fade
│   ├── 006.variable_assignment_test.fade
│   ├── 007.semicolon_test.fade
│   ├── 008.control_flow_test.fade
│   └── 009.loop_test.fade
├── fade/
│   ├── __init__.py
│   ├── ast.py
│   ├── environment.py
│   ├── errors.py
│   ├── interpreter.py
│   ├── lexer.py
│   └── parser.py
├── README.md
└── fade.py
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

### `fade.py`

Provides the Fade command-line interface, including:
- Interactive REPL
- `.fade` file execution
- Token inspection with `--tokens`
- AST inspection with `--ast`

---

## How to Use

### Requirements

* Python 3.10 or newer

### Run the REPL

Open a terminal in the project directory and run:

```bash
python fade.py
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

### Run a Fade File

Execute a `.fade` source file with:

```bash
python fade.py examples/001.integer_test.fade
```

### Inspect Tokens

```bash
python fade.py examples/001.integer_test.fade --tokens
```

### Inspect the AST

```bash
python fade.py examples/001.integer_test.fade --ast
```

Both options can also be used together:

```bash
python fade.py examples/001.integer_test.fade --tokens --ast
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

V1.2 introduced the foundation for storing and reusing values through **variables**.

Added:

* Identifiers
* Variable assignment
* Variable environment
* Variable-based expressions
---
### V1.3 — Boolean Language

V1.3 introduced **boolean values, comparisons, and logical operations**.

Added:

* Keywords: `true`, `false`
* Comparison operations
* Logical operations: `and`, `or`, `not`
* `BooleanNode`
---
### V1.3.1 — Boolean Language Patch

V1.3.1 focused on improving the internal representation and output handling of boolean expressions.

Updated:

* Returning Fade Nodes as output instead of raw Python values
* Bug fixes and stability improvements

---
### V1.4 — Control Flow

V1.4 introduced **control flow**, allowing Fade programs to make decisions based on conditions.

Added:

* Keywords: `if`, `else`
* AST nodes: `BlockNode`, `StatementNode`, `IfNode`
* Parser: `parse_block`, `parse_statements`, `parse_statement`, `parse_if`
* Interpreter support for: `BlockNode`, `StatementNode`, `IfNode`
* Semicolon-based statement separation for multiple statements on one line
---

### V1.4.1 — File Execution & CLI

V1.4.1 extended Fade beyond the interactive REPL by adding **source file execution and command-line options**.

Added:

* `.fade` source file execution
* Optional token output with `--tokens`
* Optional AST output with `--ast`
* Support for multiline Fade programs
* Newline-based statement separation for multiline source files
* `examples/` directory containing feature-specific test programs

### V1.5 — Loop Language

V1.5 introduced loops, allowing Fade programs to repeat operations and control the execution of repetitive tasks.

Added:

* Keywords: `repeat`, `until`, `break`, `continue`
* AST nodes: `ForLoopNode`, `WhileLoopNode`, `DoWhileLoopNode`, `BreakNode`, `ContinueNode`
* Parser: `chk_current_token_value`, `parse_repeat`, `parse_for_loop`, `parse_while_loop`, `parse_do_while_loop`
* Interpreter signals: `BreakSignal`, `ContinueSignal`
* Interpreter support for: `ForLoopNode`, `WhileLoopNode`, `DoWhileLoopNode`, `BreakNode`, `ContinueNode`
* JSON-based **AST** output
* Fixed the `if`/`else` multiline bug
* Test file for loop test `009.loop_test.fade`
* Changed output behavior from interpreting the entire program before displaying results to displaying outputs immediately after interpretation

## Development

Fade is still an evolving project. New language features will be added as development continues.

The language design and implementation may change as Fade grows.

---

## License

This project is currently being developed as a personal educational project.