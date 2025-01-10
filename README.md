This folder holds most of my work from the one-week intensive [compiler class](../docs/README.md), and this is quick documentation of its current status. This isn't a public repo so these are mostly notes-to-self

## Language compatibility

I finished about the middle of [Part 2 of the class](../docs/README.md#part-2--the-wabbi-language), and this compiler supports something between the Wab and [Wabbi language specs](../docs/Wabbi-Specification.md), with some side-project additions. In particular, it nominally supports:

* i32 datatype
* Binary math operators +,-,*,/
* Comparison operators <,>,<=,>=,==,!=
* Unary math operator (- only)
* LLVM code generation
* if and while structures 
  * if clauses with optional else
* functions with one or more arguments
* if clauses with one or more elif clauses
  * e.g. if x < 2 { print(3) } elif x==2 { print(2) } else { print(1) }
* line and column numbers returned in parser error messages (though not downstream compiler messages)

It does not (yet?) support from the Wabbi spec:
* Optional value assignment on variable declaration, expression statements

I'm sure it also has a range of corner-case bugs given the one-week focus on learning and implementing.

## Example Programs

It compiles and runs all the test programs in [tests/](tests/)

See [programs/](programs/) for some sample programs I've written in the language.

## Future work / TODOs

I kept quick and dirty during-class To-Dos and also in quick TODO items at the top of each of the Python compiler programs. High-level, I want to do some cleanup and documentation of what I did and what felt especially hacky / expedient to get the compiler working while it's fresh in my mind, and consolidate maybe-some-day TODOs here:

**Near-term cleanup**
* Document what I've done so far at the module level and high-level, so I'll remember it if I come back
* Add some basic Python doc strings so my IDE can give me helpful tips as I come back
* Add at least a few assert-style unit tests to existing modules (some have these, some were just debugged with 'print debugging' and visual inspection of formatted output along the way)
* Go through existing code reading TODO/HACK comments and pulling them up into a top-level TODO

**Bigger picture: future compiler / language feature interest**
* the missing Wabbi language features, above
* for loops (via a similar approach to ifelse.py where they would be rewritten as while() loops early in the compiler passes so later compile steps don't need to understand them)
* more robust error messages (especially at the parser level)
* Explore type support (float, char, maybe string)
  * Maybe a simpler fixed-length string, via implementing fixed-length-only array support
* Look into other runtime.c integration with OS-- for example, simple keystroke input support
* Dig into generating assembly (e.g. ARM64, Webassembly, other) at lest for a simple program
* Read the Crafting Interpreters book, see what it inspires
* Look into writing a transpiler from Wabbi -> Lua, Python or another language (but through this AST-manipulation model and then an AST -> Python/Lua/etc generator, as we did for LLVM)
* [ ] Explore syntax-checking tokenizer
* [ ] Look into operator precedence, with a cleanup step after tokenizing and before parsing to insert parentheses around math ops? Started to look at this, tricky
* [ ] LSP (Language Server Protocol)
* [ ] IDE integration w/ AST

**Post-class cleanup (while fresh in mind)**
* [ ] Rewrite all individual file TODOs, notes, memory, issues, etc while fresh in mind
* [X] For each file, an overall blurb about what it does, with inputs and outputs
* [ ] Reformat files w/ Python formatter and longer line length (120?), or other settings for large class objects in unit tests
* [ ] Fork or copy to personal repo for future work
* [X] Add whatever """foo""" docstrings are useful for VScode popup help at both module and function level

Lower priority cleanup:
* [ ] Configure Pylance type checking to at least 'basic' level, resolve the ~74 reported static type checking
      errors (may need to subclass EXPR to an existing class, or have some 'type overloading' / multiple types
      allowed hinting, as for example a While() can contain a statement list or STATEMENT or BLOCK at various
      stages in the compile process)
* [ ] Rename top-level functions in all modules to consistent "verb_program()", "verb_statements()", and so on
* [ ] Refactor use of printcolor() and print() to use helper function print_colorheader()
* [ ] Standardize use of printcolor (on headings vs on code bodies) across all __main__ areas
* [ ] Maybe standardize each module having a 'verbose' or 'printexamples' flag and global var vs. just assert tests
      (basically, reinstate the commented-out print() statements in the if __main__ bodies, but hide behind a print flag)
* [X] Rewrite this top-level to-do list

**General during-class todo (a bit out of date)**
* [X] Parser testing on programs w/ file
* [X] Clean up tokenizing of == vs = (operator chars iterate)
* [X] Blocks and Statements work (tough)
* [ ] Look into the list.reverse() quickly added in llvmcode.py to get functions with multiple arguments to work
    ...was the error in function arguments there? Or is this a workaround for a mistake with argument orderIn an earlier step? Verify what order the function argument should be on the stack in
* [X] Write some programs of my own...
* [ ] Snapshots / examples of a program all the way through the compilation process at each step...
* Cleanup Wab features:
  * [ ] Eliminate redundant returns, etc, 
* Implement Wabbi features:
  * [X] New mathops and relations
  * [X] Unary - (at least first pass)
  * [ ]   Is it cleaner to remove substitution from parser.py, make it Negate() Op, later compiler pass swaps to Sub?
  * [X] Optional Else clause
  * [ ] Expression statements (e.g. call function without assigning return)
  * [ ] Expression inside conditional
  * [ ] Declare var without assignment
* [ ] Copy code from Wab to Wabbi / Wabbit folders, extract previous Wab commit checkpoint
* Add more flow control structures, parsed and converted to simpler ones early in process
  * [X] if..elseif..elseif..else -> nested if
  * [ ] for.. -> while
* Wabbit features:
  * [ ] Types (especially string, perhaps?)
* [ ] Add more assertion tests all through the compiler, including unary operators
* [ ] Add a top level unit tests function which runs the tests within each module? (move those from main() to a test_module() in each)?
* [ ] Revisit Negate handling in foldconstants, expression_instructions and parser
      (for now, just rewrote at parser level, but maybe should process as a Negate() in the AST and only later transform that)
* [X] Use pretty-printer (colorful, other?) for Program objects, etc-- pprint or other? At least in compile.py
* [ ] Refactor code to use pprint where printing complex objects? Less relevant
* [ ] Improve format.py for STATEMENT and BLOCK: seeing `CALL(name='fact', n=1)` vs desired `CALL('fact',1)`
* [ ]   Mostly fixed with __str__ or __repr__ in the relevant classes: broaden that approach to more classes?
* [X] General to all programs: add type hinting for function parameters and especially return values
* [ ] See notes in 03-19 class chat or discussions about needing overloading / special features if something can return multiple valid types)
* [X] Start to add some unit tests with asserts for various individual modules, taking crafted Programs in and out
* [ ]    Include test programs from Wab3 Resolved near bottom of page?
* [ ]    Add one big integration test using compile()?
* [ ]    Write 'assert !=' or 'assert specific Exception' tests for other edge cases, erroneous code, etc?
* [X] Handle empty if / else / while statement lists?

**General Reading**
* Python
  * [Enums](https://docs.python.org/3/library/enum.html#module-enum), including new functionality / syntax in 3.11 that people were talking about-- StrEnum? ('uses value not name of the enum member')
  * Python ... operator
* Crafting Interpreters book
* PEG grammars
