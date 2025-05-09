# resolve.py
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
    if relevenat). For example, the generic Declare class becomes GlobalVar or LocalVar."""
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
                return LocalName(DUMMYTYPE, x)
            elif scope.getscope(x) == "global":
                return GlobalName(DUMMYTYPE, x)
            else:
                raise RuntimeError("Name %s referenced before definition" % x)
        case Add(t, x, y):
            return Add(DUMMYTYPE, 
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Multiply(t, x, y):
            return Multiply(DUMMYTYPE, 
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Subtract(t, x, y):
            return Subtract(DUMMYTYPE, 
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Divide(t, x, y):
            return Divide(DUMMYTYPE, 
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case Modulo(t, x, y):
            return Modulo(DUMMYTYPE, 
                resolve_scope_expr(x, scope),
                resolve_scope_expr(y, scope),
            )
        case CallFn(t, name, params):
            # resolve scope of any variable passed as parameter
            return CallFn(DUMMYTYPE, name, [resolve_scope_expr(p, scope) for p in params])
        case Relation(t, op, left, right):
            return Relation(DUMMYTYPE, op, resolve_scope_expr(left, scope), resolve_scope_expr(right, scope))
        case Integer() | RelationOp():
            return e
        case _:
            raise RuntimeError(f"Unhandled resolve_scope Expression {e}")


# prog = Program([While(Relation(RelationOp("<"), Name(DUMMYTYPE, "x"), Integer(DUMMYTYPE, 5)),[Return(Integer(DUMMYTYPE, 5))])])
# print(prog)
# print(format_program(resolve_scopes(prog)))
# quit()

######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    ast = Program(
        [
            Declare(Name(DUMMYTYPE, "x")),
            Assign(Name(DUMMYTYPE, "x"), Integer(DUMMYTYPE, 42)),
            Function(
                Name(DUMMYTYPE, "f"),
                [Name(DUMMYTYPE, "y")],
                [Declare(Name(DUMMYTYPE, "t")), Assign(Name(DUMMYTYPE, "t"), Multiply(DUMMYTYPE,Name(DUMMYTYPE, "x"), Name(DUMMYTYPE, "y"))), Return(Name(DUMMYTYPE, "t"))],
            ),
            Function(
                Name(DUMMYTYPE, "g"),
                [Name(DUMMYTYPE, "x")],
                [Return(Name(DUMMYTYPE, "x"))],
            ),
            # CHECK: The 'x' in h(z) should be global x, as the local x from g(x) was for that function only...
            Function(
                Name(DUMMYTYPE, "h"),
                [Name(DUMMYTYPE, "z")],
                [Return(Name(DUMMYTYPE, "x"))],
            ),
            IfElse(
                Relation(DUMMYTYPE,RelationOp("=="), Name(DUMMYTYPE, "x"), Integer(DUMMYTYPE, 5)),
                [  # CHECK: this x should be local because it's declared inside an If
                    Declare(Name(DUMMYTYPE, "x")),
                    Assign(Name(DUMMYTYPE, "x"), Integer(DUMMYTYPE, 13)),
                    Print(CallFn(DUMMYTYPE,Name(DUMMYTYPE, "f"), [Name(DUMMYTYPE, "x")])),
                ],
                [
                    # CHECK: this x should be global again since x is not declared locally in the else
                    Print(Name(DUMMYTYPE, "x"))
                ],
            ),
            # CHECK: this x should be global
            Print(Name(DUMMYTYPE, "x")),
        ]
    )
    # print(ast)
    #    print(format_program(ast))
    #    print("-- resolve_scopes() test --")
    #    print(resolve_scopes(ast))
    #    printcolor(format_program(resolve_scopes(ast)))

    assert resolve_scopes(ast) == Program(
        [
            GlobalVar(Name(DUMMYTYPE, "x")),
            Assign(GlobalName(DUMMYTYPE, "x"), Integer(DUMMYTYPE, 42)),
            Function(
                Name(DUMMYTYPE, "f"),
                [Name(DUMMYTYPE, "y")],
                [
                    LocalVar(Name(DUMMYTYPE, "t")),
                    Assign(LocalName(DUMMYTYPE, "t"), Multiply(DUMMYTYPE,GlobalName(DUMMYTYPE, "x"), LocalName(DUMMYTYPE, "y"))),
                    Return(LocalName(DUMMYTYPE, "t")),
                ],
            ),
            Function(Name(DUMMYTYPE, "g"), [Name(DUMMYTYPE, "x")], statements=[Return(LocalName(DUMMYTYPE, "x"))]),
            Function(Name(DUMMYTYPE, "h"), [Name(DUMMYTYPE, "z")], statements=[Return(GlobalName(DUMMYTYPE, "x"))]),
            IfElse(
                Relation(DUMMYTYPE,RelationOp("=="), GlobalName(DUMMYTYPE, "x"), Integer(DUMMYTYPE, 5)),
                [
                    LocalVar(Name(DUMMYTYPE, "x")),
                    Assign(LocalName(DUMMYTYPE, "x"), Integer(DUMMYTYPE, 13)),
                    Print(CallFn(DUMMYTYPE,Name(DUMMYTYPE, "f"), [LocalName(DUMMYTYPE, "x")])),
                ],
                [Print(GlobalName(DUMMYTYPE, "x"))],
            ),
            Print(GlobalName(DUMMYTYPE, "x")),
        ]
    )

    # Now intentionally throw an undefined variable error
    ast = Program(
        [
            Function(
                Name(DUMMYTYPE, "f"),
                [Name(DUMMYTYPE, "y")],
                [Declare(Name(DUMMYTYPE, "t")), Assign(Name(DUMMYTYPE, "t"), Multiply(DUMMYTYPE,Name(DUMMYTYPE, "x"), Name(DUMMYTYPE, "y"))), Return(Name(DUMMYTYPE, "t"))],
            ),
            Print(Name(DUMMYTYPE, "t")),
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
