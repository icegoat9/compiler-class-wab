	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
	.globl	_fact                           ; -- Begin function fact
	.p2align	2
_fact:                                  ; @fact
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	mov	x29, sp
	sub	sp, sp, #32
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	w0, [x29, #-4]
	b	LBB0_1
LBB0_1:                                 ; %L1
	mov	w8, #1                          ; =0x1
	mov	w9, #1                          ; =0x1
                                        ; kill: def $x9 killed $w9
	lsl	x10, x9, #2
	add	x10, x10, #15
	and	x11, x10, #0xfffffffffffffff0
	mov	x10, sp
	subs	x10, x10, x11
	mov	sp, x10
	stur	x10, [x29, #-24]                ; 8-byte Folded Spill
	str	w8, [x10]
	lsl	x9, x9, #2
	add	x9, x9, #15
	and	x10, x9, #0xfffffffffffffff0
	mov	x9, sp
	subs	x9, x9, x10
	mov	sp, x9
	stur	x9, [x29, #-16]                 ; 8-byte Folded Spill
	str	w8, [x9]
	b	LBB0_2
LBB0_2:                                 ; %L7
                                        ; =>This Inner Loop Header: Depth=1
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	ldur	w9, [x29, #-4]
	subs	w8, w8, w9
	cset	w8, gt
	tbnz	w8, #0, LBB0_4
	b	LBB0_3
LBB0_3:                                 ; %L2
                                        ;   in Loop: Header=BB0_2 Depth=1
	ldur	x9, [x29, #-16]                 ; 8-byte Folded Reload
	ldur	x10, [x29, #-24]                ; 8-byte Folded Reload
	ldr	w8, [x10]
	ldr	w11, [x9]
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
	sub	sp, sp, #32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	.cfi_def_cfa_offset 32
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	b	LBB1_1
LBB1_1:                                 ; %L4
	adrp	x9, _x@PAGE
	mov	w8, #1                          ; =0x1
	str	w8, [x9, _x@PAGEOFF]
	b	LBB1_2
LBB1_2:                                 ; %L8
                                        ; =>This Inner Loop Header: Depth=1
	adrp	x8, _x@PAGE
	ldr	w8, [x8, _x@PAGEOFF]
	subs	w8, w8, #10
	cset	w8, ge
	tbnz	w8, #0, LBB1_4
	b	LBB1_3
LBB1_3:                                 ; %L5
                                        ;   in Loop: Header=BB1_2 Depth=1
	adrp	x8, _x@PAGE
	str	x8, [sp, #8]                    ; 8-byte Folded Spill
	ldr	w0, [x8, _x@PAGEOFF]
	bl	_fact
	bl	__print_int
	ldr	x9, [sp, #8]                    ; 8-byte Folded Reload
	ldr	w8, [x9, _x@PAGEOFF]
	add	w8, w8, #1
	str	w8, [x9, _x@PAGEOFF]
	b	LBB1_2
LBB1_4:                                 ; %L6
	mov	w0, #0                          ; =0x0
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_x                              ; @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
