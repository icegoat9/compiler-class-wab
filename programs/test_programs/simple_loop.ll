declare i32 @_print_int(i32)
@x = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 1, i32* @x
    br label %L4
L4:
    %.r1 = load i32, i32* @x
    %.r2 = icmp sle i32 %.r1, 10
    br i1 %.r2, label %L2, label %L3
L2:
    %.r3 = load i32, i32* @x
    call i32 (i32) @_print_int(i32 %.r3)
    %.r4 = load i32, i32* @x
    %.r5 = add i32 %.r4, 1
    store i32 %.r5, i32* @x
    br label %L4
L3:
    ret i32 0
}
