declare i32 @_print_int(i32)
@x = global i32 0

define i32 @setx(i32 %.arg_v) {
entry:
    %v = alloca i32
    store i32 %.arg_v, i32* %v
    br label %L1
L1:
    %.r1 = load i32, i32* %v
    store i32 %.r1, i32* @x
    %.r2 = load i32, i32* @x
    ret i32 %.r2
}

define i32 @main() {
entry:
    br label %L2
L2:
    %.r3 = load i32, i32* @x
    call i32 (i32) @_print_int(i32 %.r3)
    %.r4 = call i32 (i32) @setx(i32 123)
    call i32 (i32) @_print_int(i32 %.r4)
    %.r5 = load i32, i32* @x
    call i32 (i32) @_print_int(i32 %.r5)
    ret i32 0
}
