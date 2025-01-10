declare i32 @_print_int(i32)

define i32 @concat(i32 %.arg_a, i32 %.arg_b) {
entry:
    %a = alloca i32
    store i32 %.arg_a, i32* %a
    %b = alloca i32
    store i32 %.arg_b, i32* %b
    br label %L1
L1:
    %out = alloca i32
    store i32 0, i32* %out
    %scale = alloca i32
    store i32 1, i32* %scale
    %.r0 = load i32, i32* %out
    %.r1 = load i32, i32* %b
    %.r2 = add i32 %.r0, %.r1
    store i32 %.r2, i32* %out
    br label %L9
L9:
    %.r3 = load i32, i32* %out
    %.r4 = icmp slt i32 999, %.r3
    br i1 %.r4, label %L2, label %L10
L2:
    store i32 10000, i32* %scale
    br label %L6
L10:
    %.r5 = load i32, i32* %out
    %.r6 = icmp slt i32 99, %.r5
    br i1 %.r6, label %L3, label %L11
L3:
    store i32 1000, i32* %scale
    br label %L6
L11:
    %.r7 = load i32, i32* %out
    %.r8 = icmp slt i32 9, %.r7
    br i1 %.r8, label %L4, label %L5
L4:
    store i32 100, i32* %scale
    br label %L6
L5:
    store i32 10, i32* %scale
    br label %L6
L6:
    %.r9 = load i32, i32* %out
    %.r10 = load i32, i32* %scale
    %.r11 = load i32, i32* %a
    %.r12 = mul i32 %.r10, %.r11
    %.r13 = add i32 %.r9, %.r12
    store i32 %.r13, i32* %out
    %.r14 = load i32, i32* %out
    ret i32 %.r14
}

define i32 @merge(i32 %.arg_a, i32 %.arg_b, i32 %.arg_c) {
entry:
    %a = alloca i32
    store i32 %.arg_a, i32* %a
    %b = alloca i32
    store i32 %.arg_b, i32* %b
    %c = alloca i32
    store i32 %.arg_c, i32* %c
    br label %L7
L7:
    %.r15 = load i32, i32* %a
    %.r16 = load i32, i32* %b
    %.r17 = add i32 %.r15, %.r16
    %.r18 = load i32, i32* %b
    %.r19 = load i32, i32* %c
    %.r20 = add i32 %.r18, %.r19
    %.r21 = call i32 (i32, i32) @concat(i32 %.r17, i32 %.r20)
    ret i32 %.r21
}
@a = global i32 0
@b = global i32 0

define i32 @main() {
entry:
    br label %L8
L8:
    store i32 12, i32* @a
    store i32 345, i32* @b
    %.r22 = load i32, i32* @a
    %.r23 = load i32, i32* @b
    %.r24 = call i32 (i32, i32) @concat(i32 %.r22, i32 %.r23)
    call i32 (i32) @_print_int(i32 %.r24)
    %.r25 = call i32 (i32, i32, i32) @merge(i32 4, i32 8, i32 6)
    call i32 (i32) @_print_int(i32 %.r25)
    ret i32 0
}
