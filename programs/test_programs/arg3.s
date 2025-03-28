	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
	.globl	_subscope                       ; -- Begin function subscope
	.p2align	2
_subscope:                              ; @subscope
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	.cfi_def_cfa_offset 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	b	LBB0_1
LBB0_1:                                 ; %L1
	adrp	x8, _y@PAGE
	ldr	w0, [x8, _y@PAGEOFF]
	bl	__print_int
	mov	w0, #0                          ; =0x0
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_testscope                      ; -- Begin function testscope
	.p2align	2
_testscope:                             ; @testscope
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	mov	x29, sp
	sub	sp, sp, #16
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	w0, [x29, #-4]
	b	LBB1_1
LBB1_1:                                 ; %L2
	ldur	w0, [x29, #-4]
	bl	__print_int
	adrp	x8, _y@PAGE
	ldr	w0, [x8, _y@PAGEOFF]
	bl	__print_int
	mov	w8, #1                          ; =0x1
                                        ; kill: def $x8 killed $w8
	lsl	x9, x8, #2
	add	x9, x9, #15
	and	x10, x9, #0xfffffffffffffff0
	mov	x9, sp
	subs	x10, x9, x10
	mov	sp, x10
	mov	w9, #66                         ; =0x42
	str	w9, [x10]
	lsl	x8, x8, #2
	add	x8, x8, #15
	and	x9, x8, #0xfffffffffffffff0
	mov	x8, sp
	subs	x8, x8, x9
	mov	sp, x8
	stur	x8, [x29, #-16]                 ; 8-byte Folded Spill
	bl	_subscope
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	str	w0, [x8]
	mov	w0, #0                          ; =0x0
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
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
	str	w2, [sp, #4]
	b	LBB2_1
LBB2_1:                                 ; %L3
	adrp	x9, _y@PAGE
	mov	w8, #55                         ; =0x37
	str	w8, [x9, _y@PAGEOFF]
	ldr	w0, [sp, #12]
	bl	__print_int
	b	LBB2_2
LBB2_2:                                 ; %L7
	ldr	w8, [sp, #12]
	subs	w8, w8, #0
	cset	w8, le
	tbnz	w8, #0, LBB2_6
	b	LBB2_3
LBB2_3:                                 ; %L4
	ldr	w0, [sp, #8]
	bl	__print_int
	b	LBB2_4
LBB2_4:                                 ; %L8
	ldr	w8, [sp, #12]
	subs	w8, w8, #1
	cset	w8, le
	tbnz	w8, #0, LBB2_6
	b	LBB2_5
LBB2_5:                                 ; %L5
	ldr	w0, [sp, #4]
	bl	__print_int
	b	LBB2_6
LBB2_6:                                 ; %L6
	mov	w0, #99                         ; =0x63
	bl	_testscope
	bl	__print_int
	mov	w0, #0                          ; =0x0
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_y                              ; @y
.zerofill __DATA,__common,_y,4,2
.subsections_via_symbols
