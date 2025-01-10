declare i32 @_print_int(i32)
@x = global i32 0
@y = global i32 0
@min = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 3, i32* @x
    store i32 4, i32* @y
    store i32 0, i32* @min
    br label %L5
L5:
    %.r1 = load i32, i32* @x
    %.r2 = load i32, i32* @y
    %.r3 = icmp slt i32 %.r1, %.r2
    br i1 %.r3, label %L2, label %L3
L2:
    %.r4 = load i32, i32* @x
    store i32 %.r4, i32* @min
    br label %L4
L3:
    %.r5 = load i32, i32* @y
    store i32 %.r5, i32* @min
    br label %L4
L4:
    %.r6 = load i32, i32* @min
    call i32 (i32) @_print_int(i32 %.r6)
    ret i32 0
}
