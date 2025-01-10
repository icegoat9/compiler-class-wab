# controlflow.py
"""Translate flow control statements to assembly-style GOTO / CBRANCH structures.

Take in a program where groups of consecutive statements have already been converted to BLOCK() objects 
with globally unique labels, and figures out how to translate If / While / Function structures into
appropriate GOTO and CBRANCH statements. This step was one of the most challenging to think through in
terms of how to link the blocks and labels.

One of the most challenging aspects was determining which 'next label' to jump to after a structure
(for example, after exiting a While loop). The current implementation determines this by working up
from the bottom of the program.

Previous compiler stage: basicblocks.py
Next compiler stage: llvmcode.py"""
#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests

# see controlflow_test1.txt for 3/21 9:54AM status:
# We are linking blocks! but, issues:
# [X] What label should end of program jump to? The passed L100, I guess this is ok?
# [X] End of If blocks should be jumping to L4, not L100 -- which next_label gets passed in link_blocks()
# [X] Block before the If conditional needs to jump to If conditional
# [X] Need to autonumber the If conditional (not just pass it L99)
# [X] Nested If, While, etc-- and also, places where I assumed the # of Blocks is exactly 1, when it could be more
# [ ] Trim dead instructions e.g. GOTO after a RETURN and so on
# [ ]    Remove HACKy special-case handling of this in link_toplevel_statements()
# [ ]    Replace "L_err_should have..." argument in link_toplevel_statements() with... what?
# [ ] Maybe: rename/renumber blocks so all blocks within a (function, statement list, etc) are adjacent

from model import *
from format import *
from label_global import *
from debughelper import *


def flow_program(program: Program) -> Program:
    """Run control flow translation process on entire program."""
    return Program(link_toplevel_statements(program.statements))


def link_toplevel_statements(statements: list[Statement]) -> list[Statement]:
    """Process the top-level program (which at this stage in the compiler consists of only
    GlobalVar definition and Function definitions, as core user code has been moved into a
    main() function in an earlier compiler step."""
    output = []
    for s in statements:
        match s:
            case Function(name, params, body):
                bodystatements = link_statements(body, "L_err_should_have_RETURNed")
                # HACK: Now trim the GOTO(L_err) we know bodystatments added to the function's last
                #        BLOCK, since we know functions ended with Return
                # TODO: move this to a more general trim function that actually checks,
                #       in case there's an error and function definition didn't end with return!
                bodystatements[-1].instructions.pop()
                func = Function(name, params, bodystatements)
                output.append(func)
            case GlobalVar():
                output.append(s)
            case _:
                raise SyntaxError(f"Unhandled statement type {s}")
    return output


def link_statements(statements: list[Statement], next_label: str) -> list[BLOCK]:
    """Link the blocks in a list of statements, including descending into If / While structures.
    Intended to be run on the statements found inside an enclosing structure (Function, If/While, etc),
    not the top-level program: does not handle global variable or function definitions.
    """
    # pointer to work backwards
    i = len(statements) - 1
    blocks = []
    while i >= 0:
        statement = statements[i]
        match statement:
            case BLOCK() | While() | IfElse():
                temp_blocks = link_blocks(statement, next_label, debug=False)
                next_label = temp_blocks[0].label
                blocks = temp_blocks + blocks
            case _:
                raise SyntaxError(f"Unhandled statement type {statement}")
        i -= 1
    return blocks


def link_blocks(statement: Statement, next_label: str, debug: bool = False) -> list[BLOCK]:
    """Add the appropriate flow control statement (GOTO or CBRANCH) to the end of the passed statement.
    At this stage in the compile process, statement can only be one of a few objects: BLOCK(), IfElse(),
    or While().

    The passed next_label value is critical: it indicates the label of the BLOCK() that comes after this
    statement (for example, where a While() continues to after exiting the loop, or an IfElse after
    processing the If or Else cases).
    """
    # if debug==True, always get "L99" from get_next_label(), for easier assertion testing
    blocks = []
    match statement:
        case While(condition, body):
            # simple While body without nested If/While inside will just contain one statement (a BLOCK)
            #   but could contain several (e.g. [BLOCK, IfElse, BLOCK] )
            #   last BLOCK is what needs to have the GOTO(next_label) added to it
            # label of the While's conditional
            #   (note: the block _before_ the While will need to add a jump to this label,
            #   so we'll need to pass it as next_label to that previous block when we get to it)
            cond_label = get_next_label(debug_force_L99=debug)
            # process statements in the body as it could contain nested If / While..
            #  and tell link_statements to add a GOTO(cond_label) to the end to loop back
            #  (which it will do by calling link_blocks and hitting the case BLOCK(): statement below...)
            body_blocks = link_statements(body, cond_label)
            # create the new block for the conditional (a label, eval conditional, cbranch)
            #  note: at end of conditional, branch to either the label of the first body block or past the While
            cond_block = BLOCK(cond_label, condition.instructions + [CBRANCH(body_blocks[0].label, next_label)])
            return [cond_block] + body_blocks
        case IfElse(condition, ifbody, elsebody):
            # Note: see While above for more explanation
            cond_label = get_next_label(debug_force_L99=debug)
            # process statements in the If/Else bodies as they could contain nested If/While
            #  and tell link_statements to add a GOTO(next label after the If/Else block) at the end
            if_blocks = link_statements(ifbody, next_label)
            # TODO: modify this area below to not return empty else_blocks below if no elsebody,
            #       to handle missing (not only empty) elsebody (requires parser change as it currently inserts empty else body, etc)
            else_blocks = link_statements(elsebody, next_label)
            # if there is an else body with content
            if elsebody:
                # build up the block for the conditional (a label, eval conditional, cbranch)
                cond_block = BLOCK(
                    cond_label, condition.instructions + [CBRANCH(if_blocks[0].label, else_blocks[0].label)]
                )
            else:
                # no else body, or empty else body (parser inserts empty else body, currently)
                # so just jump to following block
                cond_block = BLOCK(cond_label, condition.instructions + [CBRANCH(if_blocks[0].label, next_label)])
            return [cond_block] + if_blocks + else_blocks
        case BLOCK(label, instructions):
            # General code block (not If, While, Function), create a link from this block to the next one
            return [BLOCK(label, instructions + [GOTO(next_label)])]
        case _:
            raise SyntaxError(f"Unhandled statement type {statement}")


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":

    s = BLOCK(label="L2", instructions=[LOAD_GLOBAL("x"), STORE_GLOBAL("min")])
    assert link_blocks(s, "L3") == [BLOCK(label="L2", instructions=[LOAD_GLOBAL("x"), STORE_GLOBAL("min"), GOTO("L3")])]

    s = While(
        EXPR(instructions=[LOAD_GLOBAL("x"), LOAD_GLOBAL("y"), LT()]),
        [BLOCK(label="L2", instructions=[LOAD_GLOBAL("x"), STORE_GLOBAL("min")])],
    )
    # print("--- While statement in:\n%s" % s)
    # print("--- BLOCKS out:")
    # printcolor(link_blocks(s, "L9", debug=True))
    assert link_blocks(s, "L9", debug=True) == [
        BLOCK(label="L99", instructions=[LOAD_GLOBAL("x"), LOAD_GLOBAL("y"), LT(), CBRANCH(iftrue="L2", iffalse="L9")]),
        BLOCK(label="L2", instructions=[LOAD_GLOBAL("x"), STORE_GLOBAL("min"), GOTO("L99")]),
    ]

    s = IfElse(
        EXPR(instructions=[LOAD_GLOBAL("x"), LOAD_GLOBAL("y"), LT()]),
        [BLOCK(label="L2", instructions=[LOAD_GLOBAL("x"), STORE_GLOBAL("min")])],
        [BLOCK(label="L3", instructions=[LOAD_GLOBAL("y"), STORE_GLOBAL("min")])],
    )

    assert link_blocks(s, "L9", debug=True) == [
        BLOCK(label="L99", instructions=[LOAD_GLOBAL("x"), LOAD_GLOBAL("y"), LT(), CBRANCH(iftrue="L2", iffalse="L3")]),
        BLOCK(label="L2", instructions=[LOAD_GLOBAL("x"), STORE_GLOBAL("min"), GOTO("L9")]),
        BLOCK(label="L3", instructions=[LOAD_GLOBAL("y"), STORE_GLOBAL("min"), GOTO("L9")]),
    ]

    printcolor("link_blocks() unit tests on simple single BLOCK, While, IfElse PASSED", ansicode.green)

    ## tests/program2.wab
    #  var x = 3;
    #  var y = 4;
    #  var min = 0;
    #  if x < y {
    #    min = x;
    #  } else {
    #    min = y;
    #  }
    #  print min;

    # Slightly more complex AST, a few blocks that would be body of a function, thus the RETURN at the end
    prog = Program(
        [
            BLOCK(
                label="L1",
                instructions=[
                    PUSH(3),
                    STORE_GLOBAL("x"),
                ],
            ),
            IfElse(
                condition=EXPR(instructions=[LOAD_GLOBAL("x"), PUSH(4), LT()]),
                iflist=[BLOCK(label="L2", instructions=[PUSH(5), STORE_GLOBAL("min")])],
                elselist=[BLOCK(label="L3", instructions=[])],
            ),
            BLOCK(label="L4", instructions=[LOAD_GLOBAL("min"), PRINT(), PUSH(0), RETURN()]),
        ]
    )

    #    print("--- BLOCKed program:")
    #    printcolor(prog)
    # Hack for deterministic testing to hard-code the next label to use --
    #  in normal use, this module would be run right after basicblocks.py and would pick up the
    #  'next available global label' from there
    init_global_label(4)
    prog2 = Program(link_statements(prog.statements, "L100"))
    #    print("--- after Control Flow processing:")
    #    printcolor(prog2)
    #    print("--- BLOCKed program:")
    #    printcolor(format_program(prog))
    #    print("--- after Control Flow processing:")
    #    printcolor(format_program(prog2))

    assert_equal_verbose(
        prog2,
        Program(
            statements=[
                BLOCK(label="L1", instructions=[PUSH(3), STORE_GLOBAL("x"), GOTO(label="L5")]),
                BLOCK(label="L5", instructions=[LOAD_GLOBAL("x"), PUSH(4), LT(), CBRANCH(iftrue="L2", iffalse="L3")]),
                BLOCK(label="L2", instructions=[PUSH(5), STORE_GLOBAL("min"), GOTO(label="L4")]),
                BLOCK(label="L3", instructions=[GOTO(label="L4")]),
                BLOCK(label="L4", instructions=[LOAD_GLOBAL("min"), PRINT(), PUSH(0), RETURN(), GOTO(label="L100")]),
            ]
        ),
    )

    printcolor("link_statements() unit test PASSED", ansicode.green)

    # program2.wb AST after all previous steps through py:
    prog = Program(
        [
            GlobalVar(name=Name(str="x")),
            GlobalVar(name=Name(str="y")),
            GlobalVar(name=Name(str="min")),
            Function(
                name=Name(str="main"),
                params=[],
                statements=[
                    BLOCK(
                        label="L1",
                        instructions=[
                            PUSH(3),
                            STORE_GLOBAL("x"),
                            PUSH(4),
                            STORE_GLOBAL("y"),
                            PUSH(0),
                            STORE_GLOBAL("min"),
                        ],
                    ),
                    IfElse(
                        condition=EXPR(instructions=[LOAD_GLOBAL("x"), LOAD_GLOBAL("y"), LT()]),
                        iflist=[BLOCK(label="L2", instructions=[LOAD_GLOBAL("x"), STORE_GLOBAL("min")])],
                        elselist=[BLOCK(label="L3", instructions=[LOAD_GLOBAL("y"), STORE_GLOBAL("min")])],
                    ),
                    BLOCK(label="L4", instructions=[LOAD_GLOBAL("min"), PRINT(), PUSH(0), RETURN()]),
                ],
            ),
        ]
    )

    # Hack for deterministic testing to hard-code the next label to use --
    #  in normal use, this module would be run right after basicblocks.py and would pick up the
    #  'next available global label' from there
    init_global_label(4)
    prog2 = Program(link_toplevel_statements(prog.statements))
    assert_equal_verbose(
        prog2,
        Program(
            statements=[
                GlobalVar(name=Name(str="x")),
                GlobalVar(name=Name(str="y")),
                GlobalVar(name=Name(str="min")),
                Function(
                    name=Name(str="main"),
                    params=[],
                    statements=[
                        BLOCK(
                            label="L1",
                            instructions=[
                                PUSH(3),
                                STORE_GLOBAL("x"),
                                PUSH(4),
                                STORE_GLOBAL("y"),
                                PUSH(0),
                                STORE_GLOBAL("min"),
                                GOTO(label="L5"),
                            ],
                        ),
                        BLOCK(
                            label="L5",
                            instructions=[
                                LOAD_GLOBAL("x"),
                                LOAD_GLOBAL("y"),
                                LT(),
                                CBRANCH(iftrue="L2", iffalse="L3"),
                            ],
                        ),
                        BLOCK(label="L2", instructions=[LOAD_GLOBAL("x"), STORE_GLOBAL("min"), GOTO(label="L4")]),
                        BLOCK(label="L3", instructions=[LOAD_GLOBAL("y"), STORE_GLOBAL("min"), GOTO(label="L4")]),
                        BLOCK(label="L4", instructions=[LOAD_GLOBAL("min"), PRINT(), PUSH(0), RETURN()]),
                    ],
                ),
            ]
        ),
    )

    #    print("--- after Control Flow processing:")
    #    printcolor(prog2)
    #    print("--- BLOCKed program:")
    #    printcolor(format_program(prog))
    #    print("--- after Control Flow processing:")
    #    print(prog2)
    #    printcolor(format_program(prog2))

    printcolor("unit tests on sample programs PASSED", ansicode.green)
