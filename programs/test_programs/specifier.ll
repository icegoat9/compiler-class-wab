declare i32 @_print_int(i32)
declare i32 @printf(ptr noundef, ...)
@x = global i32 0
@y = global i32 0

define i32 @square(i32 %.arg_a) {
entry:
    %a = alloca i32
    store i32 %.arg_a, i32* %a
    br label %L1
L1:
    %result = alloca i32
    %.r1 = load i32, i32* %a
    %.r2 = load i32, i32* %a
    %.r3 = mul i32 %.r1, %.r2
    store i32 %.r3, i32* %result
    %.r4 = load i32, i32* %result
    ret i32 %.r4
}

define i32 @main() {
entry:
    br label %L2
L2:
    store i32 4, i32* @x
    %.r5 = load i32, i32* @x
    %.r6 = call i32 (i32) @square(i32 %.r5)
    store i32 %.r6, i32* @y
    %.r7 = load i32, i32* @y
    call i32 (i32) @_print_int(i32 %.r7)
    ret i32 0
}
