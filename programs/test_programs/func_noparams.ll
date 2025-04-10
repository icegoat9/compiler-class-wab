declare i32 @_print_int(i32)

define i32 @print5() {
entry:
    br label %L1
L1:
    call i32 (i32) @_print_int(i32 5)
    ret i32 555
}
@x = global i32 0

define i32 @main() {
entry:
    br label %L2
L2:
    %.r1 = call i32 () @print5()
    store i32 %.r1, i32* @x
    %.r2 = load i32, i32* @x
    call i32 (i32) @_print_int(i32 %.r2)
    ret i32 0
}
