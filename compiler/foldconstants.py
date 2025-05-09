# foldconstants.py
"""Evaluate and simplify math on constants (included nested math operations) across program.
"""
#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests

# TODO
# Think: Seems like I shouldn't need to handle a case for every class (and requires keeping this in sync with
#     any model.py changes), would it be sensible to somehow to iterate over all class variables and
#     apply fold_expression() to any Expression?
# [X]  Add(a,b): fold(a),fold(b) first, then check if those are integers
# [ ] Handle constant folding / expression simplification within parameters passed to function calls


from model import *
from format import *


def fold_constants(program: Program) -> Program:
    """Fold all constant math in program."""
    return Program(fold_statements(program.statements))


def fold_statements(statements: list[Statement]) -> list[Statement]:
    """Fold all constant math in a list of statements. This is separate from fold_constants(Program)
    because processing flow structures (IfElse, for example) will involve calling this recursively on the
    statement lists within them."""
    return [fold_statement(s) for s in statements]


def fold_statement(s: Statement) -> Statement:
    """Fold all constant math in this statement (including any statements contained within it such
    as If/Else bodies)."""
    match s:
        case Print(x):
            return Print(fold_expression(x))
        case Assign(x, y):
            return Assign(x, fold_expression(y))
        case DeclareValue(x, y):
            return DeclareValue(x, fold_expression(y))
        case IfElse(relation, iflist, elselist):
            return IfElse(fold_expression(relation), fold_statements(iflist), fold_statements(elselist))
        case While(relation, s):
            return While(fold_expression(relation), fold_statements(s))
        case Return(e):
            return Return(fold_expression(e))
        case Function(n, p, s):
            return Function(n, p, fold_statements(s))
        case ExprStatement(e):
            return ExprStatement(fold_expression(e))
        case Declare() | PrintStr():
            # Pass-through specific case(s) where we do nothing
            return s
        case _:
            raise RuntimeError(f"Unhandled fold_statement() case {s}")


def fold_expression(e: Expression) -> Expression:
    """Perform the work of actively computing constant math within the given expression and
    returning a simplified expression."""
    match e:
        case Integer() | Name() | RelationOp():
            return e
        # COMMENTED OUT, as this is rewritten at the parser level to be Subtract(0,x) so Negate doesn't reach here?
        #        case Negate(x):
        #            if isinstance(x, Integer):
        #                return Integer(-x.n)
        #            else:
        #                # TODO: Buggy, figure out how to handle negation of an expression e.g. -(4+5)
        #                # Don't want to fold_expression(x) first?
        #                #return Subtract(Integer(0), x)   # No, buggy, calculates '-5 + 4' as '0 - (5 + 4)'
        #                pass
        case Add(t, x, y):
            # Calculate these first to let us recursively fold nested expressions
            fx = fold_expression(x)
            fy = fold_expression(y)
            if isinstance(fx, Integer) and isinstance(fy, Integer):
                # two integers, so we can combine them!
                return Integer(UNKNOWN_TYPE, fx.n + fy.n)
            else:
                return Add(UNKNOWN_TYPE, fx, fy)
        case Multiply(t, x, y):
            fx = fold_expression(x)
            fy = fold_expression(y)
            if isinstance(fx, Integer) and isinstance(fy, Integer):
                return Integer(UNKNOWN_TYPE, fx.n * fy.n)
            else:
                return Multiply(UNKNOWN_TYPE, fx, fy)
        case Subtract(t, x, y):
            fx = fold_expression(x)
            fy = fold_expression(y)
            if isinstance(fx, Integer) and isinstance(fy, Integer):
                return Integer(UNKNOWN_TYPE, fx.n - fy.n)
            else:
                return Subtract(UNKNOWN_TYPE, fx, fy)
        case Divide(t, x, y):
            fx = fold_expression(x)
            fy = fold_expression(y)
            if isinstance(fx, Integer) and isinstance(fy, Integer):
                return Integer(UNKNOWN_TYPE, fx.n // fy.n)
            else:
                return Divide(UNKNOWN_TYPE, fx, fy)
        case Modulo(t, x, y):
            fx = fold_expression(x)
            fy = fold_expression(y)
            if isinstance(fx, Integer) and isinstance(fy, Integer):
                return Integer(UNKNOWN_TYPE, fx.n % fy.n)
            else:
                return Modulo(UNKNOWN_TYPE, fx, fy)
        case Relation(t, op, left, right):
            return Relation(UNKNOWN_TYPE, op, fold_expression(left), fold_expression(right))
        case CallFn(t, name, params):
            return CallFn(UNKNOWN_TYPE, name, [fold_expression(p) for p in params])
        case _:
            raise RuntimeError(f"Unhandled fold_expression() case {e}")


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    print("A few foldconstants.py test cases:")
    test_program_statements = (
        ([Print(Add(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,2), Integer(UNKNOWN_TYPE,3)))], [Print(Integer(UNKNOWN_TYPE,5))]),
        # [Print(Add(Negate(Integer(2)), Integer(3)))],
        # [Print(Negate(Add(Integer(2), Integer(3))))],
        (
            [
                DeclareValue(Name(UNKNOWN_TYPE,"x"), Integer(UNKNOWN_TYPE,10)),
                Assign(Name(UNKNOWN_TYPE,"x"), Add(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"x"), Integer(UNKNOWN_TYPE,1))),
                Print(Add(UNKNOWN_TYPE,Multiply(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,23), Integer(UNKNOWN_TYPE,45)), Name(UNKNOWN_TYPE,"x"))),
                Print(Multiply(UNKNOWN_TYPE,Add(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,2), Integer(UNKNOWN_TYPE,3)), Integer(UNKNOWN_TYPE,4))),
            ],
            [
                DeclareValue(Name(UNKNOWN_TYPE,"x"), Integer(UNKNOWN_TYPE,10)),
                Assign(Name(UNKNOWN_TYPE,"x"), Add(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"x"), Integer(UNKNOWN_TYPE,1))),
                Print(Add(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,1035), Name(UNKNOWN_TYPE,("x")))),
                Print(Integer(UNKNOWN_TYPE,20)),
            ],
        ),
        (
            [
                Function(
                    Name(UNKNOWN_TYPE,"add1twice"),
                    [Name(UNKNOWN_TYPE,"x")],
                    [Assign(Name(UNKNOWN_TYPE,"x"), Add(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"x"), Add(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,1), Integer(UNKNOWN_TYPE,1)))), Return(Name(UNKNOWN_TYPE,"x"))],
                ),
                DeclareValue(Name(UNKNOWN_TYPE,"x"), Integer(UNKNOWN_TYPE,10)),
                Print(Add(UNKNOWN_TYPE,Multiply(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,23), Integer(UNKNOWN_TYPE,45)), CallFn(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"add1twice"), [Name(UNKNOWN_TYPE,"x")]))),
                Print(Name(UNKNOWN_TYPE,"x")),
            ],
            [
                Function(
                    Name(UNKNOWN_TYPE,"add1twice"),
                    [Name(UNKNOWN_TYPE,"x")],
                    [Assign(Name(UNKNOWN_TYPE,"x"), Add(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"x"), Integer(UNKNOWN_TYPE,2))), Return(Name(UNKNOWN_TYPE,"x"))],
                ),
                DeclareValue(Name(UNKNOWN_TYPE,("x")), Integer(UNKNOWN_TYPE,10)),
                Print(Add(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,1035), CallFn(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"add1twice"), [Name(UNKNOWN_TYPE,"x")]))),
                Print(Name(UNKNOWN_TYPE,"x")),
            ],
        ),
        (
            [
                Function(
                    Name(UNKNOWN_TYPE,"miscmath"),
                    [Name(UNKNOWN_TYPE,"a"), Name(UNKNOWN_TYPE,"b")],
                    [
                        IfElse(
                            Relation(UNKNOWN_TYPE,RelationOp("<"), Name(UNKNOWN_TYPE,"a"), Add(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,5), Integer(UNKNOWN_TYPE,3))),
                            [
                                Return(
                                    Multiply(UNKNOWN_TYPE,
                                        Add(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,3), Integer(UNKNOWN_TYPE,4)),
                                        Add(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"a"), Multiply(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"a"), Name(UNKNOWN_TYPE,"b"))),
                                    )
                                )
                            ],
                            [Return(Integer(UNKNOWN_TYPE,4))],
                        )
                    ],
                ),
                DeclareValue(Name(UNKNOWN_TYPE,"x"), Integer(UNKNOWN_TYPE,3)),
                Print(CallFn(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"miscmath"), [Add(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,2), Add(UNKNOWN_TYPE,Integer(UNKNOWN_TYPE,2), Integer(UNKNOWN_TYPE,7))), Name(UNKNOWN_TYPE,"x")])),
            ],
            [
                Function(
                    Name(UNKNOWN_TYPE,"miscmath"),
                    [Name(UNKNOWN_TYPE,"a"), Name(UNKNOWN_TYPE,"b")],
                    [
                        IfElse(
                            Relation(UNKNOWN_TYPE,RelationOp("<"), Name(UNKNOWN_TYPE,"a"), Integer(UNKNOWN_TYPE,8)),
                            [
                                Return(
                                    Multiply(UNKNOWN_TYPE,
                                        Integer(UNKNOWN_TYPE,7),
                                        Add(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"a"), Multiply(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"a"), Name(UNKNOWN_TYPE,"b"))),
                                    )
                                )
                            ],
                            [Return(Integer(UNKNOWN_TYPE,4))],
                        )
                    ],
                ),
                DeclareValue(Name(UNKNOWN_TYPE,"x"), Integer(UNKNOWN_TYPE,3)),
                Print(CallFn(UNKNOWN_TYPE,Name(UNKNOWN_TYPE,"miscmath"), [Integer(UNKNOWN_TYPE,11), Name(UNKNOWN_TYPE,"x")])),
            ],
        ),
    )
    for s in test_program_statements:
        p = Program(s[0])
        ##        print("-- program to be folded: --")
        #print(format_program(p))
        ##        print("-- after folding: --")
        #print(format_program(fold_constants(p)))
        ##print(fold_constants(p))
        assert fold_constants(p) == Program(s[1])
    #  quit()
    printcolor("tests PASSED", ansicode.green)
