# tokenizer.py
"""Split input text into a series of tokens to feed to the parser."""
#
# TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests, especially for newer structures and tricky cases
# [X] Replace hideous hack for "==" token-- different way of looking for symbols
#     (originally put in place because the first '=' was being tokenized as ASSIGN before seeing the second =)
# [X] Add original source file line/column as token property, for better parser error messages
# [ ] Decide if it's cleaner to reverse key:value order in _symbols and _keywords
# [ ] Add more assertion tests for tricky or invalid tokenizer conditions
# [ ] Add a next stage 'tokenizer_sanitycheck' or similar to find common errors before parsing
#       (mismatched braces, missing ;, = vs == in conditional, etc-- see checktokensyntax.py and other)
# [ ] See TODO note below about n vs n+1 vs n+2 bounds checking

from model import *
from printcolor import *
from pprint import pprint
import os

_symbols = {
    "+": "PLUS",
    "*": "TIMES",
    "-": "SUB",
    "/": "DIV",
    "%": "MOD",
    "<": "LT",
    "==": "EQ",
    ">": "GT",
    "!=": "NEQ",
    "<=": "LTE",
    ">=": "GTE",
    "=": "ASSIGN",
    ";": "SEMI",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ",": "COMMA",
    "#": "HASH",
}

# chars to parse for symbols (manually keep up to date with chars used in symbols above)
_symbolchars = '+-*/%<>!=;(){},"#'

# creates dict of reserved keywords { "var": "VAR", ... } including types
_reswords = {x: x.upper() for x in ("var", "print", "if", "else", "while", "func", "return", "elif", "for", "include")}
_types = {x: x.upper() for x in ("int", "float", "char")}
_keywords = _reswords | _types

# create a quick reversed Token -> text dict ("LT": "<", etc) for symbols and keywords from the above,
#  for use in debugging and printing
_tempdict = _symbols | _keywords
token_text = dict([(value, key) for key, value in _tempdict.items()])


@dataclass
class Token:
    """Program token, example: Token("LBRACE", "{")

    .sourceline and .sourcecol track where in the original file it was parsed from, to allow the
    parser to emit more helpful error messages."""

    toktype: str
    tokvalue: str
    sourceline: int = 0  # experiment with tracking token to original source file line, for useful error messages
    sourcecol: int = 0


def token_list_eq(a: list[Token], b: list[Token]):
    """Check if two lists of tokens are equal, meaning the type and value fields
    match up, ignoring mismatch of irrelevant fields like sourceline."""
    #print(a,b) # DEBUG
    if len(a) != len(b):
        return False
    for i, toka in enumerate(a):
        tokb = b[i]
        if not token_eq(toka, tokb):
            return False
    return True


def token_eq(a: Token, b: Token):
    """Check it two tokens are equal, meaning same type and value fields.
    Ignore irrelevant fields like sourceline."""
    return a.toktype == b.toktype and a.tokvalue == b.tokvalue

def isfloat(s: str) -> bool:
    """Check if string s is a float literal (contains only numeric digits or a '.', 
    and the '.' cannot be the first character)"""
    for c in s:
        if c not in "0123456789.":
            return False
    if s.count(".") == 1 and s[0] != ".":
        return True
    
def tokenize(text: str) -> list[Token]:
    """Primary function to tokenize source into Token() objects for later parsing."""
    tokens = []
    sourceline = 1
    sourcecoldelta = 0  # difference between i and code column (reset on each newline)
    i = 0
    substr = ""
    while i < len(text):
        if text[i].isspace():
            if text[i] == "\n":
                sourceline += 1
                sourcecoldelta = i
            # skip ahead through whitespace
            i += 1
            continue
        substr += text[i]
        # TODO: set up test for this and the i+1<len() below and decide whether this needs to be
        #       i<, i+1<, i-1<, etc-- look into symbol at end of file
        if i < len(text) and text[i : i + 2] == "//":
            while i < len(text) and text[i] != "\n":
                i += 1
            substr = ""
            continue
        if substr.isnumeric() or isfloat(substr):
            while i + 1 < len(text) and (text[i + 1].isnumeric() or text[i + 1] == "."):
                i += 1
                substr += text[i]
            if isfloat(substr):
                tokens.append(Token("FLOAT", substr, sourceline, i - sourcecoldelta))
            else:
                tokens.append(Token("INTEGER", substr, sourceline, i - sourcecoldelta))
            substr = ""
        elif substr.isalpha():
            # first char of name must be alpabetic, later can be alphanumeric
            while i + 1 < len(text) and text[i + 1].isalnum():
                i += 1
                substr += text[i]
            if substr in _types:
                tokens.append(Token("TYPE", substr, sourceline, i - sourcecoldelta))
            elif substr in _reswords:
                tokens.append(Token(_reswords[substr], substr, sourceline, i - sourcecoldelta))
            else:
                tokens.append(Token("NAME", substr, sourceline, i - sourcecoldelta))
            substr = ""
        elif substr == '"':
            # quote means string constant, slurp up everything until next quote
            substr = ""  # omit first quote
            while text[i + 1] != '"':
                i += 1
                substr += text[i]
            i += 1   # skip past closing quote
            tokens.append(Token("STRCONST", substr, sourceline, i - sourcecoldelta))
            substr = ""        
        elif substr in _symbols:
            # Handle special case of two-character symbols, by looking ahead to see if
            #  current symbol + next char ahead make a valid two-char symbol
            #  (e.g. want to tokenize '==' as one token even though '=' is a valid token as well)
            if i + 1 < len(text) and substr + text[i + 1] in _symbols:
                symbol2 = substr + text[i + 1]
                tokens.append(Token(_symbols[symbol2], symbol2, sourceline, i - sourcecoldelta))
                i += 1
                substr = ""
            else:
                tokens.append(Token(_symbols[substr], substr, sourceline, i - sourcecoldelta))
            substr = ""
        i += 1
    return tokens

def tokenize_file(filename, debug: bool = False) -> list[Token]:
    """Load filename, tokenize it, return list of tokens"""
    with open(filename) as file:
        source = file.read()
    tokens = tokenize(source)
    if debug:
        printcolor("-- SOURCE FILE (%s):" % filename)
        print(source.strip())
        printcolor("-- TOKENS:")
        pprint(tokens)
    return tokens


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    # input = "print 123 + xy;"
    # print_colorheader("Sample input string: ", input)
    # output = tokenize(input)
    # print_colorheader("Tokenized output:", output)

    header = f"***  Running tests in {os.path.basename(__file__)}  ***"
    print("*" * len(header))
    print(header)
    print("*" * len(header))

    printcolor("Running tokenizer unit tests...")

    assert token_list_eq(
        tokenize('+ - * / % = < > <= >= != { } ( ) , ; == #'),
        [
            Token("PLUS", "+"),
            Token("SUB", "-"),
            Token("TIMES", "*"),
            Token("DIV", "/"),
            Token("MOD", "%"),
            Token("ASSIGN", "="),
            Token("LT", "<"),
            Token("GT", ">"),
            Token("LTE", "<="),
            Token("GTE", ">="),
            Token("NEQ", "!="),
            Token("LBRACE", "{"),
            Token("RBRACE", "}"),
            Token("LPAREN", "("),
            Token("RPAREN", ")"),
            Token("COMMA", ","),
            Token("SEMI", ";"),
            Token("EQ", "=="),
            Token("HASH", "#"),
        ],
    )

    assert token_list_eq(
        tokenize("else elif if print var while for return func"),
        [
            Token("ELSE", "else"),
            Token("ELIF", "elif"),
            Token("IF", "if"),
            Token("PRINT", "print"),
            Token("VAR", "var"),
            Token("WHILE", "while"),
            Token("FOR", "for"),
            Token("RETURN", "return"),
            Token("FUNC", "func"),
        ],
    )

    assert token_list_eq(
        tokenize("print 123 + xy;"),
        [
            Token("PRINT", "print"),
            Token("INTEGER", "123"),
            Token("PLUS", "+"),
            Token("NAME", "xy"),
            Token("SEMI", ";"),
        ],
    )

    assert token_list_eq(
        tokenize("var f = 1.5;"),
        [
            Token("VAR", "var"),
            Token("NAME", "f"),
            Token("ASSIGN", "="),
            Token("FLOAT", "1.5"),
            Token("SEMI", ";"),
        ],
    )

    assert token_list_eq(
        tokenize("var x = 5; //comment\nx = 6;"),
        [
            Token("VAR", "var"),
            Token("NAME", "x"),
            Token("ASSIGN", "="),
            Token("INTEGER", "5"),
            Token("SEMI", ";"),
            Token("NAME", "x"),
            Token("ASSIGN", "="),
            Token("INTEGER", "6"),
            Token("SEMI", ";"),
        ],
    )

    assert token_list_eq(
        tokenize("var x int;"),
        [
            Token("VAR", "var"),
            Token("NAME", "x"),
            Token("TYPE", "int"),
            Token("SEMI", ";"),
        ],
    )

    assert token_list_eq(
        tokenize("var x = \n 2+ 3;"),
        [
            Token("VAR", "var"),
            Token("NAME", "x"),
            Token("ASSIGN", "="),
            Token("INTEGER", "2"),
            Token("PLUS", "+"),
            Token("INTEGER", "3"),
            Token("SEMI", ";"),
        ],
    )

    # test that this invalid syntax is tokenized ('5x' is not a valid NAME so is parsed as Int,Name)
    assert token_list_eq(
        tokenize("var 5x = 3;"),
        [
            Token("VAR", "var"),
            Token("INTEGER", "5"),
            Token("NAME", "x"),
            Token("ASSIGN", "="),
            Token("INTEGER", "3"),
            Token("SEMI", ";"),
        ],
    )

    assert token_list_eq(
        tokenize('print "hello x=5.";'),
        [
            Token("PRINT", "print"),
            Token("STRCONST", "hello x=5."),
            Token("SEMI", ";"),
        ],
    )

    assert token_list_eq(
        tokenize('#include "stdlib.wb";'),
        [
            Token("HASH", "#"),
            Token("INCLUDE", "include"),
            Token("STRCONST", "stdlib.wb"),
            Token("SEMI", ";"),
        ],
    )

    printcolor("PASSED", ansicode.green)
