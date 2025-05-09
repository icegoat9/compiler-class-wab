declare i32 @_print_int(i32)
declare i32 @printf(ptr noundef, ...)

define i32 @fact(i32 %.arg_n) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L9
L9:
    %.r1 = load i32, i32* %n
    %.r2 = icmp slt i32 %.r1, 2
    br i1 %.r2, label %L1, label %L2
L1:
    ret i32 1
    br label %L5
L2:
    %x = alloca i32
    store i32 1, i32* %x
    %result = alloca i32
    store i32 1, i32* %result
    br label %L10
L10:
    %.r3 = load i32, i32* %x
    %.r4 = load i32, i32* %n
    %.r5 = icmp slt i32 %.r3, %.r4
    br i1 %.r5, label %L3, label %L4
L3:
    %.r6 = load i32, i32* %result
    %.r7 = load i32, i32* %x
    %.r8 = mul i32 %.r6, %.r7
    store i32 %.r8, i32* %result
    %.r9 = load i32, i32* %x
    %.r10 = add i32 %.r9, 1
    store i32 %.r10, i32* %x
    br label %L10
L4:
    %.r11 = load i32, i32* %result
    %.r12 = load i32, i32* %n
    %.r13 = mul i32 %.r11, %.r12
    ret i32 %.r13
    br label %L5
L5:
    ret i32 0
}
@x = global i32 0

define i32 @main() {
entry:
    br label %L6
L6:
    store i32 1, i32* @x
    br label %L11
L11:
    %.r14 = load i32, i32* @x
    %.r15 = icmp slt i32 %.r14, 10
    br i1 %.r15, label %L7, label %L8
L7:
    %.r16 = load i32, i32* @x
    %.r17 = call i32 (i32) @fact(i32 %.r16)
    call i32 (i32) @_print_int(i32 %.r17)
    %.r18 = load i32, i32* @x
    %.r19 = add i32 %.r18, 1
    store i32 %.r19, i32* @x
    br label %L11
L8:
    ret i32 0
}
