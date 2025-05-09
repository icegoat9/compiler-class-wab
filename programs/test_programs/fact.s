	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
	.globl	_fact                           ## -- Begin function fact
	.p2align	4, 0x90
_fact:                                  ## @fact
	.cfi_startproc
## %bb.0:                               ## %entry
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movl	%edi, -4(%rbp)
## %bb.1:                               ## %L9
	cmpl	$2, -4(%rbp)
	jge	LBB0_3
## %bb.2:                               ## %L1
	movl	$1, %eax
	movq	%rbp, %rsp
	popq	%rbp
	retq
LBB0_3:                                 ## %L2
	movq	%rsp, %rax
	movq	%rax, %rcx
	addq	$-16, %rcx
	movq	%rcx, -24(%rbp)                 ## 8-byte Spill
	movq	%rcx, %rsp
	movl	$1, -16(%rax)
	movq	%rsp, %rax
	addq	$-16, %rax
	movq	%rax, -16(%rbp)                 ## 8-byte Spill
	movq	%rax, %rsp
	movl	$1, (%rax)
LBB0_4:                                 ## %L10
                                        ## =>This Inner Loop Header: Depth=1
	movq	-24(%rbp), %rax                 ## 8-byte Reload
	movl	(%rax), %eax
	cmpl	-4(%rbp), %eax
	jge	LBB0_6
## %bb.5:                               ## %L3
                                        ##   in Loop: Header=BB0_4 Depth=1
	movq	-24(%rbp), %rax                 ## 8-byte Reload
	movq	-16(%rbp), %rcx                 ## 8-byte Reload
	movl	(%rcx), %edx
	imull	(%rax), %edx
	movl	%edx, (%rcx)
	movl	(%rax), %ecx
	addl	$1, %ecx
	movl	%ecx, (%rax)
	jmp	LBB0_4
LBB0_6:                                 ## %L4
	movq	-16(%rbp), %rax                 ## 8-byte Reload
	movl	(%rax), %eax
	imull	-4(%rbp), %eax
	movq	%rbp, %rsp
	popq	%rbp
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
LBB1_1:                                 ## %L6
	movl	$1, _x(%rip)
LBB1_2:                                 ## %L11
                                        ## =>This Inner Loop Header: Depth=1
	cmpl	$10, _x(%rip)
	jge	LBB1_4
## %bb.3:                               ## %L7
                                        ##   in Loop: Header=BB1_2 Depth=1
	movl	_x(%rip), %edi
	callq	_fact
	movl	%eax, %edi
	callq	__print_int
	movl	_x(%rip), %eax
	addl	$1, %eax
	movl	%eax, _x(%rip)
	jmp	LBB1_2
LBB1_4:                                 ## %L8
	xorl	%eax, %eax
	popq	%rcx
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_x                              ## @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
