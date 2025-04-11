# statement_instructions.py
"""Transform statements in program's AST into a stack machine representation.

This abstracts away the language representation created by the parser, toward something more like
generic machine code, as another step towards machine code generation. Store these expressions with the 
new STATEMENT class which will be used to identify what later compilation to do on this.

For example, transform Print(EXPR([exprlist]])) into STATEMENT([exprlist, PRINT()]).

Previous compiler stage: expr_instructions.py
Next compiler stage: basicblocks.py"""
#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests
# [X] rename some functions like program_..., make consistent with expression_instructions usage
# [ ] future more complex tests?

# See also test_compile_roundtrip.py for more in depth usage / testing from beginning to end

from model import *
from format import *
from pprint import pprint
from expression_instructions import *


def program_statement_instructions(program: Program) -> Program:
    """Transform all statements in program to stack machine representation."""
    return Program(statements_instructions(program.statements))


def statements_instructions(statements: list[Statement]) -> list[Statement]:
    """Transform list of statements to stack machine representation (whether the
    top-level program or the statements in the body of some flow control structure)."""
    return [statement_instructions(s) for s in statements]


def statement_instructions(s: Statement) -> Statement:
    """Transform statement to stack machine representation. The core translation logic
    for each type of statement lives here."""
    match s:
        case Print(x):
            return STATEMENT(x.instructions + [PRINT()])
        case PrintStrConstNum(n):
            return STATEMENT([PRINT_STR_CONST(n)])
        case StrConstNum(n, txt):
            return s # for now, treat like global variable declaration and ignore
        case Assign(GlobalName(x), y):
            return STATEMENT(y.instructions + [STORE_GLOBAL(x)])
        case Assign(LocalName(x), y):
            return STATEMENT(y.instructions + [STORE_LOCAL(x)])
        case LocalName(x):
            return STATEMENT([LOAD_LOCAL(x.str)])
        case GlobalName(x):
            return STATEMENT([LOAD_GLOBAL(x.str)])
        case LocalVar(x):
            return STATEMENT([LOCAL(x.str)])
        case GlobalVar():
            # TODO: nothing for now
            return s
        case Function(name, params, code):
            # TODO: nothing for now
            return Function(name, params, statements_instructions(code))
        case Return(x):
            return STATEMENT(x.instructions + [RETURN()])
        case IfElse(relation, iflist, elselist):
            return IfElse(relation, statements_instructions(iflist), statements_instructions(elselist))
        case While(relation, code):
            return While(relation, statements_instructions(code))
        case ExprStatement(x):
            return STATEMENT(x.instructions)
            ## TODO: should this also pop the stack? (since the expression pushes a result to the stack which is never used)
        case _:
            raise RuntimeError(f"Unhandled statement {s}")


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    ## Test expr substitution in a statement
    # print(42 + x)
    a = statement_instructions(Print(EXPR([PUSH(42), LOAD_LOCAL("x"), ADD()])))
    # print(a)
    # print("formatted:\n%s" % fmt_statement(a))
    assert a == STATEMENT([PUSH(42), LOAD_LOCAL("x"), ADD(), PRINT()])

    # z = (42 + x) * 65
    b = statement_instructions(Assign(LocalName("z"), EXPR([PUSH(42), LOAD_LOCAL("x"), ADD(), PUSH(65), MUL()])))
    # print(b)
    # print(fmt_statement(b))
    assert b == STATEMENT([PUSH(42), LOAD_LOCAL("x"), ADD(), PUSH(65), MUL(), STORE_LOCAL("z")])

    # var x
    c = statement_instructions(LocalVar(Name("z")))
    #    print(c)
    assert c == STATEMENT([LOCAL("z")])

    printcolor("simple single statement_instructions() tests PASSED", ansicode.green)

    # Test encoding a list of statements:
    test = [
        GlobalVar(Name("x")),
        Assign(GlobalName("x"), Add(GlobalName("x"), Integer(1))),
        Print(Add(Multiply(Integer(23), Integer(45)), GlobalName("x"))),
    ]
    #    print("--Statement list\n%s" % fmt_statements(test))

    x = statements_exprcode(test)
    #   print(x)
    #   print("--After exprcode substitution\n%s" % fmt_statements(x))

    z = statements_instructions(x)
    #    print(z)
    #    print("--After statement instruction substitution\n%s" % fmt_statements(z))

    c = statements_instructions(
        [
            IfElse(
                EXPR([LOAD_LOCAL("x"), PUSH(10), LT()]),
                [Print(EXPR([LOAD_LOCAL("x"), PUSH(1), ADD()]))],
                [Print(EXPR([LOAD_LOCAL("x"), PUSH(2), ADD()]))],
            ),
        ]
    )
    #    print(c)
    #    print(fmt_statements(c))

    assert c == [
        IfElse(
            condition=EXPR(instructions=[LOAD_LOCAL("x"), PUSH(10), LT()]),
            iflist=[STATEMENT(instructions=[LOAD_LOCAL("x"), PUSH(1), ADD(), PRINT()])],
            elselist=[STATEMENT(instructions=[LOAD_LOCAL("x"), PUSH(2), ADD(), PRINT()])],
        )
    ]

    printcolor("minimal tests PASSED", ansicode.green)
