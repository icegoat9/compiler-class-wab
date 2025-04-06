declare i32 @_print_int(i32)
@i = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 1, i32* @i
    br label %L6
L6:
    %.r1 = load i32, i32* @i
    %.r2 = icmp sle i32 %.r1, 3
    br i1 %.r2, label %L2, label %L5
L2:
    %j = alloca i32
    %.r3 = load i32, i32* @i
    %.r4 = sub i32 %.r3, 1
    store i32 %.r4, i32* %j
    br label %L7
L7:
    %.r5 = load i32, i32* %j
    %.r6 = icmp sle i32 %.r5, 3
    br i1 %.r6, label %L3, label %L4
L3:
    %.r7 = load i32, i32* @i
    %.r8 = mul i32 10, %.r7
    %.r9 = load i32, i32* %j
    %.r10 = add i32 %.r8, %.r9
    call i32 (i32) @_print_int(i32 %.r10)
    %.r11 = load i32, i32* %j
    %.r12 = add i32 %.r11, 1
    store i32 %.r12, i32* %j
    br label %L7
L4:
    %.r13 = load i32, i32* @i
    %.r14 = add i32 %.r13, 1
    store i32 %.r14, i32* @i
    br label %L6
L5:
    ret i32 0
}
