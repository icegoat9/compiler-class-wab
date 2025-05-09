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
	movl	$10, _x(%rip)
	movl	_x(%rip), %eax
	addl	$1, %eax
	movl	%eax, _x(%rip)
	movl	_x(%rip), %edi
	addl	$1035, %edi                     ## imm = 0x40B
	callq	__print_int
	xorl	%eax, %eax
	popq	%rcx
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_x                              ## @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
