declare i32 @_print_int(i32)

define i32 @pow(i32 %.arg_x, i32 %.arg_n) {
entry:
    %x = alloca i32
    store i32 %.arg_x, i32* %x
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L1
L1:
    %i = alloca i32
    store i32 0, i32* %i
    %result = alloca i32
    store i32 1, i32* %result
    br label %L5
L5:
    %.r0 = load i32, i32* %i
    %.r1 = load i32, i32* %n
    %.r2 = icmp slt i32 %.r0, %.r1
    br i1 %.r2, label %L2, label %L3
L2:
    %.r3 = load i32, i32* %result
    %.r4 = load i32, i32* %x
    %.r5 = mul i32 %.r3, %.r4
    store i32 %.r5, i32* %result
    %.r6 = load i32, i32* %i
    %.r7 = add i32 %.r6, 1
    store i32 %.r7, i32* %i
    br label %L5
L3:
    %.r8 = load i32, i32* %result
    ret i32 %.r8
}

define i32 @main() {
entry:
    br label %L4
L4:
    call i32 (i32) @_print_int(i32 3)
    call i32 (i32) @_print_int(i32 4)
    %.r9 = call i32 (i32, i32) @pow(i32 3, i32 4)
    call i32 (i32) @_print_int(i32 %.r9)
    ret i32 0
}
