# basicblocks.py
"""Convert all groups of statements in program to BLOCK() structures with globally unique labels 
(in preparation for a later compiler step which will transform If / While / Function
type flow control with GOTO and BRANCH flow control)."""
#
# Cleanup TODO
# [X] docstrings
# [X] assertion-based unit tests

from model import *
from format import *
from debughelper import *
from label_global import *


def blocks_program(program: Program) -> Program:
    """Convert program STATEMENTs to BLOCKs.

    NOTE: This is the first step in the compiler pipeline to generate blocks,
    so this initializes the global label index as well."""
    init_global_label(0)
    return Program(statements_to_blocks(program.statements))


def statements_to_blocks(statements: list[Statement]) -> list[Statement]:
    """Convert a list of Statements to list of BLOCK() structures.

    Multiple consecutive statements will be grouped into a single BLOCK with a globally unique label.
    Flow control related statements are left untouched for now, to process in a later step, but this
    function does recursively descend into each one to process the statement lists within it.
    """
    progout = []
    blocklist = []
    for s in statements:
        match s:
            case STATEMENT(body):
                # Check if we already have a running BLOCK(... being filled)
                if progout and isinstance(progout[-1], BLOCK):
                    progout[-1].instructions.extend(body)
                else:
                    progout.append(BLOCK(get_next_label(), body))
            case Function(name, params, body):
                progout.append(Function(name, params, statements_to_blocks(body)))
            case While(condition, body):
                progout.append(While(condition, statements_to_blocks(body)))
            case IfElse(condition, ifbody, elsebody):
                progout.append(IfElse(condition, statements_to_blocks(ifbody), statements_to_blocks(elsebody)))
            case _:
                progout.append(s)
    if len(blocklist) > 0:
        progout.append(BLOCK(get_next_label(), blocklist))
    return progout


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    # run unit tests on three ASTs of increasing complexity
    # (print-style debugging commands included but commented out)

    # tests/program1.wab
    prog = Program(
        [
            GlobalVar(name=Name(str="x")),
            STATEMENT(instructions=[PUSH(value=10), STORE_GLOBAL(name="x")]),
            STATEMENT(instructions=[LOAD_GLOBAL(name="x"), PUSH(value=1), ADD(), STORE_GLOBAL(name="x")]),
            STATEMENT(instructions=[PUSH(value=1035), LOAD_GLOBAL(name="x"), ADD(), PRINT()]),
            STATEMENT(instructions=[PUSH(value=0), RETURN()]),
        ]
    )
    #    print_colorheader("--- Raw program data structure:", prog)
    #    print_colorheader("--- Formatted:", format_program(prog))
    p2 = blocks_program(prog)
    #    print_colorheader("--- After BLOCKing::", p2)
    #    print_colorheader("--- Formatted:", format_program(p2))

    assert_equal_verbose(
        p2,
        Program(
            [
                GlobalVar(name=Name(str="x")),
                BLOCK(
                    label="L1",
                    instructions=[
                        PUSH(value=10),
                        STORE_GLOBAL(name="x"),
                        LOAD_GLOBAL(name="x"),
                        PUSH(value=1),
                        ADD(),
                        STORE_GLOBAL(name="x"),
                        PUSH(value=1035),
                        LOAD_GLOBAL(name="x"),
                        ADD(),
                        PRINT(),
                        PUSH(value=0),
                        RETURN(),
                    ],
                ),
            ]
        ),
        formatprogram=False,
    )

    prog = Program(
        [
            GlobalVar(name=Name(str="x")),
            Function(
                name=Name(str="main"),
                params=[],
                statements=[
                    STATEMENT(instructions=[PUSH(value=10), STORE_GLOBAL(name="x")]),
                    STATEMENT(instructions=[LOAD_GLOBAL(name="x"), PUSH(value=1), ADD(), STORE_GLOBAL(name="x")]),
                    STATEMENT(instructions=[PUSH(value=1035), LOAD_GLOBAL(name="x"), ADD(), PRINT()]),
                    STATEMENT(instructions=[PUSH(value=0), RETURN()]),
                ],
            ),
        ]
    )
    #    print_colorheader("--- Raw program data structure:", prog)
    #    print_colorheader("--- Formatted:", format_program(prog))
    p2 = blocks_program(prog)
    #    print_colorheader("--- After BLOCKing::", p2)
    #    print_colorheader("--- Formatted:", format_program(p2))

    assert_equal_verbose(
        p2,
        Program(
            statements=[
                GlobalVar(name=Name(str="x")),
                Function(
                    name=Name(str="main"),
                    params=[],
                    statements=[
                        BLOCK(
                            label="L1",
                            instructions=[
                                PUSH(10),
                                STORE_GLOBAL("x"),
                                LOAD_GLOBAL("x"),
                                PUSH(1),
                                ADD(),
                                STORE_GLOBAL("x"),
                                PUSH(1035),
                                LOAD_GLOBAL("x"),
                                ADD(),
                                PRINT(),
                                PUSH(0),
                                RETURN(),
                            ],
                        )
                    ],
                ),
            ]
        ),
        formatprogram=False,
    )

    prog = Program(
        statements=[
            Function(
                name=Name(str="fact"),
                params=[Name(str="n")],
                statements=[
                    IfElse(
                        condition=EXPR(instructions=[LOAD_LOCAL(name="n"), PUSH(value=2), LT()]),
                        iflist=[STATEMENT(instructions=[PUSH(value=1), RETURN()])],
                        elselist=[
                            STATEMENT(instructions=[LOCAL(name="x")]),
                            STATEMENT(instructions=[PUSH(value=1), STORE_LOCAL(name="x")]),
                            STATEMENT(instructions=[LOCAL(name="result")]),
                            STATEMENT(instructions=[PUSH(value=1), STORE_LOCAL(name="result")]),
                            While(
                                condition=EXPR(instructions=[LOAD_LOCAL(name="x"), LOAD_LOCAL(name="n"), LT()]),
                                statements=[
                                    STATEMENT(
                                        instructions=[
                                            LOAD_LOCAL(name="result"),
                                            LOAD_LOCAL(name="x"),
                                            MUL(),
                                            STORE_LOCAL(name="result"),
                                        ]
                                    ),
                                    STATEMENT(
                                        instructions=[
                                            LOAD_LOCAL(name="x"),
                                            PUSH(value=1),
                                            ADD(),
                                            STORE_LOCAL(name="x"),
                                        ]
                                    ),
                                ],
                            ),
                            STATEMENT(instructions=[LOAD_LOCAL(name="result"), LOAD_LOCAL(name="n"), MUL(), RETURN()]),
                        ],
                    ),
                    STATEMENT(instructions=[PUSH(value=0), RETURN()]),
                ],
            ),
            GlobalVar(name=Name(str="x")),
            Function(
                name=Name(str="main"),
                params=[],
                statements=[
                    STATEMENT(instructions=[PUSH(value=1), STORE_GLOBAL(name="x")]),
                    While(
                        condition=EXPR(instructions=[LOAD_GLOBAL(name="x"), PUSH(value=10), LT()]),
                        statements=[
                            STATEMENT(instructions=[LOAD_GLOBAL(name="x"), CALL(name="fact", n=1), PRINT()]),
                            STATEMENT(
                                instructions=[LOAD_GLOBAL(name="x"), PUSH(value=1), ADD(), STORE_GLOBAL(name="x")]
                            ),
                        ],
                    ),
                    STATEMENT(instructions=[PUSH(value=0), RETURN()]),
                ],
            ),
        ]
    )
    #    print_colorheader("--- Raw program data structure:", prog)
    #    print_colorheader("--- Formatted:", format_program(prog))
    p2 = blocks_program(prog)
    #    print_colorheader("--- After BLOCKing::", p2)
    #    print_colorheader("--- Formatted:", format_program(p2))

    assert_equal_verbose(
        p2,
        Program(
            statements=[
                Function(
                    name=Name(str="fact"),
                    params=[Name(str="n")],
                    statements=[
                        IfElse(
                            condition=EXPR(instructions=[LOAD_LOCAL("n"), PUSH(2), LT()]),
                            iflist=[BLOCK(label="L1", instructions=[PUSH(1), RETURN()])],
                            elselist=[
                                BLOCK(
                                    label="L2",
                                    instructions=[
                                        LOCAL("x"),
                                        PUSH(1),
                                        STORE_LOCAL("x"),
                                        LOCAL("result"),
                                        PUSH(1),
                                        STORE_LOCAL("result"),
                                    ],
                                ),
                                While(
                                    condition=EXPR(instructions=[LOAD_LOCAL("x"), LOAD_LOCAL("n"), LT()]),
                                    statements=[
                                        BLOCK(
                                            label="L3",
                                            instructions=[
                                                LOAD_LOCAL("result"),
                                                LOAD_LOCAL("x"),
                                                MUL(),
                                                STORE_LOCAL("result"),
                                                LOAD_LOCAL("x"),
                                                PUSH(1),
                                                ADD(),
                                                STORE_LOCAL("x"),
                                            ],
                                        )
                                    ],
                                ),
                                BLOCK(
                                    label="L4", instructions=[LOAD_LOCAL("result"), LOAD_LOCAL("n"), MUL(), RETURN()]
                                ),
                            ],
                        ),
                        BLOCK(label="L5", instructions=[PUSH(0), RETURN()]),
                    ],
                ),
                GlobalVar(name=Name(str="x")),
                Function(
                    name=Name(str="main"),
                    params=[],
                    statements=[
                        BLOCK(label="L6", instructions=[PUSH(1), STORE_GLOBAL("x")]),
                        While(
                            condition=EXPR(instructions=[LOAD_GLOBAL("x"), PUSH(10), LT()]),
                            statements=[
                                BLOCK(
                                    label="L7",
                                    instructions=[
                                        LOAD_GLOBAL("x"),
                                        CALL("fact", 1),
                                        PRINT(),
                                        LOAD_GLOBAL("x"),
                                        PUSH(1),
                                        ADD(),
                                        STORE_GLOBAL("x"),
                                    ],
                                )
                            ],
                        ),
                        BLOCK(label="L8", instructions=[PUSH(0), RETURN()]),
                    ],
                ),
            ]
        ),
        formatprogram=False,
    )

    printcolor("unit tests PASSED", ansicode.green)
