declare i32 @_print_int(i32)
@temp = global i32 0

define i32 @mainuser(i32 %.arg_argc, i32 %.arg_arg1) {
entry:
    %argc = alloca i32
    store i32 %.arg_argc, i32* %argc
    %arg1 = alloca i32
    store i32 %.arg_arg1, i32* %arg1
    br label %L1
L1:
    %.r1 = load i32, i32* %argc
    call i32 (i32) @_print_int(i32 %.r1)
    br label %L5
L5:
    %.r2 = load i32, i32* %argc
    %.r3 = icmp sgt i32 %.r2, 0
    br i1 %.r3, label %L2, label %L3
L2:
    %.r4 = load i32, i32* %arg1
    call i32 (i32) @_print_int(i32 %.r4)
    br label %L3
L3:
    ret i32 0
}

define i32 @mainuserignored(i32 %.arg_argc, i32 %.arg_arg1) {
entry:
    %argc = alloca i32
    store i32 %.arg_argc, i32* %argc
    %arg1 = alloca i32
    store i32 %.arg_arg1, i32* %arg1
    br label %L4
L4:
    store i32 77, i32* @temp
    ret i32 0
}
