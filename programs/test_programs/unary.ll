declare i32 @_print_int(i32)
@x = global i32 0
@y = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 2, i32* @x
    store i32 5, i32* @y
    call i32 (i32) @_print_int(i32 -2)
    %.r1 = load i32, i32* @x
    %.r2 = sub i32 0, %.r1
    call i32 (i32) @_print_int(i32 %.r2)
    %.r3 = load i32, i32* @x
    %.r4 = sub i32 0, %.r3
    %.r5 = load i32, i32* @y
    %.r6 = add i32 %.r4, %.r5
    call i32 (i32) @_print_int(i32 %.r6)
    %.r7 = load i32, i32* @x
    %.r8 = load i32, i32* @y
    %.r9 = add i32 %.r7, %.r8
    %.r10 = sub i32 0, %.r9
    call i32 (i32) @_print_int(i32 %.r10)
    call i32 (i32) @_print_int(i32 1)
    call i32 (i32) @_print_int(i32 1)
    call i32 (i32) @_print_int(i32 -9)
    call i32 (i32) @_print_int(i32 2)
    call i32 (i32) @_print_int(i32 -2)
    ret i32 0
}
