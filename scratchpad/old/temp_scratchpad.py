# scratchpad just to paste in program output and use VScode autoformatting to compare data structures visually

from model import *


Program(
    statements=[
        BLOCK(label="L1", instructions=[PUSH(3), STORE_GLOBAL("x")]),
        IfElse(
            condition=EXPR(instructions=[LOAD_GLOBAL("x"), PUSH(4), LT()]),
            iflist=[BLOCK(label="L2", instructions=[LOAD_GLOBAL("x"), STORE_GLOBAL("min")])],
            elselist=[BLOCK(label="L3", instructions=[LOAD_GLOBAL("y"), STORE_GLOBAL("min")])],
        ),
        BLOCK(label="L4", instructions=[LOAD_GLOBAL("min"), PRINT(), PUSH(0), RETURN()]),
    ]
)

Program(
    statements=[
        BLOCK(label="L4", instructions=[LOAD_GLOBAL("min"), PRINT(), PUSH(0), RETURN(), GOTO(label="L100")]),
        BLOCK(label="L99", instructions=[LOAD_GLOBAL("x"), PUSH(4), LT(), CBRANCH(iftrue="L2", iffalse="L3")]),
        BLOCK(label="L2", instructions=[LOAD_GLOBAL("x"), STORE_GLOBAL("min"), GOTO(label="L100")]),
        BLOCK(label="L3", instructions=[LOAD_GLOBAL("y"), STORE_GLOBAL("min"), GOTO(label="L100")]),
        BLOCK(label="L1", instructions=[PUSH(3), STORE_GLOBAL("x"), GOTO(label="L100")]),
    ]
)


Program(
    statements=[
        Function(
            name=Name(str="pow"),
            params=[Name(str="x"), Name(str="n")],
            statements=[
                DeclareValue(left=Name(str="out"), right=Integer(n=1)),
                DeclareValue(left=Name(str="i"), right=Integer(n=0)),
                While(
                    condition=Relation(op=RelationOp(name="<"), left=Name(str="i"), right=Name(str="n")),
                    statements=[
                        Assign(left=Name(str="out"), right=Multiply(left=Name(str="out"), right=Name(str="x"))),
                        Assign(left=Name(str="i"), right=Add(left=Name(str="i"), right=Integer(n=1))),
                    ],
                ),
                Return(value=Name(str="out")),
            ],
        ),
        DeclareValue(
            left=Name(str="x"),
            right=CallFn(name=Name(str="pow"), params=[Integer(n=3), Add(left=Integer(n=2), right=Integer(n=2))]),
        ),
        Print(value=Name(str="x")),
    ]
)
