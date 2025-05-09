# resolve_type.py
"""Resolve / infer expression types across entire program AST: update each expression with unknown data type
with an explicit data type.
"""

## Early WIP, just the structure/scaffold

from model import *
from format import *
from debughelper import *

# keep a list of the types of each variable declaration found, to propogate to all
#  references to that variable
# BUG/TODO: wouldn't correctly handle cases where variables with the same names in different scopes
#           (e.g. global vs. function-local) have different data types
#           need to rewrite to work within scope context (or rewrite types in resolve_scope)
# TODO: extract types from function parameters and func definitions for callfn use as well
vartypes = {}

def resolve_types(program: Program) -> Program:
    """Resolve all variable types in program."""
    return Program(resolve_type_statements(program.statements))


def resolve_type_statements(statements: list[Statement]) -> list[Statement]:
    """Resolve all variable types in a list of statements (whether top-level program or the
    list of statements within some flow control structure such as If/While)."""
    return [resolve_type_statement(s) for s in statements]


def resolve_type_statement(s: Statement) -> Statement:
    """Resolve all variable types in this statement (including recursively on contained statement blocks
    if relevant)."""
    # print("DEBUG: "+str(s))
    match s:
        case Print(x):
            return Print(resolve_type_expr(x))
        case Assign(x, y):
            return Assign(resolve_type_expr(x), resolve_type_expr(y))
        case Declare(t, x):
            # should have already been handled at parser level
            vartypes[x.str] = t 
            return s
        case DeclareValue(name, val):
            rval = resolve_type_expr(val)
            name.wtype = rval.wtype
            vartypes[name.str] = rval.wtype
            return DeclareValue(name, rval)
        case IfElse(relation, iflist, elselist):
            return IfElse(
                resolve_type_expr(relation),
                resolve_type_statements(iflist),
                resolve_type_statements(elselist),
            )
        case While(relation, s):
            return While(
                resolve_type_expr(relation),
                resolve_type_statements(s),
            )
        case Return(x):
            return Return(resolve_type_expr(x))
        case Function(name, params, body):
            vartypes[name.str] = name.wtype
            # TODO / BUG: overwrites other uses of these names in other scopes
            for p in params:
                vartypes[p.str] = p.wtype
            return Function(name, params, resolve_type_statements(body))
        case ExprStatement(x):
            return ExprStatement(resolve_type_expr(x))
        case PrintStrConstNum(x):
            return PrintStrConstNum(resolve_type_expr(x))
        case StrConstNum(x):
            return StrConstNum(resolve_type_expr(x))
        case _:
            raise RuntimeError(f"Unhandled case {s}")


def resolve_type_expr(e: Expression) -> Expression:
    """Resolve all variable types in this expression (and child expressions)."""
    match e:
        case Name(t, x):
            if x in vartypes:
                t = vartypes[x]
            return Name(t, x)
        case Add(t, x, y):
            rx = resolve_type_expr(x)
            ry = resolve_type_expr(y)   
            if rx.wtype == Type('int') and ry.wtype == Type('int'):
                return Add(Type("int"),rx,ry)
            elif rx.wtype == Type('float') and ry.wtype == Type('float'):
                return Add(Type("float"),rx,ry)
            else:
                raise RuntimeError(f"Mismatched types {rx.wtype.name} + {ry.wtype.name} in {e}")
        case Multiply(t, x, y):
            rx = resolve_type_expr(x)
            ry = resolve_type_expr(y)
            if rx.wtype == Type('int') and ry.wtype == Type('int'):
                return Multiply(Type("int"),rx,ry)
            elif rx.wtype == Type('float') and ry.wtype == Type('float'):
                return Multiply(Type("float"),rx,ry)
            else:
                raise RuntimeError(f"Unable to infer type in {e}")
        case Subtract(t, x, y):
            rx = resolve_type_expr(x)
            ry = resolve_type_expr(y)
            if rx.wtype == Type('int') and ry.wtype == Type('int'):
                return Subtract(Type("int"),rx,ry)
            elif rx.wtype == Type('float') and ry.wtype == Type('float'):
                return Subtract(Type("float"),rx,ry)
            else:
                raise RuntimeError(f"Unable to infer type in {e}")
        case Divide(t, x, y):
            rx = resolve_type_expr(x)
            ry = resolve_type_expr(y)
            if rx.wtype == Type('int') and ry.wtype == Type('int'):
                return Divide(Type("int"),rx,ry)
            elif rx.wtype == Type('float') and ry.wtype == Type('float'):
                return Divide(Type("float"),rx,ry)
            else:
                raise RuntimeError(f"Unable to infer type in {e}")
        case Modulo(t, x, y):
            rx = resolve_type_expr(x)
            ry = resolve_type_expr(y)
            if rx.wtype == Type('int') and ry.wtype == Type('int'):
                return Modulo(Type("int"),rx,ry)
            elif rx.wtype == Type('float') and ry.wtype == Type('float'):
                return Modulo(Type("float"),rx,ry)
            else:
                raise RuntimeError(f"Unable to infer type in {e}")
        case CallFn(t, name, params):
            # TODO/DEBUG: types assigned redundantly, to both CallFn and its name?
            if name.str in vartypes:
                t = vartypes[name.str]
            return CallFn(t, name, [resolve_type_expr(p) for p in params])
        case Relation(t, op, left, right):
            return Relation(t, op, resolve_type_expr(left), resolve_type_expr(right))
        case Integer(t, x):
            # this case may be redundant if handled in parser
            return Integer(Type("int"), x)
        case Float(t, x):
            # this case may be redundant if handled in parser
            return Float(Type("float"), x)
        case RelationOp():
            return e
        case _:
            raise RuntimeError(f"Unhandled resolve_type Expression {e}")

######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":

    print("Testing resolve_type_expression()...")
    tests = [
        [Integer(UNKNOWN_TYPE, 1), Integer(Type("int"), 1)],
        [
            Add(UNKNOWN_TYPE, Integer(UNKNOWN_TYPE, 1), Integer(UNKNOWN_TYPE, 1)),
            Add(Type("int"), Integer(Type("int"), 1), Integer(Type("int"), 1)),
        ],
    ]
    for test in tests:
        input = test[0]
        output = test[1]
        print(input)
        assert_equal_verbose(resolve_type_expr(input), output)

    printcolor("minimal tests PASSED", ansicode.green)
