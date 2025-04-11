declare i32 @_print_int(i32)
declare i32 @printf(ptr noundef, ...)
@.str.1 = private unnamed_addr constant [6 x i8] c"1==1
\00"

define i32 @foo() {
entry:
    br label %L4
L4:
    %.r1 = icmp eq i32 1, 1
    br i1 %.r1, label %L1, label %L2
L1:
    call i32 (ptr, ...) @printf(ptr noundef @.str.1)
    br label %L2
L2:
    ret i32 0
}

define i32 @main() {
entry:
    br label %L3
L3:
    %.r2 = call i32 () @foo()
    ret i32 0
}
