declare i32 @_print_int(i32)
declare i32 @_print_float(double)
declare i32 @printf(ptr noundef, ...)

define i32 @main() {
entry:
    br label %L1
L1:
    call i32 (i32) @_print_int(i32 3.14)
    ret i32 0
}
