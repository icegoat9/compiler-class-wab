	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
	.globl	_add1                           ## -- Begin function add1
	.p2align	4, 0x90
_add1:                                  ## @add1
	.cfi_startproc
## %bb.0:                               ## %entry
	movl	%edi, -4(%rsp)
## %bb.1:                               ## %L1
	movl	-4(%rsp), %eax
	addl	$1, %eax
	movl	%eax, -4(%rsp)
	movl	-4(%rsp), %eax
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_main                           ## -- Begin function main
	.p2align	4, 0x90
_main:                                  ## @main
	.cfi_startproc
## %bb.0:                               ## %entry
	pushq	%rax
	.cfi_def_cfa_offset 16
	jmp	LBB1_1
LBB1_1:                                 ## %L2
	movl	$10, _x(%rip)
	movl	_x(%rip), %edi
	callq	_add1
	movl	%eax, %edi
	addl	$1035, %edi                     ## imm = 0x40B
	callq	__print_int
	movl	_x(%rip), %edi
	callq	__print_int
	xorl	%eax, %eax
	popq	%rcx
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_x                              ## @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
