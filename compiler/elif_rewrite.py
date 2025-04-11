# elif_rewrite.py
"""Replaces all If..Elif..Else structures in the AST with nested If..Else structures.

Run this early after parsing (currently staged as the first operation after the parser), 
as most later compiler passes only understand how to traverse If..Else structures.

This iteratively / recursively descends into If / Elif / Else / While / For structures as these
structures may be nested within each other.
"""

# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests
# [ ] add unit test for structure within a For statement? (new untested language feature)

from model import *
from format import *


def elif_program(program: Program) -> Program:
    """Process program, rewrite elif to if..else, return new program."""
    return Program(elif_statements(program.statements))


def elif_statements(statements: list[Statement]) -> list[Statement]:
    """Process a list of statements, rewriting elif to if..else.

    Run on the main program, but also called recurively while processing the bodies of control flow structures.
    """
    slist = []
    # TODO: some better way to replace for loop with a list comprehension?
    for s in statements:
        # extend = append each statement from list elif_statments() one by one
        slist.extend(elif_statement(s))
    return slist


def elif_statement(s: Statement) -> list[Statement]:
    """Process single statement, return list of processed statements (possibly just containing one item).

    If an IfElifElse object is found, recursively break it into nested If..Else..If..Else statements.

    Also process the statement bodies of (While, If, Function) to look for nested structures.
    """
    match s:
        case IfElse(relation, iflist, elselist):
            return [IfElse(relation, elif_statements(iflist), elif_statements(elselist))]
        case While(relation, body):
            return [While(relation, elif_statements(body))]
        case For(name, startval, endval, body):
            return [For(name, startval, endval, elif_statements(body))]
        case Function(name, params, body):
            return [Function(name, params, elif_statements(body))]
        case IfElifElse(relation, iflist, elifs, elselist):
            # the conceptual sequence parsing "from the last elif clause backwards":
            # if(a) {foo},   elif(b} {bar},   elif(c) {baz},   else {moo} ->
            # if(a) {foo},   elif(b} {bar},   else { if(c) {baz},   else {moo} } ->
            # if(a) {foo},   else { if(b) {bar},   else { if(c) {baz},   else {moo} }}
            if elifs:
                last_elif = elifs.pop()  # also removes it from elifs
                return elif_statement(
                    IfElifElse(
                        relation,
                        elif_statements(iflist),
                        elifs,  # the new shortened-by-one list of elifs to process
                        [IfElse(last_elif.condition, elif_statements(last_elif.iflist), elif_statements(elselist))],
                    )
                )
            else:
                return [IfElse(relation, elif_statements(iflist), elif_statements(elselist))]
        case _:
            return [s]


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    prog = Program(
        [
            DeclareValue(Name("x"), Integer(1)),
            IfElifElse(
                Relation(RelationOp(">"), Name("x"), Integer(2)),
                [Print(Integer(99))],
                [
                    IfElse(Relation(RelationOp("=="), Name("x"), Integer(2)), [Print(Integer(2))], []),
                    IfElse(Relation(RelationOp("=="), Name("x"), Integer(1)), [Print(Integer(1))], []),
                ],
                [Print(Integer(0))],
            ),
        ]
    )
    # print(format_program(prog))
    out = elif_program(prog)
    # print(format_program(out))
    assert out == Program(
        [
            DeclareValue(Name("x"), Integer(1)),
            IfElse(
                Relation(RelationOp(">"), Name("x"), Integer(2)),
                [Print(Integer(99))],
                [
                    IfElse(
                        Relation(RelationOp("=="), Name("x"), Integer(2)),
                        [Print(Integer(2))],
                        [
                            IfElse(
                                Relation(RelationOp("=="), Name("x"), Integer(1)),
                                [Print(Integer(1))],
                                [Print(Integer(0))],
                            )
                        ],
                    )
                ],
            ),
        ]
    )

    prog = Program(
        [
            DeclareValue(Name("x"), Integer(1)),
            While(
                Relation(RelationOp("=="), Name("x"), Integer(1)),
                [
                    IfElifElse(
                        Relation(RelationOp(">"), Name("x"), Integer(2)),
                        [Print(Integer(99))],
                        [
                            IfElse(
                                Relation(RelationOp("=="), Name("x"), Integer(2)),
                                [
                                    IfElifElse(
                                        Relation(RelationOp(">"), Name("y"), Integer(10)),
                                        [Print(Integer(999))],
                                        [
                                            IfElse(
                                                Relation(RelationOp("=="), Name("y"), Integer(5)),
                                                [Print(Integer(555))],
                                                [],
                                            ),
                                            IfElse(
                                                Relation(RelationOp("=="), Name("y"), Integer(4)),
                                                [Print(Integer(444))],
                                                [],
                                            ),
                                        ],
                                        [Print(Integer(333))],
                                    ),
                                ],
                                [],
                            ),
                            IfElse(Relation(RelationOp("=="), Name("x"), Integer(1)), [Print(Integer(1))], []),
                        ],
                        [Print(Integer(0))],
                    ),
                ],
            ),
        ]
    )
    print(format_program(prog))
    out = elif_program(prog)
    print(format_program(out))
    #    print(out)
    assert out == Program(
        [
            DeclareValue(Name("x"), Integer(1)),
            While(
                Relation(RelationOp("=="), Name("x"), Integer(1)),
                [
                    IfElse(
                        Relation(RelationOp(">"), Name("x"), Integer(2)),
                        [Print(value=Integer(99))],
                        [
                            IfElse(
                                Relation(RelationOp("=="), Name("x"), Integer(2)),
                                [
                                    IfElse(
                                        Relation(RelationOp(">"), Name("y"), Integer(10)),
                                        [Print(value=Integer(999))],
                                        [
                                            IfElse(
                                                Relation(RelationOp("=="), Name("y"), Integer(5)),
                                                [Print(value=Integer(555))],
                                                [
                                                    IfElse(
                                                        Relation(RelationOp("=="), Name("y"), Integer(4)),
                                                        [Print(value=Integer(444))],
                                                        [Print(value=Integer(333))],
                                                    )
                                                ],
                                            )
                                        ],
                                    )
                                ],
                                [
                                    IfElse(
                                        Relation(RelationOp("=="), Name("x"), Integer(1)),
                                        [Print(value=Integer(1))],
                                        [Print(value=Integer(0))],
                                    )
                                ],
                            )
                        ],
                    )
                ],
            ),
        ]
    )

    printcolor("tests PASSED", ansicode.green)
