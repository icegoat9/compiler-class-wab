"""Generate Python program from the Wab program model / AST. (early prototype / experiment)

TBD: which stage of compilation we are ready to run this at. Perhaps this diverges in parallel at the same
stage that expression_instructions.py does-- that is, after defaultreturns.py or slightly earlier?
"""

# TODOs
# [ ] Remove the outer parentheses in generated expression strings by passing a 'nested' bool to py_expression
# [ ] Don't move body code into main() ? That would mean not running an earlier compiler pass in compile_to_python.py
# [ ] Globals are not handled, here-- assumes all locals

from model import *
from printcolor import *
from format import *
from debughelper import *

INDENT = "    "

@dataclass
class PY_STATEMENT(Statement):
    val: list[Statement]


@dataclass
class PY_EXPR(Expression):
    val: str


def py_program(program: Program) -> str:
    """Return the string representation (with human-friendly formatting) of a Python translation of program."""
    ps = ['# created by gen_python.py (work in progress)']
    ps.extend(py_statements(program.statements))
    ps.extend(['if __name__ == "__main__":',INDENT + 'main()'])
    return "\n".join(ps)
    

    return "\n".join(py_statements(program.statements))

def py_statements(statements: list[Statement]) -> list[Statement]:
    """Translate a list of statements (main program or body of flow control) to Python strings."""
    ss = []
    for s in statements:
        ss.extend(py_statement(s))
    return empty_to_pass(ss)

def empty_to_pass(statements: list[Statement]) -> list[Statement]:
    """Replace empty list of statements with 'pass' command for Python empty If/Else/etc bodies."""
    return statements or ["pass"]


def py_statement(s: Statement) -> list[Statement]:
    match s:
        case Print(x):
            return [f"print({py_expression(x)})"]
        case GlobalVar() | LocalVar():
            return []
        case Assign(GlobalName(x), y):
            return [f"{x} = {py_expression(y)}"]
            #TODO: handle globals, should be rare
#            return [f"global {x}", f"{x} = {py_expression(y)}"]
        case Assign(LocalName(x), y):
            return [f"{x} = {py_expression(y)}"]
        case Function(Name(name), params, code):
            pstr = ", ".join([p.str for p in params])
            out = [f"def {name}({pstr}):"]
            out.extend([INDENT + pys for pys in py_statements(code)])
            out.append("")
            return out
            # 3 lines above are equivalent to single line:
            # return [f"def {f}({pstr}):"] + [INDENT + pys for pys in py_statements(code)]
        case Return(x):
            return [f"return {py_expression(x)}"]
        case IfElse(relation, iflist, elselist):
            out = [f"if {py_expression(relation)}:"]
            out.extend([INDENT + pys for pys in py_statements(iflist)])
            out.append("else:")
            out.extend([INDENT + pys for pys in py_statements(elselist)])
            return out
        case While(relation, iflist):
            out = [f"while {py_expression(relation)}:"]
            out.extend([INDENT + pys for pys in py_statements(iflist)])
            return out
        case _:
            raise RuntimeError(f"Unhandled statement {s}")


def py_expression(expr: Expression) -> str:
    """Transform a single expression to its PY_EXPR() representation. This calls itself
    recursively on parameters of many expressions, to process nested expressions?"""
    match expr:
        case Integer(x):
            return str(x)
        case Add(left, right):
            return f"({py_expression(left)} + {py_expression(right)})"
        case Multiply(left, right):
            return f"({py_expression(left)} * {py_expression(right)})"
        case Subtract(left, right):
            return f"({py_expression(left)} - {py_expression(right)})"
        case Divide(left, right):
            # // = integer division
            return f"({py_expression(left)} // {py_expression(right)})"
        case Relation(op, left, right):
            return f"({py_expression(left)} {op.name} {py_expression(right)})"
        case Name(x):
            return x
        case LocalName(Name(x)):
            return x
        case GlobalName(Name(x)):
            return x  # TODO: fix with initial function global declaration?
        case CallFn(Name(fname), params):
            pstr = ", ".join([py_expression(p) for p in params])
            return f"{fname}({pstr})"
        case _:
            raise RuntimeError("Can't generate PY_EXPR code for Expression %s" % expr)

######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    #    assert_equal_verbose(py_expression(Add(Integer(2), GlobalName("x"))), PY_EXPR(["global x","(2 + x)"]))
    assert_equal_verbose(py_expression(Add(Integer(2), LocalName("x"))), "(2 + x)")
    assert_equal_verbose(py_expression(Relation(RelationOp("<"), Integer(5), GlobalName("x"))), "(5 < x)")

    assert_equal_verbose(py_statement(Print(Add(Integer(2), GlobalName("x")))), ["print((2 + x))"])
    assert_equal_verbose(
        py_statement(
            IfElse(
                Relation(RelationOp("<"), Integer(5), GlobalName("x")),
                [Print(Add(Integer(1), GlobalName("x")))],
                [Print(Add(Integer(2), GlobalName("x")))],
            ),
        ),
        ['if (5 < x):', INDENT+'print((1 + x))', 'else:', INDENT+'print((2 + x))'],
    )
    printcolor("unit tests PASSED", ansicode.green)
    prog = Program(
            [
                Function(
                    Name("f"),
                    [Name("y")],
                    [
                        IfElse(
                            Relation(RelationOp("=="), Name("y"), Integer(5)),
                            [Return(Name("y"))],
                            [Print(Name("y"))],
                        ),
                        Return(Integer(0)),
                    ],
                ),
                Function(
                    Name("g"),
                    [Name("y")],
                    [Return(Name("y"))],
                ),
                IfElse(
                    Relation(RelationOp("=="), Name("y"), Integer(5)),
                    [Print(Name("y"))],
                    [],
                ),
                # CHECK: this x should be global
                Print(Name("x")),
            ]
        )
    print(py_program(prog))
