# Overview

I spent one intense week taking Dave Beazley's [Compiler Class](https://www.dabeaz.com/compiler.html), in which each student writes a [compiler](https://en.wikipedia.org/wiki/Compiler) from scratch, using no outside libraries[^1] or frameworks.

[^1]: Depending what we mean by "no outside libraries". The compiler we each wrote generates machine-agnostic LLVM assembly code, but if we want to run the result on our computer we still use Clang to compile this 'intermediate representation' assembly code down to the machine code for the specific chip architecture we're using.

I enjoyed the experience, learned a lot, and found it a bit brain-burning as well. By the end I'd written a working compiler from a simple language to assembly code. I'm sure it has various bugs and edge cases, and it certainly contains some hacky or non-ideal code-- but the experience was the real goal...

A quick taste of a few transformations in the compilation process of a single line of user code through machine instructions:

``` llvm
while x <= 10 {
 ...
while [LOAD_GLOBAL('x'), PUSH(10), LTE()] {
 ...
%.r2 = icmp sle i32 %.r1, 10
br i1 %.r2, label %L2, label %L3
 ...
subs	w8, w8, #10
cset	w8, gt
tbnz	w8, #0, LBB0_4
```

After the class I did some light cleanup and moved my work to this repo, to play around with in the future if inspiration strikes. (I also picked up a copy of [Crafting Interpreters](https://craftinginterpreters.com/) for some light reading.)

# Language

We wrote compilers for subsets of a small imperative programming language 'Wabbit' created by the course instructor, which includes expressions, variables, printing, basic flow control, and user-defined functions, allowing programs such as this:

``` c
// fib.wb -  Compute fibonacci numbers
func fib(n) {              // Custom function
    if n > 1 {             // Conditional
        return fib(n-1) + fib(n-2);  // Recursion
    }
    return 1;
}

var n = 0;                 // Variable declaration
while n < 30 {             // Looping
    print fib(n);          // Printing
    n = n + 1;             // Assignment
}
```

I implemented the core of this language, and experimented with adding some other features that seemed interesting. The [Wabbish Language Specification](docs/Wabbish-Specification.md) is a living document where I keep a full specification for the language this compiler supports.

# Usage

To compile a simple program that raises a number to a power (this also generates the intermediate LLVM assembly .ll  and machine code .s from the compilation, for inspection):

``` sh
./compile.sh programs/pow.wb 
programs/pow.exe                // computes and prints 3 ^ (2 + 2) = 81
```

``` sh
./run.sh programs/pow.wb        // combines both of the above steps
```
A work-in-progress prototype that partially compiles a program, then transpiles it to a minimal subset of Python, as a quick way of sanity-checking program logic for more complex programs.
``` sh
./gen_python.sh programs/pow.wb
```

# Design Approach

At a high level, a compiler is organized into a series of passes that each perform a task such as tokenizing, parsing, or code generation.

At a lower level, this is a 'nano-pass' compiler with dozens of passes. Each pass ingests the current program representation (i.e. its [Abstract Syntax Tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree)), performs one particular transformation or simplification of it (often in a recursive way, descending down into depths of nested `if`, `while`, and `function` structures), and returns the result. 

By running each of these passes in order, we eventually transform the text of the program into the equivalent assembly code.

This design approach makes it easier to design, debug, reason about, and test each step of the process, as each of these compiler passes is implemented as its own small program. I chose to develop in Python because I was comfortable working quickly in it.

## Compilation Steps

The most up-to-date list of compiler passes is in the source code of compile_ast.py, but here's a quick summary, with simplified explanations to remind myself where to look later:

| compiler pass | summary |
| ------------- | ------- |
| tokenize input | e.g. `"x=1"` -> `["x", "=", "1"]` |
| parse tokens | Convert into AST data structure, e.g. `["x", "=", "1"]` -> `[[Variable "x", Operator "=", Integer 1]]` |
| elif rewrite |  Rewrite `if..elif..else` blocks as nested `if..else` blocks (so that later compiler steps only need to understand if..else, not elif) |
| for rewrite |  Rewrite `for...` blocks as equivalent `while...` blocks (to allow use of for without later compiler steps needing to be modified to understand it) |
| fold constants |  Pre-compute math on constants (e.g. `4 * 5` -> `20`), repeat recursively as needed |
| deinit |  separate variable declaration from assignment, e.g. `var x = 1;` -> `var x; x = 1;` |
| unscript |  move many top-level statements into a `main()` function |
| resolve_scope |  infer and resolve variable scopes and make explicit in program representation (`global` and `local`) |
| default_returns |  add an explicit `return 0` to the end of all functions, which simplifies later steps |
| expr_instructions + statement_instructions |  convert expressions to the conceptually different stack machine representations, which are how low-level processor instructions operate (for example, rather than saying `ADD(X,2)`, you push 2 and the value of the register that represents x to the stack, then run the 'add' operator, which pulls the top two elements of the stack ) |
| block statements |  merge groups of statements into blocks with labels that can be used for assembly language's GOTO-style flow control |
| control flow |  convert if / while / function flow control to assembly code style GOTO / BRANCH structures  |
| LLVM codegen + other LLVM | Various passes to translate the program data structure (which by this point is "organized like assembly language") into the equivalent LLVM assembly code representation |

### Compile Passes by Example

[docs/compile_passes_example.md](docs/compile_passes_example.md) shows a simple program taken through each compile pass, and what the intermediate outputs look like.

# Next Steps

I kept a quick running [TODO list](docs/TODO.md) during and after the class with some ideas...
