declare i32 @_print_int(i32)
declare i32 @printf(ptr noundef, ...)
@.str.1 = private unnamed_addr constant [15 x i8] c"hello, world.
\00"
@.str.2 = private unnamed_addr constant [16 x i8] c"hello\n world.
\00"
@.str.3 = private unnamed_addr constant [15 x i8] c"hello
 world.
\00"
@.str.4 = private unnamed_addr constant [17 x i8] c"hello\13 world.
\00"
@.str.5 = private unnamed_addr constant [18 x i8] c"hello\013 world.
\00"

define i32 @main() {
entry:
    br label %L1
L1:
    call i32 (ptr, ...) @printf(ptr noundef @.str.1)
    call i32 (ptr, ...) @printf(ptr noundef @.str.2)
    call i32 (ptr, ...) @printf(ptr noundef @.str.3)
    call i32 (ptr, ...) @printf(ptr noundef @.str.4)
    call i32 (ptr, ...) @printf(ptr noundef @.str.5)
    ret i32 0
}
