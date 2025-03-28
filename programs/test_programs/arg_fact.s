	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
	.globl	_factre                         ; -- Begin function factre
	.p2align	2
_factre:                                ; @factre
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
LBB0_1:                                 ; %L10
	ldr	w8, [sp, #12]
	ldr	w9, [sp, #8]
	subs	w8, w8, w9
	cset	w8, ne
	tbnz	w8, #0, LBB0_3
	b	LBB0_2
LBB0_2:                                 ; %L1
	ldr	w0, [sp, #8]
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
LBB0_3:                                 ; %L2
	ldr	w8, [sp, #12]
	str	w8, [sp, #4]                    ; 4-byte Folded Spill
	ldr	w8, [sp, #12]
	add	w0, w8, #1
	ldr	w1, [sp, #8]
	bl	_factre
	ldr	w8, [sp, #4]                    ; 4-byte Folded Reload
	mul	w0, w8, w0
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_fact                           ; -- Begin function fact
	.p2align	2
_fact:                                  ; @fact
	.cfi_startproc
; %bb.0:                                ; %entry
	sub	sp, sp, #32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	.cfi_def_cfa_offset 32
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	str	w0, [sp, #12]
	b	LBB1_1
LBB1_1:                                 ; %L11
	ldr	w8, [sp, #12]
	subs	w8, w8, #0
	cset	w8, le
	tbnz	w8, #0, LBB1_3
	b	LBB1_2
LBB1_2:                                 ; %L4
	ldr	w1, [sp, #12]
	mov	w0, #1                          ; =0x1
	bl	_factre
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
LBB1_3:                                 ; %L5
	mov	w0, #1                          ; =0x1
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
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
	b	LBB2_1
LBB2_1:                                 ; %L12
	ldr	w8, [sp, #12]
	subs	w8, w8, #0
	cset	w8, le
	tbnz	w8, #0, LBB2_3
	b	LBB2_2
LBB2_2:                                 ; %L7
	ldr	w0, [sp, #8]
	bl	_fact
	bl	__print_int
	b	LBB2_4
LBB2_3:                                 ; %L8
	mov	w0, #1                          ; =0x1
	bl	_fact
	bl	__print_int
	b	LBB2_4
LBB2_4:                                 ; %L9
	mov	w0, #0                          ; =0x0
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
.subsections_via_symbols
