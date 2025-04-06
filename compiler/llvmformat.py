# llvmformat.py
"""Convert nearly-final compiled Program() object to LLVM text format, to feed into Clang.

Nearly all the compilation logic has already happened in previous compiler passes.
This adds header statements to the file and some type definition for functions and globals,
as well as adding human-readable formatting such as block indents.

Previous compiler pass: llvmentry.py"""
#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [ ] assertion-based unit tests (somewhat brittle as part of this is human-readable formatting that could change)

from model import *
from printcolor import *

def format_llvm(program : Program) -> str:
    output = [ 'declare i32 @_print_int(i32)' ]
    # output = [ 'declare i32 @_print_int(i32)', 'declare i32 @_scan_int()' ]
    for s in program.statements:
        match s:
            case GlobalVar(name):
                output.append(f'@{name.str} = global i32 0')
            case Function(name, params, body):
                pstr = ', '.join([f'i32 %{p.str}' for p in params])
                output.append(f'\ndefine i32 @{name.str}({pstr}) {{')
                for block in body:
                    output.append(f'{block.label}:')
                    for inst in block.instructions:
                        output.append(f'    {inst.op}')
                output.append('}')
    return '\n'.join(output)

######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    printcolor("no unit tests defined", ansicode.yellow)
#    printcolor("tests PASSED", ansicode.green)
