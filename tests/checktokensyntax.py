# checktokensyntax.py

# Side experiment to look at whether scanning output of tokenizer.py is useful state to find syntax errors
#  (not in active use, only implemented a quick brace and paren check as an experiment)

# TODO:
# [ ] Integrate into tokenizer as a second pass, and if so...
# [ ] docstrings
# [ ] conceptual description / high-level comments
# [ ] assertion-based unit tests

# Add compiler/ sibling directory to sys.path so we can import the modules we want to test
#  (not necessarily best practice for project structure but this is a quick standalone test)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../compiler")))

from model import *
from printcolor import *
from tokenizer import *


def check_syntax_string(text: str):
    print("Checking syntax of")
    printcolor(text)
    check_syntax_errors(tokenize(text))


def check_syntax_errors(tokens: list[Token], debug=False) -> bool:
    # WIP experiment to find some common syntax errors before parsing
    # TBD if this makes sense here vs. on the output of parser.py, though
    errors = False
    ## Mismatched parens and braces or interrupted ones
    bracedepth = 0
    parendepth = 0
    if debug:
        print("Checking syntax of: %s" % tokens)
    for token in tokens:
        match token.toktype:
            case "LBRACE":
                bracedepth += 1
                if parendepth != 0:
                    errors = True
                    print("Syntax Check Error on line %d: { seen in middle of unclosed ()" % token.sourceline)
            case "RBRACE":
                bracedepth -= 1
                if parendepth != 0:
                    errors = True
                    print("Syntax Check Error on line %d: } seen in middle of unclosed ()" % token.sourceline)
            case "LPAREN":
                parendepth += 1
            case "RPAREN":
                parendepth -= 1
    if bracedepth != 0:
        errors = True
        print("Syntax Check Error: mismatched total # of {}")
    if bracedepth != 0:
        errors = True
        print("Syntax Check Error: mismatched total # of ()")
    return errors


check_syntax_string("{(2+(3+4))}")
check_syntax_string("func f(x) {\n  print(2+3;\n }\n print(5)")
