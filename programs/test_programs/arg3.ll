declare i32 @_print_int(i32)
@y = global i32 0

define i32 @subscope() {
entry:
    br label %L1
L1:
    %.r1 = load i32, i32* @y
    call i32 (i32) @_print_int(i32 %.r1)
    ret i32 0
}

define i32 @testscope(i32 %.arg_x) {
entry:
    %x = alloca i32
    store i32 %.arg_x, i32* %x
    br label %L2
L2:
    %.r2 = load i32, i32* %x
    call i32 (i32) @_print_int(i32 %.r2)
    %.r3 = load i32, i32* @y
    call i32 (i32) @_print_int(i32 %.r3)
    %z = alloca i32
    store i32 66, i32* %z
    %w = alloca i32
    %.r4 = call i32 () @subscope()
    store i32 %.r4, i32* %w
    ret i32 0
}

define i32 @mainuser(i32 %.arg_argc, i32 %.arg_arg1, i32 %.arg_arg2) {
entry:
    %argc = alloca i32
    store i32 %.arg_argc, i32* %argc
    %arg1 = alloca i32
    store i32 %.arg_arg1, i32* %arg1
    %arg2 = alloca i32
    store i32 %.arg_arg2, i32* %arg2
    br label %L3
L3:
    store i32 55, i32* @y
    %.r5 = load i32, i32* %argc
    call i32 (i32) @_print_int(i32 %.r5)
    br label %L7
L7:
    %.r6 = load i32, i32* %argc
    %.r7 = icmp sgt i32 %.r6, 0
    br i1 %.r7, label %L4, label %L6
L4:
    %.r8 = load i32, i32* %arg1
    call i32 (i32) @_print_int(i32 %.r8)
    br label %L8
L8:
    %.r9 = load i32, i32* %argc
    %.r10 = icmp sgt i32 %.r9, 1
    br i1 %.r10, label %L5, label %L6
L5:
    %.r11 = load i32, i32* %arg2
    call i32 (i32) @_print_int(i32 %.r11)
    br label %L6
L6:
    %.r12 = call i32 (i32) @testscope(i32 99)
    call i32 (i32) @_print_int(i32 %.r12)
    ret i32 0
}
