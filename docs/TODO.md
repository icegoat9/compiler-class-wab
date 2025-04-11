Running notes-to-self document during and after class.

# Current Status

The compiler runs and produces the desired result on all the test programs in [/programs/test_programs](/programs/test_programs), with these exceptions:
* for_redeclare.wb
* badbrace.wb
* badparen.wb

See [/programs/](/programs/) for longer sample programs using the language.

### Language Compatibility
See [Wabbish-Specification.md](Wabbish-Specification.md) for details, but generally:
* i32 datatype
* Binary math operators +,-,*,/
* Comparison operators <,>,<=,>=,==,!=
* Unary math operator (- only)
* LLVM code generation
* while, for, and if structures (including if..elif..else)
* functions with one or more arguments
* hooks to a few I/O functions (print, command-line arguments)

### Helpful Compiler Features
* Line and column numbers returned in parser error messages (though not in downstream compiler messages)

# Future work / TODOs

I kept quick and dirty during-class To-Dos and also in quick TODO items at the top of each of the Python compiler programs.

## Future Compiler / Language Feature Ideas

(some ideas fleshed out in more detail in [Future-Specification.md](Future-Specification.md))

* [x] Optional value assignment on variable declaration
* [x] Expression statements (e.g. call function without assigning return)
  * [ ] Test in more depth, and remove caution in specification doc once more tested
* [x] Implement modulo operator %
  * [ ] Revise implementation to implement Floored vs. Truncated modulo for negative numbers
* [ ] Expression inside conditional
* [ ] Check for mismatched braces and parens in AST, throw a usefully specific compile error
* [x] Zero-parameter functions
  * [ ] Test in more depth
* [ ] RND(int)
* [ ] Look into other runtime.c integration with OS
  * [x] command-line arguments for compiled binaries
  * [ ] simple terminal/keypress input reading (number entry or arrow keys?)
    * [~] scanf wrapper to compile in
    * [~] add _int_scanf() LLVM definition to LLVM program header in llvmformat
    * [~] generate stack and register calls for Input() in llvmcode
    * [ ] add definition of INPUT() expression in model.py
    * [ ] handle INPUT() in all earlier compiler passes
    * [ ] add compile_ast command-line arg, or move input (and args?) into helper.c
    * [ ] add tests, support in formatter, etc
  * [ ] Add some sort of #include or #link directive or companion build file, that lets compile.sh know which helper.c, args.c, ... files to link in
    * [ ] Or generate this after tokenizing based on presence of specific tokens (e.g. if INPUT or argc or PRINT is present, generate some linking file that compile.sh will use)
* [x] for loops (via a similar approach to ifelse.py where they would be rewritten as while() loops early in the compiler passes so later compile steps don't need to understand them)
  * [x] improve syntax to remove third ; and/or shift to commas?
  * [x] drastically simplify syntax to e.g. `for i=1,10 { }`, perhaps?
  * [ ] fix compile error if loop variable is previously declared in scope (or make local in scope?), or perhaps a more general-purpose compiler pass to strip duplicate declarations?
* [ ] more robust error messages (especially at the parser level)
* [ ] fixed-length array support
  * [ ] length function
  * [ ] `for x in array` type iterator? (can start with `for i=1,len(array) {}`)
* [x] Basic string literal (perhaps not even valid as variable data, just as argument to special function printstr() which is parsed expecting a string literal, and generating LLVM const string header.
  * [ ] optionally, printstr() doesn't automatically append a newline? Add way to add that? e.g. a separate printnewline function to call? A special character? A backslash char?
  * [ ] optionally, "print" overloaded to mean printstr or printint depending on parsing (is it followed by strconst or not)
* [ ] Explore type support beyond int (float, char, maybe string)
  * [ ] Simpler fixed-length string using array functionality 
  * [ ] Build left(), right(), substr(), and so on in user space functions
* [ ] Explore syntax-checking tokenizer
* [ ] Look into operator precedence, with a cleanup step after tokenizing and before parsing to insert parentheses around math ops? Started to look at this, tricky
* [~] Look into writing a transpiler from Wabbish -> Lua, Python or another language (through this AST-manipulation model and then an AST -> Python/Lua/etc generator, as we did for LLVM)

## More Testing
* [ ] Add more assertion tests all through the compiler, including unary operators
* [ ] Add a top level unit tests function which runs the tests within each module? (move those from main() to a test_module() in each)?
* [X] Start to add some unit tests with asserts for various individual modules, taking crafted Programs in and out
* [ ]    Add one big integration test using compile()?
* [ ]    Write 'assert !=' or 'assert specific Exception' tests for other edge cases, erroneous code, etc?

## General Learning / Reading

* [ ] Read the Crafting Interpreters book, see what ideas it inspires
* [ ] Dig into generating machine code without LLVM (e.g. ARM64 or Webassembly), at least for a simple program to understand it
* [ ] LSP (Language Server Protocol)
* [ ] IDE integration w/ AST
* [ ] Python
  * [ ] [Enums](https://docs.python.org/3/library/enum.html#module-enum), including new functionality / syntax in 3.11 that someone in class mentioned: StrEnum? ('uses value not name of the enum member')
  * [ ] Python ... operator
* [ ] PEG grammars

## Bug fixing and related
* [ ] For loop variable redeclare issue noted above
* [ ] Decide on (currently undefined) behavior of variables initialized without assignment and then used before assignment -- should compiler catch this?
* [ ] Look into the list.reverse() quickly added in llvmcode.py to get functions with multiple arguments to work
    ...was the error in function arguments there? Or is this a workaround for a mistake with argument orderIn an earlier step? Verify what order the function argument should be on the stack in

## Cleanup

### Functional Cleanup (e.g. refactors)

* [ ] Is it cleaner to remove substitution from parser.py, make it Negate() Op, later compiler pass swaps to Sub?
* [ ] Revisit Negate handling in foldconstants, expression_instructions and parser
      (for now, just rewrote at parser level, but maybe should process as a Negate() in the AST and only later transform that)
* [ ] Refactor code to use pprint where printing complex objects? Less relevant
* [ ] Improve format.py for STATEMENT and BLOCK: seeing `CALL(name='fact', n=1)` vs desired `CALL('fact',1)`
* [ ] Mostly fixed with __str__ or __repr__ in the relevant classes: broaden that approach to more classes?
* [X] General to all programs: add type hinting for function parameters and especially return values
* [ ] See notes in 03-19 class chat or discussions about needing overloading / special features if something can return multiple valid types
* [ ] Configure Pylance type checking to at least 'basic' level, resolve the ~74 reported static type checking errors (may need to subclass EXPR to an existing class, or have some 'type overloading' / multiple types.
   * [ ] Allow hinting, as for example a While() can contain a statement list or STATEMENT or BLOCK at various stages in the compile process)
* [ ] Low priority: Eliminate sometimes-redundant return 0 at end of function (only for simple case where last line in function is a return-- not trying to intelligently parse all if/else structures to determine if each returns)

### Non-functional cleanup

* [ ] Go through existing code reading TODO/HACK comments and pull them up into this top-level TODO (as bugs or cleanup or refactors)
* [x] Document what I've done so far at the module level and high-level, so I'll remember it if I come back
* [~] Add some basic Python doc strings so my IDE can give me helpful tips as I come back
* [~] Add at least a few assert-style unit tests to all existing modules (some have these, some were just debugged with 'print debugging' and visual inspection of formatted output along the way)
* [X] For each file, an overall blurb about what it does, with inputs and outputs
* [ ] Reformat files w/ Python formatter and longer line length (120?), or other settings for large class objects in unit tests
* [X] Use pretty-printer (colorful, other?) for Program objects, etc-- pprint or other? At least in compile.py
* [x] Fork or copy to personal repo for future work
* [X] Add whatever """foo""" docstrings are useful for VScode popup help at both module and function level
* [ ] Rename top-level functions in all modules to consistent "verb_program()", "verb_statements()", and so on
* [ ] Refactor use of printcolor() and print() to use helper function print_colorheader()
* [ ] Standardize use of printcolor (on headings vs on code bodies) across all __main__ areas
* [ ] Standardize each module having a 'printexamples' flag and global var vs. just assert tests
      (basically, reinstate the commented-out print() statements in the `if __main__` self-test code, but hide behind a print flag)

## Older during-class todo (obsolete):
* [X] Parser testing on programs w/ file
* [X] Clean up tokenizing of == vs = (operator chars iterate)
* [X] Blocks and Statements work (tough)
* [X] Write some programs of my own...
* [x] Snapshots / examples of a program all the way through the compilation process at each step...
* [x] Copy code from Wab to Wabbi / Wabbit folders, extract previous Wab commit checkpoint
* [X] New mathops and relations
* [X] Unary - (at least first pass)
* [X] Optional Else clause
* [X] if..elseif..elseif..else -> nested if
* [x] for.. -> while

