# compile.py filename [-l] [-p] [-v] [-f]
"""Apply the full sequence of compiler 'micropasses' to transform the output of parser.py
into LLVM code ready to compile with Clang."""

# TODOs:
# [X] docstrings
# [X] clean up main function by having some loop over a data structure of "function to run: description"
# [ ] if called with no parameters, print the help
# [ ] maybe rename module to avoid overlap with Python compile(), change all references to it (ast_compile?)
# [X] deprecate translate_to_llvm_string wrapper and just call the function it calls?
# [X] conceptual description / high-level comments

from model import *
from format import *
import deinit
import strconst_enum
import elif_rewrite
import for_rewrite
import foldconstants
import resolve_type
import resolve_scope
import unscript
import defaultreturns
import argparse
import parser_ast
import expression_instructions
import statement_instructions
import basicblocks
import controlflow
import llvmcode
import llvmentry
import llvmformat
from printcolor import *
from pprint import pprint

def compile(program: Program, llvm_str_output: bool = True, debug: bool = False, argmode: bool = False) -> Program:
    """Apply the full sequence of compiler 'micro-passes', as transformations to the AST.
    
    Input is a freshed parsed Program AST (the output of parser.py), output is by default an
    LLVM program ready for Clang compilation. 
    
    However, if llvm_str_output = False, output is the fully compiled AST of LLVM instructions,
    without the final format-as-LLVM-program step, which may be useful for debugging.

    (WIP, unimplemented) If argmode is True, compile into a main function expecting
       arguments (to be passed from a C helper function linked in later)
    """
    if debug:
        printcolor("--AST input to compiler--")
        print(program)
        print()
        printcolor("-----------------------------------")
    
    compile_fns = (("input from parser", "run through human-readable formatter", (lambda x:x)),
                   ("elif_rewrite", "rewrite if..elif.else clauses as nested if..else", elif_rewrite.elif_program),
                   ("for_rewrite", "rewrite for loops as whiles", for_rewrite.for_program),
                   ("fold constants", "pre-compute math on constants", foldconstants.fold_constants),
                   ("resolve type", "assign types to expressions", resolve_type.resolve_types),
                   ("deinit", "separate variable declartion from assignment", deinit.deinit_variables),
                   ("strconst", "extract and uniquely number string constants", strconst_enum.strconst_program),
                   ("unscript", "move top-level statements to main() except globalvar and strconst", unscript.unscript_toplevel, argmode),
                   ("resolve", "resolve variable scope and make explicit in data structure", resolve_scope.resolve_scopes),
                   ("defaultreturns", "add return 0 to functions, to simplify assembly codegen", defaultreturns.add_returns),
                   ("expr_instructions", "expressions -> stack machine representation", expression_instructions.expr_program),
                   ("statement_instructions", "statements -> stack machine representation", statement_instructions.program_statement_instructions),
                   ("blocks statements", "merge statements into BLOCK data structures with labels", basicblocks.blocks_program),
                   ("block flow", "convert If/While/Func flow control to GOTO / BRANCH structure", controlflow.flow_program),
                   ("LLVM initial codegen", "convert pseudo state machine to LLVM instructions", llvmcode.llvm_program),
                   ("LLVM function entry", "add LLVM variable initialization code to functions", llvmentry.llvm_entry_program),
                   )

    for i,c in enumerate(compile_fns):
        if len(c) == 3:
            # most compiler passes take only the output of the previous pass as input
            program = c[2](program)
        elif len(c) == 4:
            # some passes take an extra argument
            program = c[2](program, c[3])
        if debug:
            printcolor("--compiler pass %d: %s %s(%s)" % (i, c[0], ansicode.reset, c[1]))
            print(format_program(program))

    if llvm_str_output:
        if debug:
            printcolor("--LLVM-compatible output--%s (convert our final internal data structure to string)" % ansicode.reset)
        programstr = llvmformat.format_llvm(program)
        print(programstr)
        return programstr

    return program

if __name__ == "__main__":

    argparser = argparse.ArgumentParser(
        prog="compile.py",
        description="""Compile a Wab .wb program and pass through AST cleanup / rewrite steps. 
            Note: not all formatting flags below are compatible with each other or with all processing steps.""",
    )

    argparser.add_argument("filename", help="filename of Wab program")
    argparser.add_argument("-v", "--verbose", help="print output of intemediate process steps", action="store_true")
    argparser.add_argument("-a", "--ast_output", help="leave output as AST not LLVM text format", action="store_true")
    argparser.add_argument("-c", "--cmd_args", help="support command-line args through wrapper to be linked in", action="store_true")
    argparser.add_argument("-p", "--prettyprint", help="(if ast_output) pretty-print final output", action="store_true")
    argparser.add_argument("-f", "--format_ast", help="(if ast_output) run output through AST formatter", action="store_true")
    args = argparser.parse_args()

    prog = parser_ast.parse_file(args.filename, debug=args.verbose)

    compiled = compile(prog, llvm_str_output=not(args.ast_output), debug=args.verbose, argmode=args.cmd_args)

    if args.prettyprint:
        pprint(compiled, width=120)
    elif args.format_ast:
        print(format_program(compiled))
