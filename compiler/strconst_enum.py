# strconst_enum.py
"""Split PrintStr statements in the AST into two parts, to better match the structure of future assembly code
where string literals are defined in a header:
* A string constant definition with a unique global ID
* A print-string-constant-by-ID statement

e.g. 'printstr("hello")' -> ['strconst(1,"hello")', 'printstrconstnum(1)']

Then in a second pass, walk the AST and extract all of the strconst definitions,
moving them to the top level of the program, which will simplify later translation to assembly code.
"""

from model import *
from format import *
from debughelper import *

_strconst_n = 0
"""Index for globally unique strconst ID. Incremented before value is returned, so
initializing to 0 means the first strconst will be 1, and so on."""


def set_strconst_n(n) -> None:
    """Directly set the global strconst index to a specific value. This is likely only useful for
    debugging and deterministic testing, where we want to test some subset of this module."""
    global _strconst_n
    _strconst_n = n


def next_strconst_n() -> int:
    """Return a globally unique strconst number, which is incremented each time this is called."""
    global _strconst_n
    _strconst_n += 1
    return _strconst_n


def strconst_program(program: Program) -> Program:
    s = strconst_statements(program.statements)
    # debug
    # print("\n*** program with printstr separated ***")
    # print(s)
    # print("\n*** now shifting strconst definitions to the top level ***")
    slist, deflist = separate_strconst_statements(s)
    # print("\n*** extracted definitions ***")
    # print(deflist)
    # print("\n*** remaining statements ***")
    # print(slist)

    # move all strconst definitions to the beginning of the program
    return Program(deflist + slist)


def separate_strconst_statements(statements: list[Statement]) -> list[list[Statement]]:
    """Separate list of statements into two lists: one list containing the original statements
    but with any strconst definitions (at any level of depth) removed, the second as a flat list
    of only these strconst definitions, to make it easy to aggregate them across recursive calls of this
    and eventually have a flat top-level list of constant definitions."""
    slist = []
    deflist = []
    for s in statements:
        out_s, out_def = separate_strconst_statement(s)
        slist.extend(out_s)
        deflist.extend(out_def)
    return slist, deflist


def separate_strconst_statement(s: Statement) -> list[list[Statement]]:
    """Separate a single statement into strconst definitions vs. other, as noted above.
    Return two lists: the main program, and just a list of strconst definitions."""
    match s:
        case StrConstNum():
            # The primary purpose of this compiler pass: split out strconstnum definitions
            #  into a second list
            return [], [s]
        case IfElse(relation, iflist, elselist):
            # Process the bodies of If/Else statements (recursively if needed), extracting any StrConstNum definitions in them
            if_s, if_def = separate_strconst_statements(iflist)
            else_s, else_def = separate_strconst_statements(elselist)
            return [IfElse(relation, if_s, else_s)], if_def + else_def
        case While(relation, s):
            body_s, body_def = separate_strconst_statements(s)
            return [While(relation, body_s)], body_def
        case Function(n, p, s):
            body_s, body_def = separate_strconst_statements(s)
            return [Function(n, p, body_s)], body_def
        case Print() | Assign() | Return() | Declare() | ExprStatement() | PrintStrConstNum():
            # Listed all these remaining cases out so we can save the fallthrough "case _" for errors
            return [s], []
        case _:
            raise RuntimeError(f"Unhandled separate_strconst_statement() case {s}")


def strconst_statements(statements: list[Statement]) -> list[Statement]:
    """Translate a list of statements, could be at the top program level, or a list of statements
    nested within a Function, IfElse, While, or so on."""
    slist = []
    # TODO: some better way to replace for loop with a list comprehension?
    for s in statements:
        # print("DEBUG " + str(deinit_statement(s)))
        # extend = append each statement from list deinit_statments() one by one
        slist.extend(strconst_statement(s))
    return slist


def strconst_statement(s: Statement) -> list[Statement]:
    """Pass throguh most statements, but split PrintStr() statement into unique string constant
    definition and usage."""
    ## TODO(BUG): if StrConstNum is within a structure (Function, etc) it won't be at the top
    ##            level of the program (unlike global var declarations), which is needed later
    match s:
        case PrintStr(txt):
            # The primary purpose of this compiler pass
            n = next_strconst_n()
            return [StrConstNum(n, txt), PrintStrConstNum(n)]
        case IfElse(relation, iflist, elselist):
            return [IfElse(relation, strconst_statements(iflist), strconst_statements(elselist))]
        case While(relation, s):
            return [While(relation, strconst_statements(s))]
        case Function(n, p, s):
            return [Function(n, p, strconst_statements(s))]
        case Print() | Assign() | Return() | Declare() | ExprStatement():
            # Listed all these remaining cases out so we can save the fallthrough case _ for errors
            return [s]
        case _:
            raise RuntimeError(f"Unhandled strconst_statement() case {s}")


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    # Simple top-level test
    assert strconst_program(Program([Print(Integer(5)), PrintStr("hello world")])) == Program(
        [StrConstNum(1, "hello world"), Print(Integer(5)), PrintStrConstNum(1)]
    )
    # Tested with strconst within another structure (need to manually reset global strconst_n
    #  first for deterministic output, as it was incremented by any tests above)
    set_strconst_n(0)
    assert strconst_program(
        Program(
            [
                Function(
                    Name("foo"),
                    [],
                    [
                        IfElse(
                            Relation(RelationOp("=="), Integer(1), Integer(1)),
                            [PrintStr("1==1")],
                            [],
                        )
                    ],
                ),
                ExprStatement(CallFn(Name("foo"), [])),
            ]
        )
    ) == Program(
        [
            StrConstNum(1, "1==1"),
            Function(
                Name("foo"),
                [],
                [
                    IfElse(
                        Relation(RelationOp("=="), Integer(1), Integer(1)),
                        [PrintStrConstNum(1)],
                        [],
                    )
                ],
            ),
            ExprStatement(CallFn(Name("foo"), [])),
        ]
    )

    printcolor("tests PASSED", ansicode.green)
