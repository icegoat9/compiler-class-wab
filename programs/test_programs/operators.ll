declare i32 @_print_int(i32)
@x = global i32 0
@y = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 2, i32* @x
    store i32 5, i32* @y
    %.r0 = load i32, i32* @x
    %.r1 = load i32, i32* @y
    %.r2 = add i32 %.r0, %.r1
    call i32 (i32) @_print_int(i32 %.r2)
    %.r3 = load i32, i32* @x
    %.r4 = load i32, i32* @y
    %.r5 = sub i32 %.r3, %.r4
    call i32 (i32) @_print_int(i32 %.r5)
    %.r6 = load i32, i32* @x
    %.r7 = load i32, i32* @y
    %.r8 = mul i32 %.r6, %.r7
    call i32 (i32) @_print_int(i32 %.r8)
    %.r9 = load i32, i32* @x
    %.r10 = load i32, i32* @y
    %.r11 = sdiv i32 %.r9, %.r10
    call i32 (i32) @_print_int(i32 %.r11)
    %.r12 = load i32, i32* @y
    %.r13 = load i32, i32* @x
    %.r14 = sdiv i32 %.r12, %.r13
    call i32 (i32) @_print_int(i32 %.r14)
    ret i32 0
}
