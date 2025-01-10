# test_compile_roundtrip.py

# load in a sample program and pass through whole compiler chain as an example,
#   showing intermediate formats along the way

# Add compiler/ sibling directory to sys.path so we can import the modules we want to test
#  (not necessarily best practice for project structure but this is a quick standalone test)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../compiler")))

import compile_ast
import format
import parser_ast
import tokenizer
import expression_instructions
from printcolor import *
import sys

# default files
filename = 'tests/program1.wb'
filename = 'tests/fact.wb'
filename = 'programs/sign.wb'

if len(sys.argv) > 1:
    filename = sys.argv[1]

with open(filename) as file:
    source = file.read()
    printcolor('--source code text--')
    print(source)
    tokens = tokenizer.tokenize(source)
    program = parser_ast.parse_program(tokens)
    program = compile_ast.compile(program, llvm_str_output = True, debug = True)

