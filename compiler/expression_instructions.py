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
"""
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
        case ExprStatement(e):
            return ExprStatement(expr_instructions(e))
        case PrintStrConstNum() | StrConstNum():
            return s
        case _:
            raise RuntimeError(f"Unhandled statement {s}")


def expr_instructions(expr: Expression) -> EXPR:
    """Transform a single expression to its EXPR() state machine representation. This calls itself
    recursively on parameters of many expressions, to process nested expressions."""
    match expr:
        case Integer(t, x):
            return EXPR(t, [PUSH(x)])
        case Float(t, x):
            return EXPR(t, [FPUSH(x)])
        case Add(t, left, right):
            return EXPR(t, expr_instructions(left).instructions + expr_instructions(right).instructions + [ADD()])
        case Multiply(t, left, right):
            return EXPR(t, expr_instructions(left).instructions + expr_instructions(right).instructions + [MUL()])
        case Subtract(t, left, right):
            return EXPR(t, expr_instructions(left).instructions + expr_instructions(right).instructions + [SUB()])
        case Divide(t, left, right):
            return EXPR(t, expr_instructions(left).instructions + expr_instructions(right).instructions + [DIV()])
        case Modulo(t, left, right):
            return EXPR(t, expr_instructions(left).instructions + expr_instructions(right).instructions + [MOD()])
        # COMMENTED OUT -- already done earlier at parser level to rewrite to Subtract(0,x) so won't reach here
        #        case Negate(left):
        #            # rewrite -x as 0-x expression, representing '(0-x)'
        #            # TODO: somewhere between here and parser this isn't working
        #            return EXPR([PUSH(0)] + expr_instructions(left).instructions + [ SUB() ])
        case RelationOp(x):
            if x == "<":
                return EXPR(UNKNOWN_TYPE,[LT()])
            elif x == "==":
                return EXPR(UNKNOWN_TYPE,[EQ()])
            elif x == ">":
                return EXPR(UNKNOWN_TYPE,[GT()])
            elif x == ">=":
                return EXPR(UNKNOWN_TYPE,[GTE()])
            elif x == "<=":
                return EXPR(UNKNOWN_TYPE,[LTE()])
            elif x == "!=":
                return EXPR(UNKNOWN_TYPE,[NEQ()])
            # Todo: error case?
        case Relation(t, op, left, right):
            return EXPR(t, 
                expr_instructions(left).instructions
                + expr_instructions(right).instructions
                + expr_instructions(op).instructions
            )
        case LocalName(t, x):
            return EXPR(t, [LOAD_LOCAL(x)])
        case GlobalName(t, x):
            return EXPR(t, [LOAD_GLOBAL(x)])
        case CallFn(t, Name(tname, fname), params):
            pushparams = []
            # Push each parameter onto the stack: parameters themselves are expressions
            for p in params:
                pushparams.extend(expr_instructions(p).instructions)
            return EXPR(t, pushparams + [CALL(fname, len(params))])
        case _:
            raise RuntimeError("Can't generate EXPR code for Expression %s" % expr)

######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    expr = Add(TEST_TYPE,Integer(TEST_TYPE,2), GlobalName(TEST_TYPE,"x"))
    #    print(expr_instructions(expr))
    #    print(EXPR([PUSH(2), LOAD_GLOBAL("x"), ADD()]))
    expr2 = expr_instructions(expr)
    # print(expr2)
    # print("formatted: %s" % fmt_expr(expr2))
    assert expr2 == EXPR(TEST_TYPE,[PUSH(2), LOAD_GLOBAL("x"), ADD()])

    assert expr_instructions(Relation(TEST_TYPE,RelationOp("<"), Integer(TEST_TYPE,5), GlobalName(TEST_TYPE,"x"))) == EXPR(
        TEST_TYPE,
        [PUSH(5), LOAD_GLOBAL("x"), LT()]
    )

    # call function f(3,4)
    # print(expr_instructions(CallFn(Name("f"), [Integer(3), Integer(4)])))
    # print(expr_instructions(CallFn(TEST_TYPE,Name(TEST_TYPE,"f"), [Integer(TEST_TYPE,3), Integer(TEST_TYPE,4)])))
    # print(EXPR(TEST_TYPE,[PUSH(3), PUSH(4), CALL("f", 2)]))
    assert expr_instructions(CallFn(TEST_TYPE,Name(TEST_TYPE,"f"), [Integer(TEST_TYPE,3), Integer(TEST_TYPE,4)])) == EXPR(TEST_TYPE,[PUSH(3), PUSH(4), CALL("f", 2)])

    # 42 + x
    a = expr_instructions(Add(TEST_TYPE,Integer(TEST_TYPE,42), LocalName(TEST_TYPE,"x")))
    assert a == EXPR(TEST_TYPE,[PUSH(42), LOAD_LOCAL("x"), ADD()])

    # (42 + x) * 65
    b = expr_instructions(Multiply(TEST_TYPE,Add(TEST_TYPE,Integer(TEST_TYPE,42), LocalName(TEST_TYPE,"x")), Integer(TEST_TYPE,65)))
    #    print(b)
    #    print(fmt_expr(b))
    assert b == EXPR(TEST_TYPE,[PUSH(42), LOAD_LOCAL("x"), ADD(), PUSH(65), MUL()])

    printcolor("tests PASSED", ansicode.green)
