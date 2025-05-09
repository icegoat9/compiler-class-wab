	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
	.globl	_factre                         ## -- Begin function factre
	.p2align	4, 0x90
_factre:                                ## @factre
	.cfi_startproc
## %bb.0:                               ## %entry
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movl	%edi, 20(%rsp)
	movl	%esi, 16(%rsp)
## %bb.1:                               ## %L10
	movl	20(%rsp), %eax
	cmpl	16(%rsp), %eax
	jne	LBB0_3
## %bb.2:                               ## %L1
	movl	16(%rsp), %eax
	addq	$24, %rsp
	retq
LBB0_3:                                 ## %L2
	movl	20(%rsp), %eax
	movl	%eax, 12(%rsp)                  ## 4-byte Spill
	movl	20(%rsp), %edi
	addl	$1, %edi
	movl	16(%rsp), %esi
	callq	_factre
	movl	%eax, %ecx
	movl	12(%rsp), %eax                  ## 4-byte Reload
	imull	%ecx, %eax
	addq	$24, %rsp
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_fact                           ## -- Begin function fact
	.p2align	4, 0x90
_fact:                                  ## @fact
	.cfi_startproc
## %bb.0:                               ## %entry
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	%edi, 4(%rsp)
## %bb.1:                               ## %L11
	xorl	%eax, %eax
	cmpl	4(%rsp), %eax
	jge	LBB1_3
## %bb.2:                               ## %L4
	movl	4(%rsp), %esi
	movl	$1, %edi
	callq	_factre
	popq	%rcx
	retq
LBB1_3:                                 ## %L5
	movl	$1, %eax
	popq	%rcx
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
	jmp	LBB2_1
LBB2_1:                                 ## %L7
	movl	$1, _x(%rip)
LBB2_2:                                 ## %L12
                                        ## =>This Inner Loop Header: Depth=1
	cmpl	$10, _x(%rip)
	jge	LBB2_4
## %bb.3:                               ## %L8
                                        ##   in Loop: Header=BB2_2 Depth=1
	movl	_x(%rip), %edi
	callq	_fact
	movl	%eax, %edi
	callq	__print_int
	movl	_x(%rip), %eax
	addl	$1, %eax
	movl	%eax, _x(%rip)
	jmp	LBB2_2
LBB2_4:                                 ## %L9
	xorl	%eax, %eax
	popq	%rcx
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_x                              ## @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
