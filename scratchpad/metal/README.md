# Lower-level 'metal' compilation exercises

These are from some quick exercises I did before David Beazley's [Write a Compiler in a week](https://www.dabeaz.com/compiler.html) class, and likely won't make sense without more context-- most of my work is in the other folders.

This runs simple C programs through compiler stages to translate them into LLVM Assembly and lower-level assembly, to manually inspect and understand at the detailed register and instruction level.

But for example, C code like this:

```
int square(int n) {
  return n*n;
}
```

Becomes LLVM (machine-independent, more generic assembly) code:

```
define i32 @square(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %3 = load i32, ptr %2, align 4
  %4 = load i32, ptr %2, align 4
  %5 = mul nsw i32 %3, %4
  ret i32 %5
}
```

Becomes lower-level assembly like:

```
	.globl	_square                        
	.p2align	2
_square:                              
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #16
	.cfi_def_cfa_offset 16
	str	w0, [sp, #12]
	ldr	w8, [sp, #12]
	ldr	w9, [sp, #12]
	mul	w0, w8, w9
	add	sp, sp, #16
	ret
	.cfi_endproc
```