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
	movl	$1, _result(%rip)
	movl	$1, _x(%rip)
LBB0_2:                                 ## %L4
                                        ## =>This Inner Loop Header: Depth=1
	cmpl	$10, _x(%rip)
	jge	LBB0_4
## %bb.3:                               ## %L2
                                        ##   in Loop: Header=BB0_2 Depth=1
	movl	_result(%rip), %eax
	imull	_x(%rip), %eax
	movl	%eax, _result(%rip)
	movl	_x(%rip), %eax
	addl	$1, %eax
	movl	%eax, _x(%rip)
	jmp	LBB0_2
LBB0_4:                                 ## %L3
	movl	_result(%rip), %edi
	callq	__print_int
	xorl	%eax, %eax
	popq	%rcx
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_result                         ## @result
.zerofill __DATA,__common,_result,4,2
	.globl	_x                              ## @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
