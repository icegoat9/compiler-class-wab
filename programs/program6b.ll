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
    store i32 10, i32* %scale
    br label %L9
L9:
    %.r0 = load i32, i32* %scale
    %.r1 = load i32, i32* %b
    %.r2 = add i32 %.r1, 1
    %.r3 = icmp slt i32 %.r0, %.r2
    br i1 %.r3, label %L2, label %L3
L2:
    %.r4 = load i32, i32* %scale
    %.r5 = mul i32 %.r4, 10
    store i32 %.r5, i32* %scale
    br label %L9
L3:
    %.r6 = load i32, i32* %out
    %.r7 = load i32, i32* %scale
    %.r8 = load i32, i32* %a
    %.r9 = mul i32 %.r7, %.r8
    %.r10 = add i32 %.r6, %.r9
    store i32 %.r10, i32* %out
    %.r11 = load i32, i32* %scale
    %.r12 = load i32, i32* %a
    %.r13 = mul i32 %.r11, %.r12
    %.r14 = load i32, i32* %b
    %.r15 = add i32 %.r13, %.r14
    ret i32 %.r15
}

define i32 @merge(i32 %.arg_a, i32 %.arg_b, i32 %.arg_c) {
entry:
    %a = alloca i32
    store i32 %.arg_a, i32* %a
    %b = alloca i32
    store i32 %.arg_b, i32* %b
    %c = alloca i32
    store i32 %.arg_c, i32* %c
    br label %L4
L4:
    %.r16 = load i32, i32* %a
    %.r17 = load i32, i32* %b
    %.r18 = add i32 %.r16, %.r17
    %.r19 = load i32, i32* %b
    %.r20 = load i32, i32* %c
    %.r21 = add i32 %.r19, %.r20
    %.r22 = call i32 (i32, i32) @concat(i32 %.r18, i32 %.r21)
    ret i32 %.r22
}

define i32 @lennum(i32 %.arg_num) {
entry:
    %num = alloca i32
    store i32 %.arg_num, i32* %num
    br label %L5
L5:
    %i = alloca i32
    store i32 1, i32* %i
    %scale = alloca i32
    store i32 10, i32* %scale
    br label %L10
L10:
    %.r23 = load i32, i32* %scale
    %.r24 = load i32, i32* %num
    %.r25 = add i32 %.r24, 1
    %.r26 = icmp slt i32 %.r23, %.r25
    br i1 %.r26, label %L6, label %L7
L6:
    %.r27 = load i32, i32* %scale
    %.r28 = mul i32 %.r27, 10
    store i32 %.r28, i32* %scale
    %.r29 = load i32, i32* %i
    %.r30 = add i32 %.r29, 1
    store i32 %.r30, i32* %i
    br label %L10
L7:
    %.r31 = load i32, i32* %i
    ret i32 %.r31
}
@a = global i32 0
@b = global i32 0

define i32 @main() {
entry:
    br label %L8
L8:
    store i32 12, i32* @a
    store i32 345, i32* @b
    %.r32 = load i32, i32* @a
    %.r33 = load i32, i32* @b
    %.r34 = call i32 (i32, i32) @concat(i32 %.r32, i32 %.r33)
    call i32 (i32) @_print_int(i32 %.r34)
    %.r35 = call i32 (i32, i32, i32) @merge(i32 4, i32 8, i32 6)
    call i32 (i32) @_print_int(i32 %.r35)
    ret i32 0
}
