	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
	.globl	_mainuser                       ; -- Begin function mainuser
	.p2align	2
_mainuser:                              ; @mainuser
	.cfi_startproc
; %bb.0:                                ; %entry
	sub	sp, sp, #32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	.cfi_def_cfa_offset 32
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	str	w0, [sp, #12]
	str	w1, [sp, #8]
	b	LBB0_1
LBB0_1:                                 ; %L1
	ldr	w0, [sp, #12]
	bl	__print_int
	b	LBB0_2
LBB0_2:                                 ; %L5
	ldr	w8, [sp, #12]
	subs	w8, w8, #0
	cset	w8, le
	tbnz	w8, #0, LBB0_4
	b	LBB0_3
LBB0_3:                                 ; %L2
	ldr	w0, [sp, #8]
	bl	__print_int
	b	LBB0_4
LBB0_4:                                 ; %L3
	mov	w0, #0                          ; =0x0
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_mainuserignored                ; -- Begin function mainuserignored
	.p2align	2
_mainuserignored:                       ; @mainuserignored
	.cfi_startproc
; %bb.0:                                ; %entry
	sub	sp, sp, #16
	.cfi_def_cfa_offset 16
	str	w0, [sp, #12]
	str	w1, [sp, #8]
	b	LBB1_1
LBB1_1:                                 ; %L4
	adrp	x9, _temp@PAGE
	mov	w8, #77                         ; =0x4d
	str	w8, [x9, _temp@PAGEOFF]
	mov	w0, #0                          ; =0x0
	add	sp, sp, #16
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_temp                           ; @temp
.zerofill __DATA,__common,_temp,4,2
.subsections_via_symbols
