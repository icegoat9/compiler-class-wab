declare i32 @_print_int(i32)

define i32 @mod(i32 %.arg_x, i32 %.arg_n) {
entry:
    %x = alloca i32
    store i32 %.arg_x, i32* %x
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L1
L1:
    %d = alloca i32
    %.r1 = load i32, i32* %x
    %.r2 = load i32, i32* %n
    %.r3 = sdiv i32 %.r1, %.r2
    store i32 %.r3, i32* %d
    %.r4 = load i32, i32* %x
    %.r5 = load i32, i32* %d
    %.r6 = load i32, i32* %n
    %.r7 = mul i32 %.r5, %.r6
    %.r8 = sub i32 %.r4, %.r7
    ret i32 %.r8
}

define i32 @pow(i32 %.arg_x, i32 %.arg_n) {
entry:
    %x = alloca i32
    store i32 %.arg_x, i32* %x
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L2
L2:
    %out = alloca i32
    store i32 1, i32* %out
    %i = alloca i32
    store i32 0, i32* %i
    br label %L30
L30:
    %.r9 = load i32, i32* %i
    %.r10 = load i32, i32* %n
    %.r11 = icmp slt i32 %.r9, %.r10
    br i1 %.r11, label %L3, label %L4
L3:
    %.r12 = load i32, i32* %out
    %.r13 = load i32, i32* %x
    %.r14 = mul i32 %.r12, %.r13
    store i32 %.r14, i32* %out
    %.r15 = load i32, i32* %i
    %.r16 = add i32 %.r15, 1
    store i32 %.r16, i32* %i
    br label %L30
L4:
    %.r17 = load i32, i32* %out
    ret i32 %.r17
}

define i32 @lennum(i32 %.arg_num) {
entry:
    %num = alloca i32
    store i32 %.arg_num, i32* %num
    br label %L5
L5:
    %i = alloca i32
    store i32 1, i32* %i
    %scale = alloca i32
    store i32 10, i32* %scale
    br label %L31
L31:
    %.r18 = load i32, i32* %scale
    %.r19 = load i32, i32* %num
    %.r20 = add i32 %.r19, 1
    %.r21 = icmp slt i32 %.r18, %.r20
    br i1 %.r21, label %L6, label %L7
L6:
    %.r22 = load i32, i32* %scale
    %.r23 = mul i32 %.r22, 10
    store i32 %.r23, i32* %scale
    %.r24 = load i32, i32* %i
    %.r25 = add i32 %.r24, 1
    store i32 %.r25, i32* %i
    br label %L31
L7:
    %.r26 = load i32, i32* %i
    ret i32 %.r26
}

define i32 @concat(i32 %.arg_a, i32 %.arg_b) {
entry:
    %a = alloca i32
    store i32 %.arg_a, i32* %a
    %b = alloca i32
    store i32 %.arg_b, i32* %b
    br label %L8
L8:
    %scale = alloca i32
    %.r27 = load i32, i32* %b
    %.r28 = call i32 (i32) @lennum(i32 %.r27)
    %.r29 = call i32 (i32, i32) @pow(i32 10, i32 %.r28)
    store i32 %.r29, i32* %scale
    %.r30 = load i32, i32* %scale
    %.r31 = load i32, i32* %a
    %.r32 = mul i32 %.r30, %.r31
    %.r33 = load i32, i32* %b
    %.r34 = add i32 %.r32, %.r33
    ret i32 %.r34
}

define i32 @digitn(i32 %.arg_num, i32 %.arg_n) {
entry:
    %num = alloca i32
    store i32 %.arg_num, i32* %num
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L9
L9:
    %x = alloca i32
    %.r35 = load i32, i32* %n
    %.r36 = call i32 (i32, i32) @pow(i32 10, i32 %.r35)
    store i32 %.r36, i32* %x
    %.r37 = load i32, i32* %num
    %.r38 = load i32, i32* %x
    %.r39 = call i32 (i32, i32) @mod(i32 %.r37, i32 %.r38)
    %.r40 = load i32, i32* %num
    %.r41 = load i32, i32* %x
    %.r42 = sdiv i32 %.r41, 10
    %.r43 = call i32 (i32, i32) @mod(i32 %.r40, i32 %.r42)
    %.r44 = sub i32 %.r39, %.r43
    %.r45 = load i32, i32* %x
    %.r46 = sdiv i32 %.r45, 10
    %.r47 = sdiv i32 %.r44, %.r46
    ret i32 %.r47
}

define i32 @mergedigits(i32 %.arg_n) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L10
L10:
    %len = alloca i32
    %.r48 = load i32, i32* %n
    %.r49 = call i32 (i32) @lennum(i32 %.r48)
    store i32 %.r49, i32* %len
    %i = alloca i32
    store i32 1, i32* %i
    %out = alloca i32
    store i32 0, i32* %out
    br label %L34
L34:
    %.r50 = load i32, i32* %len
    %.r51 = icmp eq i32 %.r50, 1
    br i1 %.r51, label %L11, label %L32
L11:
    %.r52 = load i32, i32* %n
    ret i32 %.r52
    br label %L32
L32:
    %.r53 = load i32, i32* %i
    %.r54 = load i32, i32* %len
    %.r55 = icmp slt i32 %.r53, %.r54
    br i1 %.r55, label %L12, label %L16
L12:
    %right = alloca i32
    %.r56 = load i32, i32* %n
    %.r57 = load i32, i32* %i
    %.r58 = call i32 (i32, i32) @digitn(i32 %.r56, i32 %.r57)
    store i32 %.r58, i32* %right
    %left = alloca i32
    %.r59 = load i32, i32* %n
    %.r60 = load i32, i32* %i
    %.r61 = add i32 %.r60, 1
    %.r62 = call i32 (i32, i32) @digitn(i32 %.r59, i32 %.r61)
    store i32 %.r62, i32* %left
    %sum = alloca i32
    %.r63 = load i32, i32* %left
    %.r64 = load i32, i32* %right
    %.r65 = add i32 %.r63, %.r64
    store i32 %.r65, i32* %sum
    br label %L33
L33:
    %.r66 = load i32, i32* %i
    %.r67 = icmp eq i32 %.r66, 1
    br i1 %.r67, label %L13, label %L14
L13:
    %.r68 = load i32, i32* %sum
    store i32 %.r68, i32* %out
    br label %L15
L14:
    %.r69 = load i32, i32* %sum
    %.r70 = load i32, i32* %out
    %.r71 = call i32 (i32, i32) @concat(i32 %.r69, i32 %.r70)
    store i32 %.r71, i32* %out
    br label %L15
L15:
    %.r72 = load i32, i32* %i
    %.r73 = add i32 %.r72, 1
    store i32 %.r73, i32* %i
    br label %L32
L16:
    %.r74 = load i32, i32* %out
    ret i32 %.r74
}

define i32 @mergeloop(i32 %.arg_n, i32 %.arg_verbose) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    %verbose = alloca i32
    store i32 %.arg_verbose, i32* %verbose
    br label %L40
L40:
    %.r75 = load i32, i32* %n
    %.r76 = icmp slt i32 %.r75, 0
    br i1 %.r76, label %L17, label %L18
L17:
    ret i32 -1
    br label %L18
L18:
    %prev = alloca i32
    store i32 0, i32* %prev
    %endloop = alloca i32
    store i32 0, i32* %endloop
    %loops = alloca i32
    store i32 0, i32* %loops
    br label %L35
L35:
    %.r77 = load i32, i32* %endloop
    %.r78 = icmp eq i32 %.r77, 0
    br i1 %.r78, label %L39, label %L26
L39:
    %.r79 = load i32, i32* %verbose
    %.r80 = icmp ne i32 %.r79, 0
    br i1 %.r80, label %L19, label %L20
L19:
    %.r81 = load i32, i32* %n
    call i32 (i32) @_print_int(i32 %.r81)
    br label %L20
L20:
    %.r82 = load i32, i32* %n
    store i32 %.r82, i32* %prev
    %.r83 = load i32, i32* %n
    %.r84 = call i32 (i32) @mergedigits(i32 %.r83)
    store i32 %.r84, i32* %n
    %.r85 = load i32, i32* %loops
    %.r86 = add i32 %.r85, 1
    store i32 %.r86, i32* %loops
    br label %L36
L36:
    %.r87 = load i32, i32* %prev
    %.r88 = load i32, i32* %n
    %.r89 = icmp eq i32 %.r87, %.r88
    br i1 %.r89, label %L21, label %L22
L21:
    store i32 1, i32* %endloop
    br label %L35
L22:
    %len = alloca i32
    %.r90 = load i32, i32* %n
    %.r91 = call i32 (i32) @lennum(i32 %.r90)
    store i32 %.r91, i32* %len
    br label %L37
L37:
    %.r92 = load i32, i32* %len
    %.r93 = icmp sge i32 %.r92, 8
    br i1 %.r93, label %L23, label %L38
L23:
    store i32 2, i32* %endloop
    br label %L35
L38:
    %.r94 = load i32, i32* %loops
    %.r95 = icmp sgt i32 %.r94, 20
    br i1 %.r95, label %L24, label %L25
L24:
    store i32 3, i32* %endloop
    br label %L35
L25:
    store i32 0, i32* %endloop
    br label %L35
L26:
    %.r96 = load i32, i32* %endloop
    ret i32 %.r96
}

define i32 @mainuser(i32 %.arg_argc, i32 %.arg_arg1, i32 %.arg_arg2) {
entry:
    %argc = alloca i32
    store i32 %.arg_argc, i32* %argc
    %arg1 = alloca i32
    store i32 %.arg_arg1, i32* %arg1
    %arg2 = alloca i32
    store i32 %.arg_arg2, i32* %arg2
    br label %L41
L41:
    %.r97 = load i32, i32* %arg1
    %.r98 = icmp ne i32 %.r97, 0
    br i1 %.r98, label %L27, label %L28
L27:
    %.r99 = load i32, i32* %arg1
    %.r100 = load i32, i32* %arg2
    %.r101 = call i32 (i32, i32) @mergeloop(i32 %.r99, i32 %.r100)
    call i32 (i32) @_print_int(i32 %.r101)
    br label %L29
L28:
    %.r102 = call i32 (i32, i32) @mergeloop(i32 1467, i32 1)
    call i32 (i32) @_print_int(i32 %.r102)
    call i32 (i32) @_print_int(i32 -1)
    %.r103 = call i32 (i32, i32) @mergeloop(i32 1792, i32 1)
    call i32 (i32) @_print_int(i32 %.r103)
    call i32 (i32) @_print_int(i32 -1)
    %.r104 = call i32 (i32, i32) @mergeloop(i32 1537, i32 1)
    call i32 (i32) @_print_int(i32 %.r104)
    call i32 (i32) @_print_int(i32 -1)
    br label %L29
L29:
    ret i32 0
}
