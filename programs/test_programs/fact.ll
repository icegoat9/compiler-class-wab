declare i32 @_print_int(i32)

define i32 @fact(i32 %.arg_n) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L9
L9:
    %.r0 = load i32, i32* %n
    %.r1 = icmp slt i32 %.r0, 2
    br i1 %.r1, label %L1, label %L2
L1:
    ret i32 1
    br label %L5
L2:
    %x = alloca i32
    store i32 1, i32* %x
    %result = alloca i32
    store i32 1, i32* %result
    br label %L10
L10:
    %.r2 = load i32, i32* %x
    %.r3 = load i32, i32* %n
    %.r4 = icmp slt i32 %.r2, %.r3
    br i1 %.r4, label %L3, label %L4
L3:
    %.r5 = load i32, i32* %result
    %.r6 = load i32, i32* %x
    %.r7 = mul i32 %.r5, %.r6
    store i32 %.r7, i32* %result
    %.r8 = load i32, i32* %x
    %.r9 = add i32 %.r8, 1
    store i32 %.r9, i32* %x
    br label %L10
L4:
    %.r10 = load i32, i32* %result
    %.r11 = load i32, i32* %n
    %.r12 = mul i32 %.r10, %.r11
    ret i32 %.r12
    br label %L5
L5:
    ret i32 0
}
@x = global i32 0

define i32 @main() {
entry:
    br label %L6
L6:
    store i32 1, i32* @x
    br label %L11
L11:
    %.r13 = load i32, i32* @x
    %.r14 = icmp slt i32 %.r13, 10
    br i1 %.r14, label %L7, label %L8
L7:
    %.r15 = load i32, i32* @x
    %.r16 = call i32 (i32) @fact(i32 %.r15)
    call i32 (i32) @_print_int(i32 %.r16)
    %.r17 = load i32, i32* @x
    %.r18 = add i32 %.r17, 1
    store i32 %.r18, i32* @x
    br label %L11
L8:
    ret i32 0
}
