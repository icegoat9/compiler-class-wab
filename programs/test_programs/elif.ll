declare i32 @_print_int(i32)
@x = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 1, i32* @x
    br label %L7
L7:
    %.r0 = load i32, i32* @x
    %.r1 = icmp sgt i32 %.r0, 2
    br i1 %.r1, label %L2, label %L8
L2:
    call i32 (i32) @_print_int(i32 99)
    br label %L6
L8:
    %.r2 = load i32, i32* @x
    %.r3 = icmp eq i32 %.r2, 2
    br i1 %.r3, label %L3, label %L9
L3:
    call i32 (i32) @_print_int(i32 2)
    br label %L6
L9:
    %.r4 = load i32, i32* @x
    %.r5 = icmp eq i32 %.r4, 1
    br i1 %.r5, label %L4, label %L5
L4:
    call i32 (i32) @_print_int(i32 1)
    br label %L6
L5:
    call i32 (i32) @_print_int(i32 0)
    br label %L6
L6:
    ret i32 0
}
