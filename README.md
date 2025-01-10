# Overview

I spent an intense week taking Dave Beazley's [Compiler Class](https://www.dabeaz.com/compiler.html), in which each student writes a [compiler](https://en.wikipedia.org/wiki/Compiler) from scratch, using no outside libraries[^1] or frameworks.

[!NOTE]
TODO: Include simple image or code block of code in -> assembly out

I deeply enjoyed the experience, learned a lot, found it a bit brain-burning, and by the end had written a fully working[^2] compiler in Python for a simple language.

[^1]: Depending what we mean by "no outside libraries". The compiler we each wrote generates machine-agnostic LLVM assembly code, but if we want to run the result on our computer we still use Clang to compile this 'intermediate representation' assembly code down to the machine code for the specific chip architecture we're using.

[^2]: Well... 'Fully Working' meaning the compiler passed every test I threw at it and produced correct-looking assembly when inspected by eye on those test cases, and I was able to write a few programs using it... but it may have bugs or edge cases, and the code certainly contains some non-ideal, hacky, or just-good-enough-for-now ways of doing things-- it was only a one week project, after all.

After the class I did some light cleanup and moved my work to this repo for potential future playing around.

# Language

We wrote compilers for subsets of a small imperative programming language 'Wabbit' by the course instructor, including expressions, variables, printing, basic flow control, and user-defined functions, allowing programs such as this:

```
// fib.wb -  Compute fibonacci numbers

// A function declaration
func fibonacci(n int) int {
    if n > 1 {              // Conditionals
        return fibonacci(n-1) + fibonacci(n-2);
    } else {
        return 1;
    }
}

var n int = 0;             // Variable declaration
while n < 30 {             // Looping (while)
    print fibonacci(n);    // Printing
    n = n + 1;             // Assignment
}
```


The [Wabbish Language Specification](Wabbish-Specification.md) is a living document containing the specification for the language my compiler supports (the syntax and list of valid operators, expressions, statements, and so on).

# Design Approach

At a high level, the compiler is organized into a series of passes that each perform a task such as tokenizing, parsing, or code generation.

At a lower level, it is a 'nano-pass' compiler with dozens of steps. Each pass ingests the current program representation (i.e. its [Abstract Syntax Tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree)), performs one particular transformation or simplification of it (often in a recursive way, descending down into depths of nested `if`, `while`, and `function` structures), and returns the result. 

By running each of these passes in order, you eventually transform the text of the program into the equivalent assembly code.

This design approach makes it easier to design, debug, reason about, and test each step, as each of these compiler passes is implemented as its own small Python program in its own file.

## Compilation Steps

These are most of the passes the compiler performs, with simplified explanations to remind myself later-- there are many additional details and steps documented in the relevant code.

* "tokenize input text" (e.g. `"x=1"` -> `["x", "=", "1"]`)
* "parse tokens" into data structure (e.g. `["x", "=", "1"]` -> `[[Variable "x", Operator "=", Integer 1]]`)
* "elif rewrite": Rewrite `if..elif..else` blocks as nested `if..else` blocks (so that later compiler steps only need to understand if..else, not elif)
* "fold constants": Pre-compute math on constants (e.g. `4 * 5` -> `20`), repeat recursively as needed
* "deinit": separate variable declaration from assignment (e.g. `var x = 1;` -> `var x; x = 1;`)
* "resolve": infer and resolve variable scopes and make explicit in program representation (`global` and `local`)
* "unscript": move certain top-level statements to a `main()` function
* "default_returns": add an explicit `return 0` to the end of all functions, which simplifies later steps
* "expr_instructions": convert expressions to the conceptually different stack machine representations, which are how low-level processor instructions operate (for example, rather than saying x + 2, you push 2 and the current value of x to the stack, then run the 'add' operator, which pulls the top two elements of the stack)
* "block statements": merge groups of statements into blocks with labels that can be used for assembly language's GOTO-style flow control
* "block flow": convert if / while / function flow control to assembly code style GOTO / BRANCH structures 
* "LLVM codegen" (multiple steps): translate various data structures (which by this point are "organized like assembly language") into the equivalent LLVM assembly code representation
* "LLVM function entry": add LLVM variable initialization code to assembly code function blocks



