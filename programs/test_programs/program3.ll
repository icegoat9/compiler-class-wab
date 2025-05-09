declare i32 @_print_int(i32)
declare i32 @printf(ptr noundef, ...)
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
    %.r1 = load i32, i32* @x
    %.r2 = icmp slt i32 %.r1, 10
    br i1 %.r2, label %L2, label %L3
L2:
    %.r3 = load i32, i32* @result
    %.r4 = load i32, i32* @x
    %.r5 = mul i32 %.r3, %.r4
    store i32 %.r5, i32* @result
    %.r6 = load i32, i32* @x
    %.r7 = add i32 %.r6, 1
    store i32 %.r7, i32* @x
    br label %L4
L3:
    %.r8 = load i32, i32* @result
    call i32 (i32) @_print_int(i32 %.r8)
    ret i32 0
}
