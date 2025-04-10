declare i32 @_print_int(i32)

define i32 @printval(i32 %.arg_x) {
entry:
    %x = alloca i32
    store i32 %.arg_x, i32* %x
    br label %L1
L1:
    %.r1 = load i32, i32* %x
    call i32 (i32) @_print_int(i32 %.r1)
    %.r2 = load i32, i32* %x
    ret i32 %.r2
}
@y = global i32 0

define i32 @main() {
entry:
    br label %L2
L2:
    store i32 0, i32* @y
    %.r3 = call i32 (i32) @printval(i32 2)
    store i32 %.r3, i32* @y
    %.r4 = call i32 (i32) @printval(i32 5)
    %.r5 = load i32, i32* @y
    %.r6 = load i32, i32* @y
    %.r7 = add i32 10, %.r6
    %.r8 = call i32 (i32) @printval(i32 %.r7)
    ret i32 0
}
