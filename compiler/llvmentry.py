# llvmentry.py
"""Small compiler pass to add LLVM entry code for function definitions.

Specifically, create a small 'entry block' with the LLVM code to store passed parameters in registers
that will serve as local variables within the function call.
"""
#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [ ] assertion-based unit tests (including one involving a function call with multiple parameters)

from model import *
from format import *
from printcolor import *

def llvm_entry_program(program: Program) -> Program:
    """Add LLVM entry code (see module doc) to all functions in program."""
    output = []
    for s in program.statements:
        match s:
            case GlobalVar() | StrConstNum():
                output.append(s)
            case Function(name, params, body):
                llvm_params = []
                allocate_code = []
                for p in params:
                    localarg = f".arg_{p.str}"
                    llvm_params.append(Name(p.wtype,localarg))
                    allocate_code.append(LLVM(f"%{p.str} = alloca i32"))
                    allocate_code.append(LLVM(f"store i32 %{localarg}, i32* %{p.str}"))
                allocate_code.append(LLVM(f"br label %{body[0].label}"))
                allocate_block = [BLOCK("entry", allocate_code)]
                output.append(Function(name, llvm_params, allocate_block + body))
            case _:
                raise SyntaxError(f"Unhandled statement type {s}")
    return Program(output)

######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    printcolor("no unit tests defined", ansicode.yellow)
#    printcolor("tests PASSED", ansicode.green)


