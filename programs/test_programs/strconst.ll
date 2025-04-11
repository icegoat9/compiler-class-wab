declare i32 @_print_int(i32)
declare i32 @printf(ptr noundef, ...)
@.str.1 = private unnamed_addr constant [15 x i8] c"hello, world.
\00"
@.str.2 = private unnamed_addr constant [8 x i8] c"now x=
\00"
@x = global i32 0

define i32 @main() {
entry:
    br label %L1
L1:
    store i32 7, i32* @x
    call i32 (ptr, ...) @printf(ptr noundef @.str.1)
    call i32 (i32) @_print_int(i32 3)
    call i32 (ptr, ...) @printf(ptr noundef @.str.2)
    %.r1 = load i32, i32* @x
    call i32 (i32) @_print_int(i32 %.r1)
    ret i32 0
}
