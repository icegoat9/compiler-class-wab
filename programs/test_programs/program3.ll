declare i32 @_print_int(i32)
@result = global i32 0
@x = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 1, i32* @result
    store i32 1, i32* @x
    br label %L4
L4:
    %.r0 = load i32, i32* @x
    %.r1 = icmp slt i32 %.r0, 10
    br i1 %.r1, label %L2, label %L3
L2:
    %.r2 = load i32, i32* @result
    %.r3 = load i32, i32* @x
    %.r4 = mul i32 %.r2, %.r3
    store i32 %.r4, i32* @result
    %.r5 = load i32, i32* @x
    %.r6 = add i32 %.r5, 1
    store i32 %.r6, i32* @x
    br label %L4
L3:
    %.r7 = load i32, i32* @result
    call i32 (i32) @_print_int(i32 %.r7)
    ret i32 0
}
