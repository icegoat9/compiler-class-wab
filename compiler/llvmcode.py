# llvmcode.py
"""Begin process of translating program from the generic stack machine representation to
an LLVM-specific representation, by substituting specific LLVM(statements for their stack machine
equivalents.

This is still wrapping these LLVM(statements in an LLVM() Instruction instance rather than representing
them as raw strings, to save the "program object -> string" conversion for the last compiler step,
as that includes some non-functional formatting choices (indentation, etc) which also make it harder
to debug and test intermediate steps.
"""
#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests
# [ ] more complex assertion unit test involving function call with multi parameters as that's a bit subtle
# TODO:
# [ ] Dig into the .reverse() I do below on function params-- is the error here or earlier?
# [ ] Add or add link to documentation of full set of LLVM(instructions as reference, rather
#     than comment at bottom of file.

from model import *
from format import *
from printcolor import *

_register_n = 0
"""Index for globally unique LLVM(register. Incremented before value is returned, so
initializing to 0 means the first register will be 'register 1' and so on."""


def set_register_index(n) -> None:
    """Directly set the global register index to a specific value. This is likely only useful for
    debugging and deterministic testing, where we want to test some subset of this module."""
    global _register_n
    _register_n = n


def next_register() -> str:
    """Return a globally unique register name, which is incremented each time this is called,
    for LLVM's requirement on unique register use in each line."""
    global _register_n
    _register_n += 1
    return f"%.r{_register_n}"


def llvm_program(program: Program) -> Program:
    """Convert program from pseudo stack code to partial LLVM(statement code."""
    return Program(statements_to_llvm(program.statements))


def statements_to_llvm(statements: list[Statement]) -> list[Statement]:
    """Make LLVM() substitution on a list of statements, whether the top-level program or the body
    of a function.

    Note that we no longer need to be recursively descending into IfElse and While structure bodies,
    as in a previous compiler step those were transformed to generic BLOCK-and-label structures and
    GOTO / JUMP / BRANCH type flow control-- the only structures containing statements now are the
    top-level program, Functions, and BLOCKs."""
    output = []
    # print(statements)
    for s in statements:
        # printcolor("debug: s = %s" % s, ansicode.yellow)
        match s:
            case GlobalVar() | StrConstNum():
                # handled in a later LLVM pass
                output.append(s)
            case Function(name, params, body):
                output.append(Function(name, params, statements_to_llvm(body)))
            case BLOCK():
                # llvm = create_llvm(s)
                # print(llvm)
                output.append(create_llvm(s))
            case _:
                raise SyntaxError(f"Unhandled statement type {s}")
    # printcolor("output-in-progress:%s %s" % (ansicode.reset, output))
    return output


def create_llvm(block: BLOCK) -> BLOCK:
    """Perform the instruction -> LLVM(instruction translation on statements in a single BLOCK.
    This workhorse function does the logical work of transforming stack-based management of parameters
    to LLVM(register-based management and is where handling of future new compiler instructions would live.
    """
    ops = []
    stack = []
    for instr in block.instructions:
        # print("*debug: %s" % instr)
        # printcolor("oplist[]: %s %s" % (ansicode.reset, ops))
        # printcolor("stack: %s %s" % (ansicode.reset, stack))
        match instr:
            case PUSH():
                stack.append(str(instr.value))
            ## math ops
            case ADD():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                ops.append(LLVM(f"{result} = add i32 {left}, {right}"))
                stack.append(result)
            case MUL():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                ops.append(LLVM(f"{result} = mul i32 {left}, {right}"))
                stack.append(result)
            case SUB():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                ops.append(LLVM(f"{result} = sub i32 {left}, {right}"))
                stack.append(result)
            case DIV():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                ops.append(LLVM(f"{result} = sdiv i32 {left}, {right}"))
                stack.append(result)
            case MOD():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                # TODO: fix this to compute modulo 
                #       (this instruction is remainder: only the same as modulo if arguments have the same sign)
                ops.append(LLVM(f"{result} = srem i32 {left}, {right}"))
                stack.append(result)
            ## Comparison ops
            case EQ():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                ops.append(LLVM(f"{result} = icmp eq i32 {left}, {right}"))
                stack.append(result)
            case LT():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                ops.append(LLVM(f"{result} = icmp slt i32 {left}, {right}"))
                stack.append(result)
            case LTE():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                ops.append(LLVM(f"{result} = icmp sle i32 {left}, {right}"))
                stack.append(result)
            case GT():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                ops.append(LLVM(f"{result} = icmp sgt i32 {left}, {right}"))
                stack.append(result)
            case GTE():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                ops.append(LLVM(f"{result} = icmp sge i32 {left}, {right}"))
                stack.append(result)
            case NEQ():
                right = stack.pop()
                left = stack.pop()
                result = next_register()
                ops.append(LLVM(f"{result} = icmp ne i32 {left}, {right}"))
                stack.append(result)
            ## mem ops
            case LOCAL(name):
                ops.append(LLVM(f"%{name} = alloca i32"))
            case LOAD_LOCAL():
                result = next_register()
                ops.append(LLVM(f"{result} = load i32, i32* %{instr.name}"))
                stack.append(result)
            case STORE_LOCAL(name):
                val = stack.pop()
                ops.append(LLVM(f"store i32 {val}, i32* %{name}"))
            case LOAD_GLOBAL():
                result = next_register()
                ops.append(LLVM(f"{result} = load i32, i32* @{instr.name}"))
                stack.append(result)
            case STORE_GLOBAL(name):
                val = stack.pop()
                ops.append(LLVM(f"store i32 {val}, i32* @{name}"))
            ## flow ops
            case GOTO(name):
                ops.append(LLVM(f"br label %{name}"))
            case CBRANCH(ifname, elsename):
                test = stack.pop()
                ops.append(LLVM(f"br i1 {test}, label %{ifname}, label %{elsename}"))
            case CALL(name, numparam):
                result = next_register()
                # load call parameters from the stack
                params = []
                ptypes = []
                for i in range(numparam):
                    params.append(f"i32 {stack.pop()}")
                    ptypes.append("i32")
                # TODO (HACK): fix this-- I saw params in wrong order in LLVM(output code so reversed
                #              these and that fixed the problem, but need to dig deeper and see if it's
                #              an error in an earlier stage
                params.reverse()
                ptypes.reverse()
                paramstr = ", ".join(params)
                ptypestr = ", ".join(ptypes)
                ops.append(LLVM(f"{result} = call i32 ({ptypestr}) @{name}({paramstr})"))
                stack.append(result)
            case RETURN():
                val = stack.pop()
                ops.append(LLVM(f"ret i32 {val}"))
            ## printing
            case PRINT():
                val = stack.pop()
                ops.append(LLVM(f"call i32 (i32) @_print_int(i32 {val})"))
            case PRINT_STR_CONST(n):
                ops.append(LLVM(f"call i32 (ptr, ...) @printf(ptr noundef @.str.{n})"))
            # case INPUT():
            #     result = next_register()
            #     ops.append(LLVM(f"{result} = call i32 (i32) @_scan_int()"))
            #     stack.append(result)
            case _:
                raise TypeError(f"No LLVM(translation available for instruction {instr}")
    return BLOCK(block.label, ops)

######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":

    # 1+2;
    x = BLOCK(label="L1", instructions=[PUSH(1), PUSH(2), ADD()])
    llvm = create_llvm(x)
    # print("-- Input:\n%s" % fmt_statement(x))
    # print("-- Output:\n%s" % fmt_statement(llvm))

    assert llvm == BLOCK("L1", [LLVM("%.r1 = add i32 1, 2")])

    prog1block = BLOCK(
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

    #    print("-- Input:\n%s" % fmt_statement(prog1block))
    llvm = create_llvm(prog1block)
    #    print("-- Output:\n%s" % fmt_statement(llvm))
    #    print("-- Output:\n%s" % llvm)

    assert llvm == BLOCK(
        label="L1",
        instructions=[
            LLVM("store i32 10, i32* @x"),
            LLVM("%.r2 = load i32, i32* @x"),
            LLVM("%.r3 = add i32 %.r2, 1"),
            LLVM("store i32 %.r3, i32* @x"),
            LLVM("%.r4 = load i32, i32* @x"),
            LLVM("%.r5 = add i32 1035, %.r4"),
            LLVM("call i32 (i32) @_print_int(i32 %.r5)"),
            LLVM("ret i32 0"),
        ],
    )

    prog1 = Program(
        [
            GlobalVar(Name(DUMMYTYPE, "x")),
            Function(
                Name(DUMMYTYPE, "main"),
                [],
                [
                    BLOCK(
                        ("L1"),
                        [
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
    )

    #    print(prog1)
    llvm = llvm_program(prog1)
    #    print(llvm)

    assert llvm == Program(
        [
            GlobalVar(Name(DUMMYTYPE, "x")),
            Function(
                Name(DUMMYTYPE, "main"),
                [],
                [
                    BLOCK(
                        "L1",
                        [
                            LLVM("store i32 10, i32* @x"),
                            LLVM("%.r6 = load i32, i32* @x"),
                            LLVM("%.r7 = add i32 %.r6, 1"),
                            LLVM("store i32 %.r7, i32* @x"),
                            LLVM("%.r8 = load i32, i32* @x"),
                            LLVM("%.r9 = add i32 1035, %.r8"),
                            LLVM("call i32 (i32) @_print_int(i32 %.r9)"),
                            LLVM("ret i32 0"),
                        ],
                    )
                ],
            ),
        ]
    )

    printcolor("tests PASSED", ansicode.green)


# LLVM(reference
# ; Math operations

# {result} = add i32 {left}, {right}         ; result = left + right
# {result} = mul i32 {left}, {right}         ; result = left * right
# {result} = icmp eq i32 {left}, {right}     ; result = left == right
# {result} = icmp slt i32 {left}, {right}    ; result = left < right

# ; Memory operations
# %{name} = alloca i32                       ; local name;
# {result} = load i32, i32* %{name}          ; result = local[name]
# store i32 {value}, i32* %{name}            ; local[name] = value
# {result} = load i32, i32* @{name}          ; result = global[name]
# store i32 {value}, i32* @{name}            ; global[name] = value

# ; Control flow operations
# br label %{name}                           ; GOTO(name)
# br i1 {test}, label %{Lc}, label %{La}     ; CBRANCH(Lc, La)
# {result} = call i32 (i32) @name(i32 {arg}) ; result = name(arg)
# ret i32 {value}                            ; return value

# ; Printing
# call i32 (i32) @_print_int(i32 {value})    ; print value
