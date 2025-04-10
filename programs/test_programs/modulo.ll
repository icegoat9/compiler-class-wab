declare i32 @_print_int(i32)
@x = global i32 0
@y = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 5, i32* @x
    store i32 3, i32* @y
    %.r1 = load i32, i32* @x
    call i32 (i32) @_print_int(i32 %.r1)
    %.r2 = load i32, i32* @y
    call i32 (i32) @_print_int(i32 %.r2)
    %.r3 = load i32, i32* @x
    %.r4 = load i32, i32* @y
    %.r5 = sdiv i32 %.r3, %.r4
    call i32 (i32) @_print_int(i32 %.r5)
    %.r6 = load i32, i32* @x
    %.r7 = load i32, i32* @y
    %.r8 = srem i32 %.r6, %.r7
    call i32 (i32) @_print_int(i32 %.r8)
    %.r9 = load i32, i32* @x
    %.r10 = sub i32 0, %.r9
    %.r11 = load i32, i32* @y
    %.r12 = sdiv i32 %.r10, %.r11
    call i32 (i32) @_print_int(i32 %.r12)
    %.r13 = load i32, i32* @x
    %.r14 = sub i32 0, %.r13
    %.r15 = load i32, i32* @y
    %.r16 = srem i32 %.r14, %.r15
    call i32 (i32) @_print_int(i32 %.r16)
    %.r17 = load i32, i32* @x
    %.r18 = load i32, i32* @y
    %.r19 = sub i32 0, %.r18
    %.r20 = sdiv i32 %.r17, %.r19
    call i32 (i32) @_print_int(i32 %.r20)
    %.r21 = load i32, i32* @x
    %.r22 = sub i32 0, %.r21
    %.r23 = load i32, i32* @y
    %.r24 = sub i32 0, %.r23
    %.r25 = srem i32 %.r22, %.r24
    call i32 (i32) @_print_int(i32 %.r25)
    %.r26 = load i32, i32* @x
    %.r27 = sub i32 0, %.r26
    %.r28 = load i32, i32* @y
    %.r29 = sub i32 0, %.r28
    %.r30 = srem i32 %.r27, %.r29
    call i32 (i32) @_print_int(i32 %.r30)
    ret i32 0
}
