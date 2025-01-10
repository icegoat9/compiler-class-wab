declare i32 @_print_int(i32)
@x = global i32 0
@y = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 2, i32* @x
    store i32 5, i32* @y
    br label %L20
L20:
    %.r0 = load i32, i32* @x
    %.r1 = load i32, i32* @y
    %.r2 = icmp slt i32 %.r0, %.r1
    br i1 %.r2, label %L2, label %L3
L2:
    call i32 (i32) @_print_int(i32 1)
    br label %L19
L3:
    call i32 (i32) @_print_int(i32 0)
    br label %L19
L19:
    %.r3 = load i32, i32* @x
    %.r4 = load i32, i32* @y
    %.r5 = icmp sle i32 %.r3, %.r4
    br i1 %.r5, label %L4, label %L5
L4:
    call i32 (i32) @_print_int(i32 1)
    br label %L18
L5:
    call i32 (i32) @_print_int(i32 0)
    br label %L18
L18:
    %.r6 = load i32, i32* @y
    %.r7 = load i32, i32* @x
    %.r8 = icmp sgt i32 %.r6, %.r7
    br i1 %.r8, label %L6, label %L7
L6:
    call i32 (i32) @_print_int(i32 1)
    br label %L17
L7:
    call i32 (i32) @_print_int(i32 0)
    br label %L17
L17:
    %.r9 = load i32, i32* @y
    %.r10 = load i32, i32* @x
    %.r11 = icmp sge i32 %.r9, %.r10
    br i1 %.r11, label %L8, label %L9
L8:
    call i32 (i32) @_print_int(i32 1)
    br label %L16
L9:
    call i32 (i32) @_print_int(i32 0)
    br label %L16
L16:
    %.r12 = load i32, i32* @x
    %.r13 = load i32, i32* @y
    %.r14 = icmp eq i32 %.r12, %.r13
    br i1 %.r14, label %L10, label %L11
L10:
    call i32 (i32) @_print_int(i32 0)
    br label %L15
L11:
    call i32 (i32) @_print_int(i32 1)
    br label %L15
L15:
    %.r15 = load i32, i32* @x
    %.r16 = load i32, i32* @y
    %.r17 = icmp ne i32 %.r15, %.r16
    br i1 %.r17, label %L12, label %L13
L12:
    call i32 (i32) @_print_int(i32 1)
    br label %L14
L13:
    call i32 (i32) @_print_int(i32 0)
    br label %L14
L14:
    ret i32 0
}
