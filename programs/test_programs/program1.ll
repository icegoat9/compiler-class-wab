declare i32 @_print_int(i32)
declare i32 @printf(ptr noundef, ...)
@x = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 10, i32* @x
    %.r1 = load i32, i32* @x
    %.r2 = add i32 %.r1, 1
    store i32 %.r2, i32* @x
    %.r3 = load i32, i32* @x
    %.r4 = add i32 1035, %.r3
    call i32 (i32) @_print_int(i32 %.r4)
    ret i32 0
}
