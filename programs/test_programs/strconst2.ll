declare i32 @_print_int(i32)
declare i32 @printf(ptr noundef, ...)
@.str.1 = private unnamed_addr constant [20 x i8] c"function printn():
\00"
@.str.2 = private unnamed_addr constant [14 x i8] c"quite large!
\00"
@.str.3 = private unnamed_addr constant [15 x i8] c"hello, world.
\00"
@x = global i32 0

define i32 @printn(i32 %.arg_n) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L1
L1:
    call i32 (ptr, ...) @printf(ptr noundef @.str.1)
    %.r1 = load i32, i32* %n
    call i32 (i32) @_print_int(i32 %.r1)
    br label %L6
L6:
    %.r2 = load i32, i32* %n
    %.r3 = icmp sgt i32 %.r2, 100
    br i1 %.r3, label %L2, label %L3
L2:
    call i32 (ptr, ...) @printf(ptr noundef @.str.2)
    br label %L4
L3:
    call i32 (i32) @_print_int(i32 -1)
    br label %L4
L4:
    ret i32 0
}

define i32 @main() {
entry:
    br label %L5
L5:
    store i32 7, i32* @x
    call i32 (ptr, ...) @printf(ptr noundef @.str.3)
    %.r4 = load i32, i32* @x
    %.r5 = call i32 (i32) @printn(i32 %.r4)
    %.r6 = call i32 (i32) @printn(i32 200)
    ret i32 0
}
