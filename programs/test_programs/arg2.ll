declare i32 @_print_int(i32)

define i32 @mainuser(i32 %.arg_argc, i32 %.arg_arg1, i32 %.arg_arg2) {
entry:
    %argc = alloca i32
    store i32 %.arg_argc, i32* %argc
    %arg1 = alloca i32
    store i32 %.arg_arg1, i32* %arg1
    %arg2 = alloca i32
    store i32 %.arg_arg2, i32* %arg2
    br label %L1
L1:
    %.r1 = load i32, i32* %argc
    call i32 (i32) @_print_int(i32 %.r1)
    br label %L5
L5:
    %.r2 = load i32, i32* %argc
    %.r3 = icmp sgt i32 %.r2, 0
    br i1 %.r3, label %L2, label %L4
L2:
    %.r4 = load i32, i32* %arg1
    call i32 (i32) @_print_int(i32 %.r4)
    br label %L6
L6:
    %.r5 = load i32, i32* %argc
    %.r6 = icmp sgt i32 %.r5, 1
    br i1 %.r6, label %L3, label %L4
L3:
    %.r7 = load i32, i32* %arg2
    call i32 (i32) @_print_int(i32 %.r7)
    br label %L4
L4:
    ret i32 0
}
