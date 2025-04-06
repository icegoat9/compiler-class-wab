declare i32 @_print_int(i32)
@i = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 1, i32* @i
    br label %L8
L8:
    %.r1 = load i32, i32* @i
    %.r2 = icmp slt i32 %.r1, 10
    br i1 %.r2, label %L9, label %L7
L9:
    %.r3 = load i32, i32* @i
    %.r4 = icmp sle i32 %.r3, 3
    br i1 %.r4, label %L2, label %L10
L2:
    %.r5 = load i32, i32* @i
    call i32 (i32) @_print_int(i32 %.r5)
    br label %L6
L10:
    %.r6 = load i32, i32* @i
    %.r7 = icmp sle i32 %.r6, 6
    br i1 %.r7, label %L3, label %L5
L3:
    %j = alloca i32
    store i32 1, i32* %j
    br label %L11
L11:
    %.r8 = load i32, i32* %j
    %.r9 = icmp slt i32 %.r8, 4
    br i1 %.r9, label %L4, label %L6
L4:
    %.r10 = load i32, i32* @i
    %.r11 = mul i32 10, %.r10
    %.r12 = load i32, i32* %j
    %.r13 = add i32 %.r11, %.r12
    call i32 (i32) @_print_int(i32 %.r13)
    %.r14 = load i32, i32* %j
    %.r15 = add i32 %.r14, 1
    store i32 %.r15, i32* %j
    br label %L11
L5:
    %.r16 = load i32, i32* @i
    %.r17 = mul i32 100, %.r16
    call i32 (i32) @_print_int(i32 %.r17)
    br label %L6
L6:
    %.r18 = load i32, i32* @i
    %.r19 = add i32 %.r18, 1
    store i32 %.r19, i32* @i
    br label %L8
L7:
    ret i32 0
}
