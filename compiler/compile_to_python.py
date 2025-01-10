#compile_to_python.py

from model import *
from format import *
import deinit
import elif_rewrite
import foldconstants
import resolve_scope
import unscript
import defaultreturns
import argparse
import parser_ast
import gen_python
from printcolor import *
from pprint import pprint

def compile_python(program: Program, debug: bool = False) -> str:
    if debug:
        printcolor("--input AST representation from parser--")
        print(program)
    
    compile_fns = (("input from parser", "run through human-readable formatter", (lambda x:x)),
                   ("elif_rewrite", "rewrite if..elif.else clauses as nested if..else", elif_rewrite.elif_program),
                   ("fold constants", "pre-compute math on constants", foldconstants.fold_constants),
                   ("deinit", "separate variable declartion from assignment", deinit.deinit_variables),
                   ("resolve", "resolve variable scope and make explicit in data structure", resolve_scope.resolve_scopes),
                   ("unscript", "move top-level statements to main() except globalvar", unscript.unscript_toplevel),
                   ("defaultreturns", "add return 0 to functions, to simplify assembly codegen", defaultreturns.add_returns)
                   )

    for i,c in enumerate(compile_fns):
        program = c[2](program)
        if debug:
            printcolor("--compiler pass %d: %s %s(%s)" % (i, c[0], ansicode.reset, c[1]))
            print(format_program(program))

    programstr = gen_python.py_program(program)
    return programstr

if __name__ == "__main__":

    argparser = argparse.ArgumentParser(
        prog="compile.py",
        description="""Compile a Wab .wb program and pass through AST cleanup / rewrite steps, then translate to Python?""",
    )

    argparser.add_argument("filename", help="filename of Wab program")
    argparser.add_argument("-v", "--verbose", help="print output of intemediate process steps", action="store_true")
    args = argparser.parse_args()

    prog = parser_ast.parse_file(args.filename, debug=args.verbose)

    compiled = compile_python(prog, debug=args.verbose)
    print(f'# original source: {args.filename}\n' + compiled)
