declare i32 @_print_int(i32)

define i32 @abs(i32 %.arg_x) {
entry:
    %x = alloca i32
    store i32 %.arg_x, i32* %x
    br label %L4
L4:
    %.r0 = load i32, i32* %x
    %.r1 = icmp slt i32 %.r0, 0
    br i1 %.r1, label %L1, label %L2
L1:
    %.r2 = load i32, i32* %x
    %.r3 = sub i32 0, %.r2
    ret i32 %.r3
    br label %L2
L2:
    %.r4 = load i32, i32* %x
    ret i32 %.r4
}

define i32 @main() {
entry:
    br label %L3
L3:
    %.r5 = call i32 (i32) @abs(i32 2)
    call i32 (i32) @_print_int(i32 %.r5)
    %.r6 = call i32 (i32) @abs(i32 -2)
    call i32 (i32) @_print_int(i32 %.r6)
    ret i32 0
}
