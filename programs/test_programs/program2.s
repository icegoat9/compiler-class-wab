	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
	.globl	_main                           ## -- Begin function main
	.p2align	4, 0x90
_main:                                  ## @main
	.cfi_startproc
## %bb.0:                               ## %entry
	pushq	%rax
	.cfi_def_cfa_offset 16
	jmp	LBB0_1
LBB0_1:                                 ## %L1
	movl	$3, _x(%rip)
	movl	$4, _y(%rip)
	movl	$0, _min(%rip)
## %bb.2:                               ## %L5
	movl	_x(%rip), %eax
	cmpl	_y(%rip), %eax
	jge	LBB0_4
## %bb.3:                               ## %L2
	movl	_x(%rip), %eax
	movl	%eax, _min(%rip)
	jmp	LBB0_5
LBB0_4:                                 ## %L3
	movl	_y(%rip), %eax
	movl	%eax, _min(%rip)
LBB0_5:                                 ## %L4
	movl	_min(%rip), %edi
	callq	__print_int
	xorl	%eax, %eax
	popq	%rcx
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_x                              ## @x
.zerofill __DATA,__common,_x,4,2
	.globl	_y                              ## @y
.zerofill __DATA,__common,_y,4,2
	.globl	_min                            ## @min
.zerofill __DATA,__common,_min,4,2
.subsections_via_symbols
