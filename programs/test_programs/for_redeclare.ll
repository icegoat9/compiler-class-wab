declare i32 @_print_int(i32)
@i = global i32 0
@i = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 5, i32* @i
    %.r1 = load i32, i32* @i
    call i32 (i32) @_print_int(i32 %.r1)
    store i32 1, i32* @i
    br label %L4
L4:
    %.r2 = load i32, i32* @i
    %.r3 = icmp sle i32 %.r2, 10
    br i1 %.r3, label %L2, label %L3
L2:
    %.r4 = load i32, i32* @i
    call i32 (i32) @_print_int(i32 %.r4)
    %.r5 = load i32, i32* @i
    %.r6 = add i32 %.r5, 1
    store i32 %.r6, i32* @i
    br label %L4
L3:
    %.r7 = load i32, i32* @i
    call i32 (i32) @_print_int(i32 %.r7)
    ret i32 0
}
