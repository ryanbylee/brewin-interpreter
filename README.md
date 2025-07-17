# Brewin Interpreter

This repository contains a reference implementation of an interpreter for the **Brewin** language used in UCLA's CS&nbsp;131 course.  The interpreter is implemented in Python and built in four progressive versions that correspond to the course projects.

## Repository Layout

```
p1/    # Version 1 – minimal interpreter
p2/    # Version 2 – adds functions and control flow
p3/    # Version 3 – adds reference parameters and basic lambdas
p4/    # Version 4 – adds closures and objects
```

Every version directory contains the following key modules:

- `intbase.py` – base `InterpreterBase` class and error definitions.
- `brewlex.py` / `brewparse.py` – lexer and parser built with [PLY](http://www.dabeaz.com/ply/).
- `element.py` – simple wrapper class used to represent AST nodes.
- `interpretervX.py` – implementation of the Brewin interpreter for that project.

The `ply/` directory is vendored so there are no external dependencies besides Python 3.

## Version Overview

### p1 – Version 1
- Handles integer and string variables.
- Supports basic assignment, `print`, and `inputi`.
- Simple arithmetic (`+`/`-`) with rudimentary error checking.

### p2 – Version 2
- Introduces user defined functions with their own local scope.
- Adds conditional statements (`if`/`else`) and `while` loops.
- Extends arithmetic to include multiplication, division and comparisons.
- Provides built‑in `inputs` for string input.

### p3 – Version 3
- Adds pass‑by‑reference parameters via `ref`.
- Supports boolean values and operations.
- Lambdas are represented as values, though they are not true closures.

### p4 – Version 4
- Implements proper first‑class functions and closures.
- Adds object creation (`@`) and method calls via `obj.method()`.
- Includes type coercion rules and a complete set of operators.

## Running
Each interpreter exposes a `run(program_string)` method which executes the Brewin program provided as a string.  Example using the final version:

```python
from p4.interpreterv4 import Interpreter

program = """
func main() {
    print(1 + 2);
}
"""

intr = Interpreter()
intr.run(program)
```

Running any `interpretervX.py` directly will execute a small demonstration program defined at the bottom of the file.

## License and Attribution
This repository is **not** released under an open‑source license.  It is provided for reference only.  The original code was written by [Carey Nachenberg](http://careynachenberg.weebly.com/) and the CS 131 teaching assistants.
