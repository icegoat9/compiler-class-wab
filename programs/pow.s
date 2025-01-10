	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0
	.globl	_pow                            ; -- Begin function pow
	.p2align	2
_pow:                                   ; @pow
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	.cfi_def_cfa_offset 16
	mov	x29, sp
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	sub	sp, sp, #32
	stur	w0, [x29, #-4]
	stur	w1, [x29, #-8]
	b	LBB0_1
LBB0_1:                                 ; %L1
	mov	w8, #1
                                        ; kill: def $x8 killed $w8
	lsl	x9, x8, #2
	add	x9, x9, #15
	and	x10, x9, #0xfffffffffffffff0
	mov	x9, sp
	subs	x10, x9, x10
	mov	sp, x10
	stur	x10, [x29, #-24]                ; 8-byte Folded Spill
	mov	w9, #1
	str	w9, [x10]
	lsl	x8, x8, #2
	add	x8, x8, #15
	and	x9, x8, #0xfffffffffffffff0
	mov	x8, sp
	subs	x8, x8, x9
	mov	sp, x8
	stur	x8, [x29, #-16]                 ; 8-byte Folded Spill
	str	wzr, [x8]
	b	LBB0_2
LBB0_2:                                 ; %L5
                                        ; =>This Inner Loop Header: Depth=1
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	ldur	w9, [x29, #-8]
	subs	w8, w8, w9
	cset	w8, ge
	tbnz	w8, #0, LBB0_4
	b	LBB0_3
LBB0_3:                                 ; %L2
                                        ;   in Loop: Header=BB0_2 Depth=1
	ldur	x9, [x29, #-16]                 ; 8-byte Folded Reload
	ldur	x10, [x29, #-24]                ; 8-byte Folded Reload
	ldr	w8, [x10]
	ldur	w11, [x29, #-4]
	mul	w8, w8, w11
	str	w8, [x10]
	ldr	w8, [x9]
	add	w8, w8, #1
	str	w8, [x9]
	b	LBB0_2
LBB0_4:                                 ; %L3
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	ldr	w0, [x8]
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	.cfi_def_cfa_offset 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	b	LBB1_1
LBB1_1:                                 ; %L4
	mov	w0, #3
	mov	w1, #4
	bl	_pow
	adrp	x8, _x@PAGE
	str	w0, [x8, _x@PAGEOFF]
	ldr	w0, [x8, _x@PAGEOFF]
	bl	__print_int
	mov	w0, #0
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_x                              ; @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
