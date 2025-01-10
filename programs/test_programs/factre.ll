declare i32 @_print_int(i32)

define i32 @factre(i32 %.arg_x, i32 %.arg_n) {
entry:
    %x = alloca i32
    store i32 %.arg_x, i32* %x
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L10
L10:
    %.r1 = load i32, i32* %x
    %.r2 = load i32, i32* %n
    %.r3 = icmp eq i32 %.r1, %.r2
    br i1 %.r3, label %L1, label %L2
L1:
    %.r4 = load i32, i32* %n
    ret i32 %.r4
    br label %L3
L2:
    %.r5 = load i32, i32* %x
    %.r6 = load i32, i32* %x
    %.r7 = add i32 %.r6, 1
    %.r8 = load i32, i32* %n
    %.r9 = call i32 (i32, i32) @factre(i32 %.r7, i32 %.r8)
    %.r10 = mul i32 %.r5, %.r9
    ret i32 %.r10
    br label %L3
L3:
    ret i32 0
}

define i32 @fact(i32 %.arg_n) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L11
L11:
    %.r11 = load i32, i32* %n
    %.r12 = icmp slt i32 0, %.r11
    br i1 %.r12, label %L4, label %L5
L4:
    %.r13 = load i32, i32* %n
    %.r14 = call i32 (i32, i32) @factre(i32 1, i32 %.r13)
    ret i32 %.r14
    br label %L6
L5:
    ret i32 1
    br label %L6
L6:
    ret i32 0
}
@x = global i32 0

define i32 @main() {
entry:
    br label %L7
L7:
    store i32 1, i32* @x
    br label %L12
L12:
    %.r15 = load i32, i32* @x
    %.r16 = icmp slt i32 %.r15, 10
    br i1 %.r16, label %L8, label %L9
L8:
    %.r17 = load i32, i32* @x
    %.r18 = call i32 (i32) @fact(i32 %.r17)
    call i32 (i32) @_print_int(i32 %.r18)
    %.r19 = load i32, i32* @x
    %.r20 = add i32 %.r19, 1
    store i32 %.r20, i32* @x
    br label %L12
L9:
    ret i32 0
}
