declare i32 @_print_int(i32)
@y = global i32 0
@i = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 10, i32* @y
    store i32 1, i32* @i
    br label %L4
L4:
    %.r1 = load i32, i32* @i
    %.r2 = icmp sle i32 %.r1, 10
    br i1 %.r2, label %L2, label %L3
L2:
    %.r3 = load i32, i32* @i
    %.r4 = load i32, i32* @y
    %.r5 = mul i32 %.r3, %.r4
    call i32 (i32) @_print_int(i32 %.r5)
    %.r6 = load i32, i32* @i
    %.r7 = add i32 %.r6, 1
    store i32 %.r7, i32* @i
    br label %L4
L3:
    %.r8 = load i32, i32* @i
    call i32 (i32) @_print_int(i32 %.r8)
    ret i32 0
}
