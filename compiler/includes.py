# includes.py
"""After tokenizing but before parsing, execute the preprocessor #include directives to 
import other files, such as shared libraries. 

Each of the included files will itself need to be tokenized.

TODO: Decide how to handle nested includes, including detecting circular includes.
For now, we will only process #includes in the first top-level file.
"""

import os
from printcolor import *
from tokenizer import *
from pprint import pprint


def expand_includes(tokens: list[Token], workingdir: str=".") -> list[Token]:
    """Insert the tokenized contents of any #included files in the current token list.
    Currently does not recursively include the #includes of those files, until we have a
    plan for handling potential circuilar includes."""
    # TODO: fix sourceline and sourcecol notations as well
    # #     perhaps add a new 'sourcefile' attribute per line for syntax errors? hmm
    includes = []
    tokensout = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        # TODO: check we're not too close to end of file either
        if tok.toktype == "HASH" and tokens[i + 1].toktype == "INCLUDE" and tokens[i + 2].toktype == "STRCONST":
            includefile = os.path.join(workingdir, tokens[i + 2].tokvalue)   
            # Check if the file exists, if so tokenize its contents and insert in file
            if not os.path.exists(includefile):
                raise FileNotFoundError(f"Include file '{includefile}' not found")
            include_tokens = tokenize_file(includefile)
            tokensout.extend(include_tokens)
            # TODO: In future, search included files for their own includes, perhaps by calling
            #       expand_includes() recursively here after tokenize_file(),
            #       but need to avoid infinite circular includes
            i += 3  # skip over the #include directive tokens
        else:
            # not an include directive, so just copy the token to the output list
            tokensout.append(tok)
            i += 1
    return tokensout


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    header = f"***  Running tests in {os.path.basename(__file__)}  ***"
    print("*" * len(header))
    print(header)
    print("*" * len(header))

    # try tokenizing a file within the test directory that includes another, both very simple
    currentdir = os.path.dirname(os.path.abspath(__file__))
    testsdir = os.path.join(currentdir, "tests")
    testfile = os.path.join(testsdir, "include1.wb")
    testfile_result = os.path.join(testsdir, "include1result.wb")
    test_expand = expand_includes(tokenize_file(testfile), testsdir)
    #pprint(test_expand)
    goal_expand = tokenize_file(testfile_result)
    # print("*** Should match reference file: ***")
    #pprint(goal_expand)
    # only check tokens not row/col numbers
    for i in range(len(test_expand)):
        # print(test_expand[i], "\n", goal_expand[i], "\n")
        assert(test_expand[i].toktype == goal_expand[i].toktype)
        assert(test_expand[i].tokvalue == goal_expand[i].tokvalue)

    printcolor("PASSED", ansicode.green)

