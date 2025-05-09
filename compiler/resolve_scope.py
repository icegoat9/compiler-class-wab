# resolve_scope.py
"""Resolve variable scope across entire program AST: replace each variable definition or use with an
explicit Global or Local classification (by subtituting in new Local and Global subclasses for objects).
"""

#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests (note: minimal)


# TODOs:
# [X] rename more descriptively?
# [ ] make tougher unit tests with nested ifs, or if in a function
# [X] combine islocal and localvars into a data structure / class?
# [X]    more involved class with add_to_scope and child_scope methods vs just copying?
# [X] catch some undefined variables error?

from model import *
from format import *


def resolve_scopes(program: Program) -> Program:
    """Resolve all variable scopes in program."""
    return Program(resolve_scope_statements(program.statements))


def resolve_scope_statements(statements: list[Statement], scope: Scope = Scope()) -> list[Statement]:
    """Resolve all variable scopes in a list of statements (whether top-level program or the
    list of statements within some flow control structure such as If/While)."""
    return [resolve_scope_statement(s, scope) for s in statements]


def resolve_scope_statement(s: Statement, scope: Scope) -> Statement:
    """Resolve all variable scopes in this statement (including recursively on contained statement blocks
    if relevant). For example, the generic Declare class becomes GlobalVar or LocalVar."""
    # print("DEBUG: "+str(s))
    match s:
        case Print(x):
            return Print(resolve_scope_expr(x, scope))
        case Assign(x, y):
            return Assign(resolve_scope_expr(x, scope), resolve_scope_expr(y, scope))
        case Declare(x):
            scope.declare(x)
            if scope.isglobalscope():
                return GlobalVar(x)
            else:
                return LocalVar(x)
        case IfElse(relation, iflist, elselist):
            return IfElse(
                resolve_scope_expr(relation, scope),
                resolve_scope_statements(iflist, scope.new_child_scope()),
                resolve_scope_statements(elselist, scope.new_child_scope()),
            )
        case While(relation, s):
            return While(
                resolve_scope_expr(relation, scope),
                resolve_scope_statements(s, scope.new_child_scope()),
            )
        case Return(x):
            return Return(resolve_scope_expr(x, scope))
        case Function(n, params, s):
            # Create a new child scope for the function and add passed parameters to it
            fscope = scope.new_child_scope()
            for p in params:
                fscope.declare(p)
            return Function(n, params, resolve_scope_statements(s, fscope))
        case ExprStatement(x):
            return ExprStatement(resolve_scope_expr(x, scope))
        case PrintStrConstNum() | StrConstNum():
            return s
        case _:
            raise RuntimeError(f"Unhandled case {s}")


def resolve_scope_expr(e: Expression, scope: Scope) -> Expression:
    """Resolve all variable scopes in this expression (and child expressions). e.g. Name -> LocalName or GlobalName."""
    # print("DEBUG %s, localvars %s" % (e, localvars))
    match e:
        case Name(t, x):
            if scope.getscope(x) == "local":
                return LocalName(t, x)
            elif scope.getscope(x) == "global":
                return GlobalName(t, x)
            else:
                raise RuntimeError("Name %s referenced before definition" % x)
        case Add(t, x, y):
            return Add(t, 
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Multiply(t, x, y):
            return Multiply(t, 
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Subtract(t, x, y):
            return Subtract(t, 
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Divide(t, x, y):
            return Divide(t, 
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Modulo(t, x, y):
            return Modulo(t, 
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case CallFn(t, name, params):
            # resolve scope of any variable passed as parameter
            return CallFn(t, name, [resolve_scope_expr(p, scope) for p in params])
        case Relation(t, op, left, right):
            return Relation(t, op, resolve_scope_expr(left, scope), resolve_scope_expr(right, scope))
        case Integer() | RelationOp():
            return e
        case _:
            raise RuntimeError(f"Unhandled resolve_scope Expression {e}")


# print(prog)
# print(format_program(resolve_scopes(prog)))
# quit()

######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    ast = Program(
        [
            Declare(Name(TEST_TYPE, "x")),
            Assign(Name(TEST_TYPE, "x"), Integer(TEST_TYPE, 42)),
            Function(
                Name(TEST_TYPE, "f"),
                [Name(TEST_TYPE, "y")],
                [Declare(Name(TEST_TYPE, "t")), Assign(Name(TEST_TYPE, "t"), Multiply(TEST_TYPE,Name(TEST_TYPE, "x"), Name(TEST_TYPE, "y"))), Return(Name(TEST_TYPE, "t"))],
            ),
            Function(
                Name(TEST_TYPE, "g"),
                [Name(TEST_TYPE, "x")],
                [Return(Name(TEST_TYPE, "x"))],
            ),
            # CHECK: The 'x' in h(z) should be global x, as the local x from g(x) was for that function only...
            Function(
                Name(TEST_TYPE, "h"),
                [Name(TEST_TYPE, "z")],
                [Return(Name(TEST_TYPE, "x"))],
            ),
            IfElse(
                Relation(TEST_TYPE,RelationOp("=="), Name(TEST_TYPE, "x"), Integer(TEST_TYPE, 5)),
                [  # CHECK: this x should be local because it's declared inside an If
                    Declare(Name(TEST_TYPE, "x")),
                    Assign(Name(TEST_TYPE, "x"), Integer(TEST_TYPE, 13)),
                    Print(CallFn(TEST_TYPE,Name(TEST_TYPE, "f"), [Name(TEST_TYPE, "x")])),
                ],
                [
                    # CHECK: this x should be global again since x is not declared locally in the else
                    Print(Name(TEST_TYPE, "x"))
                ],
            ),
            # CHECK: this x should be global
            Print(Name(TEST_TYPE, "x")),
        ]
    )
    # print(ast)
    #    print(format_program(ast))
    #    print("-- resolve_scopes() test --")
    #    print(resolve_scopes(ast))
    #    printcolor(format_program(resolve_scopes(ast)))

    assert resolve_scopes(ast) == Program(
        [
            GlobalVar(Name(TEST_TYPE, "x")),
            Assign(GlobalName(TEST_TYPE, "x"), Integer(TEST_TYPE, 42)),
            Function(
                Name(TEST_TYPE, "f"),
                [Name(TEST_TYPE, "y")],
                [
                    LocalVar(Name(TEST_TYPE, "t")),
                    Assign(LocalName(TEST_TYPE, "t"), Multiply(TEST_TYPE,GlobalName(TEST_TYPE, "x"), LocalName(TEST_TYPE, "y"))),
                    Return(LocalName(TEST_TYPE, "t")),
                ],
            ),
            Function(Name(TEST_TYPE, "g"), [Name(TEST_TYPE, "x")], statements=[Return(LocalName(TEST_TYPE, "x"))]),
            Function(Name(TEST_TYPE, "h"), [Name(TEST_TYPE, "z")], statements=[Return(GlobalName(TEST_TYPE, "x"))]),
            IfElse(
                Relation(TEST_TYPE,RelationOp("=="), GlobalName(TEST_TYPE, "x"), Integer(TEST_TYPE, 5)),
                [
                    LocalVar(Name(TEST_TYPE, "x")),
                    Assign(LocalName(TEST_TYPE, "x"), Integer(TEST_TYPE, 13)),
                    Print(CallFn(TEST_TYPE,Name(TEST_TYPE, "f"), [LocalName(TEST_TYPE, "x")])),
                ],
                [Print(GlobalName(TEST_TYPE, "x"))],
            ),
            Print(GlobalName(TEST_TYPE, "x")),
        ]
    )

    # Now intentionally throw an undefined variable error
    ast = Program(
        [
            Function(
                Name(TEST_TYPE, "f"),
                [Name(TEST_TYPE, "y")],
                [Declare(Name(TEST_TYPE, "t")), Assign(Name(TEST_TYPE, "t"), Multiply(TEST_TYPE,Name(TEST_TYPE, "x"), Name(TEST_TYPE, "y"))), Return(Name(TEST_TYPE, "t"))],
            ),
            Print(Name(TEST_TYPE, "t")),
        ]
    )
    #    print("----\n%s" % format_program(ast))
    #    print("-- resolve_scopes() test, should give undefined variable error --")
    # print(resolve_scopes(ast))
    try:
        format_program(resolve_scopes(ast))
    except RuntimeError as err:
        #        printcolor(str(err), ansicode.yellow)
        assert str(err) == "Name t referenced before definition"

    printcolor("minimal tests PASSED", ansicode.green)
