declare i32 @_print_int(i32)

define i32 @sign(i32 %.arg_n) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L6
L6:
    %.r0 = load i32, i32* %n
    %.r1 = icmp sgt i32 %.r0, 0
    br i1 %.r1, label %L1, label %L7
L1:
    ret i32 1
    br label %L4
L7:
    %.r2 = load i32, i32* %n
    %.r3 = icmp slt i32 %.r2, 0
    br i1 %.r3, label %L2, label %L3
L2:
    ret i32 -1
    br label %L4
L3:
    ret i32 0
    br label %L4
L4:
    ret i32 0
}
@x = global i32 0

define i32 @main() {
entry:
    br label %L5
L5:
    store i32 -6, i32* @x
    %.r4 = load i32, i32* @x
    %.r5 = call i32 (i32) @sign(i32 %.r4)
    call i32 (i32) @_print_int(i32 %.r5)
    ret i32 0
}
