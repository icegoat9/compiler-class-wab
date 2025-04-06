declare i32 @_print_int(i32)

define i32 @fact(i32 %.arg_n) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L1
L1:
    %result = alloca i32
    store i32 1, i32* %result
    %x = alloca i32
    store i32 1, i32* %x
    br label %L7
L7:
    %.r1 = load i32, i32* %x
    %.r2 = load i32, i32* %n
    %.r3 = icmp sle i32 %.r1, %.r2
    br i1 %.r3, label %L2, label %L3
L2:
    %.r4 = load i32, i32* %result
    %.r5 = load i32, i32* %x
    %.r6 = mul i32 %.r4, %.r5
    store i32 %.r6, i32* %result
    %.r7 = load i32, i32* %x
    %.r8 = add i32 %.r7, 1
    store i32 %.r8, i32* %x
    br label %L7
L3:
    %.r9 = load i32, i32* %result
    ret i32 %.r9
}
@x = global i32 0

define i32 @main() {
entry:
    br label %L4
L4:
    store i32 1, i32* @x
    br label %L8
L8:
    %.r10 = load i32, i32* @x
    %.r11 = icmp slt i32 %.r10, 10
    br i1 %.r11, label %L5, label %L6
L5:
    %.r12 = load i32, i32* @x
    %.r13 = call i32 (i32) @fact(i32 %.r12)
    call i32 (i32) @_print_int(i32 %.r13)
    %.r14 = load i32, i32* @x
    %.r15 = add i32 %.r14, 1
    store i32 %.r15, i32* @x
    br label %L8
L6:
    ret i32 0
}
