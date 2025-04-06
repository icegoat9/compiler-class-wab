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
    store i32 0, i32* %j
    br label %L7
L7:
    %.r3 = load i32, i32* %j
    %.r4 = icmp slt i32 %.r3, 5
    br i1 %.r4, label %L3, label %L4
L3:
    %.r5 = load i32, i32* @i
    %.r6 = mul i32 10, %.r5
    %.r7 = load i32, i32* %j
    %.r8 = add i32 %.r6, %.r7
    call i32 (i32) @_print_int(i32 %.r8)
    %.r9 = load i32, i32* %j
    %.r10 = add i32 %.r9, 1
    store i32 %.r10, i32* %j
    br label %L7
L4:
    %.r11 = load i32, i32* @i
    %.r12 = add i32 %.r11, 1
    store i32 %.r12, i32* @i
    br label %L6
L5:
    ret i32 0
}
