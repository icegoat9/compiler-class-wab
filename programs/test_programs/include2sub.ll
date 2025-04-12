declare i32 @_print_int(i32)
declare i32 @printf(ptr noundef, ...)
@.str.1 = private unnamed_addr constant [19 x i8] c"include2subsub.wb
\00"
@.str.2 = private unnamed_addr constant [16 x i8] c"include2sub.wb
\00"

define i32 @times(i32 %.arg_a, i32 %.arg_b) {
entry:
    %a = alloca i32
    store i32 %.arg_a, i32* %a
    %b = alloca i32
    store i32 %.arg_b, i32* %b
    br label %L1
L1:
    %.r1 = load i32, i32* %a
    %.r2 = load i32, i32* %b
    %.r3 = mul i32 %.r1, %.r2
    ret i32 %.r3
}

define i32 @square(i32 %.arg_n) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L2
L2:
    %.r4 = load i32, i32* %n
    %.r5 = load i32, i32* %n
    %.r6 = call i32 (i32, i32) @times(i32 %.r4, i32 %.r5)
    ret i32 %.r6
}

define i32 @main() {
entry:
    br label %L3
L3:
    call i32 (ptr, ...) @printf(ptr noundef @.str.1)
    call i32 (ptr, ...) @printf(ptr noundef @.str.2)
    ret i32 0
}
