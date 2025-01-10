# expr_instructions.py
"""Transform expressions in program's AST into a stack machine representation.

This abstracts away the language representation created by the parser, toward something more like
generic machine code, as a step towards machine code generation. Store these expressions with the 
new EXPR class. 

For example, transform:
    Add(Integer(2), GlobalName("x"))
into:
    EXPR([PUSH(2), LOAD_GLOBAL("x"), ADD()])

In this pass, focus on transforming expressions (including nested expressions that will need the transformation
applied recursively to all arguments), not statements (e.g. Print(), etc) or flow control.

Previous compiler stage: defaultreturns.py
Next compiler stage: statement_instructions.py"""
#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests

from model import *
from format import *
from pprint import pprint


def expr_program(program: Program) -> Program:
    """Transform all expressions in program to EXPR() stack machine representation."""
    return Program(statements_exprcode(program.statements))


def statements_exprcode(statements: list[Statement]) -> list[Statement]:
    """Transform expressions contained in the list of statements.
    This function is called on the top-level program, but is also called when processing lists of
    statements nested inside other program structures (the If / Else code blocks, for example)."""
    return [statement_exprcode(s) for s in statements]


# replace all Expressions in statement with EXPR() equivalent
def statement_exprcode(s: Statement) -> Statement:
    """Transform expressions within this single statement (including as needed nested statements such as
    If/Else bodies)."""
    match s:
        case Print(x):
            return Print(expr_instructions(x))
        case Assign(x, y):
            return Assign(x, expr_instructions(y))
        case LocalVar(x) | GlobalVar(x):
            return s
        case DeclareValue(x, y):
            return DeclareValue(x, expr_instructions(y))
        case IfElse(relation, iflist, elselist):
            return IfElse(expr_instructions(relation), statements_exprcode(iflist), statements_exprcode(elselist))
        case While(relation, s):
            return While(expr_instructions(relation), statements_exprcode(s))
        case Return(e):
            return Return(expr_instructions(e))
        case Function(n, p, s):
            return Function(n, p, statements_exprcode(s))
        case _:
            raise RuntimeError(f"Unhandled statement {s}")


def expr_instructions(expr: Expression) -> EXPR:
    """Transform a single expression to its EXPR() state machine representation. This calls itself
    recursively on parameters of many expressions, to process nested expressions."""
    match expr:
        case Integer(x):
            return EXPR([PUSH(x)])
        case Add(left, right):
            return EXPR(expr_instructions(left).instructions + expr_instructions(right).instructions + [ADD()])
        case Multiply(left, right):
            return EXPR(expr_instructions(left).instructions + expr_instructions(right).instructions + [MUL()])
        case Subtract(left, right):
            return EXPR(expr_instructions(left).instructions + expr_instructions(right).instructions + [SUB()])
        case Divide(left, right):
            return EXPR(expr_instructions(left).instructions + expr_instructions(right).instructions + [DIV()])
        # COMMENTED OUT -- already done earlier at parser level to rewrite to Subtract(0,x) so won't reach here
        #        case Negate(left):
        #            # rewrite -x as 0-x expression, representing '(0-x)'
        #            # TODO: somewhere between here and parser this isn't working
        #            return EXPR([PUSH(0)] + expr_instructions(left).instructions + [ SUB() ])
        case RelationOp(x):
            if x == "<":
                return EXPR([LT()])
            elif x == "==":
                return EXPR([EQ()])
            elif x == ">":
                return EXPR([GT()])
            elif x == ">=":
                return EXPR([GTE()])
            elif x == "<=":
                return EXPR([LTE()])
            elif x == "!=":
                return EXPR([NEQ()])
            # Todo: error case?
        case Relation(op, left, right):
            return EXPR(
                expr_instructions(left).instructions
                + expr_instructions(right).instructions
                + expr_instructions(op).instructions
            )
        case LocalName(x):
            return EXPR([LOAD_LOCAL(x)])
        case GlobalName(x):
            return EXPR([LOAD_GLOBAL(x)])
        case CallFn(Name(fname), params):
            pushparams = []
            # Push each parameter onto the stack: parameters themselves are expressions
            for p in params:
                pushparams.extend(expr_instructions(p).instructions)
            return EXPR(pushparams + [CALL(fname, len(params))])
        case _:
            raise RuntimeError("Can't generate EXPR code for Expression %s" % expr)

######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    expr = Add(Integer(2), GlobalName("x"))
    #    print(expr_instructions(expr))
    #    print(EXPR([PUSH(2), LOAD_GLOBAL("x"), ADD()]))
    expr2 = expr_instructions(expr)
    # print(expr2)
    # print("formatted: %s" % fmt_expr(expr2))
    assert expr2 == EXPR([PUSH(2), LOAD_GLOBAL("x"), ADD()])

    assert expr_instructions(Relation(RelationOp("<"), Integer(5), GlobalName("x"))) == EXPR(
        [PUSH(5), LOAD_GLOBAL("x"), LT()]
    )

    # call function f(3,4)
    # print(expr_instructions(CallFn(Name("f"), [Integer(3), Integer(4)])))
    assert expr_instructions(CallFn(Name("f"), [Integer(3), Integer(4)])) == EXPR([PUSH(3), PUSH(4), CALL("f", 2)])

    # 42 + x
    a = expr_instructions(Add(Integer(42), LocalName("x")))
    assert a == EXPR([PUSH(42), LOAD_LOCAL("x"), ADD()])

    # (42 + x) * 65
    b = expr_instructions(Multiply(Add(Integer(42), LocalName("x")), Integer(65)))
    #    print(b)
    #    print(fmt_expr(b))
    assert b == EXPR([PUSH(42), LOAD_LOCAL("x"), ADD(), PUSH(65), MUL()])

    printcolor("tests PASSED", ansicode.green)
