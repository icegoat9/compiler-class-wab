declare i32 @_print_int(i32)

define i32 @absclamped(i32 %.arg_n, i32 %.arg_bound) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    %bound = alloca i32
    store i32 %.arg_bound, i32* %bound
    br label %L9
L9:
    %.r0 = load i32, i32* %n
    %.r1 = icmp sgt i32 %.r0, 0
    br i1 %.r1, label %L10, label %L11
L10:
    %.r2 = load i32, i32* %n
    %.r3 = load i32, i32* %bound
    %.r4 = icmp sgt i32 %.r2, %.r3
    br i1 %.r4, label %L1, label %L2
L1:
    %.r5 = load i32, i32* %bound
    ret i32 %.r5
    br label %L7
L2:
    %.r6 = load i32, i32* %n
    ret i32 %.r6
    br label %L7
L11:
    %.r7 = load i32, i32* %n
    %.r8 = icmp eq i32 %.r7, 0
    br i1 %.r8, label %L3, label %L12
L3:
    ret i32 0
    br label %L7
L12:
    %.r9 = load i32, i32* %n
    %.r10 = load i32, i32* %bound
    %.r11 = sub i32 0, %.r10
    %.r12 = icmp slt i32 %.r9, %.r11
    br i1 %.r12, label %L4, label %L13
L4:
    %.r13 = load i32, i32* %bound
    ret i32 %.r13
    br label %L7
L13:
    %.r14 = load i32, i32* %n
    %.r15 = load i32, i32* %bound
    %.r16 = sub i32 0, %.r15
    %.r17 = icmp eq i32 %.r14, %.r16
    br i1 %.r17, label %L5, label %L6
L5:
    ret i32 -9999
    br label %L7
L6:
    %.r18 = load i32, i32* %n
    %.r19 = sub i32 0, %.r18
    ret i32 %.r19
    br label %L7
L7:
    ret i32 0
}

define i32 @main() {
entry:
    br label %L8
L8:
    %.r20 = call i32 (i32, i32) @absclamped(i32 0, i32 10)
    call i32 (i32) @_print_int(i32 %.r20)
    %.r21 = call i32 (i32, i32) @absclamped(i32 13, i32 10)
    call i32 (i32) @_print_int(i32 %.r21)
    %.r22 = call i32 (i32, i32) @absclamped(i32 -13, i32 10)
    call i32 (i32) @_print_int(i32 %.r22)
    %.r23 = call i32 (i32, i32) @absclamped(i32 -13, i32 20)
    call i32 (i32) @_print_int(i32 %.r23)
    %.r24 = call i32 (i32, i32) @absclamped(i32 -13, i32 13)
    call i32 (i32) @_print_int(i32 %.r24)
    ret i32 0
}
