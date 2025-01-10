	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0
	.globl	_mod                            ; -- Begin function mod
	.p2align	2
_mod:                                   ; @mod
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	.cfi_def_cfa_offset 16
	mov	x29, sp
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	sub	sp, sp, #16
	stur	w0, [x29, #-4]
	stur	w1, [x29, #-8]
	b	LBB0_1
LBB0_1:                                 ; %L1
	mov	w8, #1
                                        ; kill: def $x8 killed $w8
	lsl	x8, x8, #2
	add	x8, x8, #15
	and	x9, x8, #0xfffffffffffffff0
	mov	x8, sp
	subs	x9, x8, x9
	mov	sp, x9
	ldur	w8, [x29, #-4]
	ldur	w10, [x29, #-8]
	sdiv	w8, w8, w10
	str	w8, [x9]
	ldur	w8, [x29, #-4]
	ldr	w9, [x9]
	ldur	w10, [x29, #-8]
	mul	w9, w9, w10
	subs	w0, w8, w9
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
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
	b	LBB1_1
LBB1_1:                                 ; %L2
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
	b	LBB1_2
LBB1_2:                                 ; %L30
                                        ; =>This Inner Loop Header: Depth=1
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	ldur	w9, [x29, #-8]
	subs	w8, w8, w9
	cset	w8, ge
	tbnz	w8, #0, LBB1_4
	b	LBB1_3
LBB1_3:                                 ; %L3
                                        ;   in Loop: Header=BB1_2 Depth=1
	ldur	x9, [x29, #-16]                 ; 8-byte Folded Reload
	ldur	x10, [x29, #-24]                ; 8-byte Folded Reload
	ldr	w8, [x10]
	ldur	w11, [x29, #-4]
	mul	w8, w8, w11
	str	w8, [x10]
	ldr	w8, [x9]
	add	w8, w8, #1
	str	w8, [x9]
	b	LBB1_2
LBB1_4:                                 ; %L4
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	ldr	w0, [x8]
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_lennum                         ; -- Begin function lennum
	.p2align	2
_lennum:                                ; @lennum
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
	b	LBB2_1
LBB2_1:                                 ; %L5
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
	subs	x9, x8, x9
	mov	sp, x9
	stur	x9, [x29, #-16]                 ; 8-byte Folded Spill
	mov	w8, #10
	str	w8, [x9]
	b	LBB2_2
LBB2_2:                                 ; %L31
                                        ; =>This Inner Loop Header: Depth=1
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	ldur	w9, [x29, #-4]
	add	w9, w9, #1
	subs	w8, w8, w9
	cset	w8, ge
	tbnz	w8, #0, LBB2_4
	b	LBB2_3
LBB2_3:                                 ; %L6
                                        ;   in Loop: Header=BB2_2 Depth=1
	ldur	x9, [x29, #-24]                 ; 8-byte Folded Reload
	ldur	x10, [x29, #-16]                ; 8-byte Folded Reload
	ldr	w8, [x10]
	mov	w11, #10
	mul	w8, w8, w11
	str	w8, [x10]
	ldr	w8, [x9]
	add	w8, w8, #1
	str	w8, [x9]
	b	LBB2_2
LBB2_4:                                 ; %L7
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	ldr	w0, [x8]
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_concat                         ; -- Begin function concat
	.p2align	2
_concat:                                ; @concat
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	.cfi_def_cfa_offset 16
	mov	x29, sp
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	sub	sp, sp, #16
	stur	w0, [x29, #-4]
	stur	w1, [x29, #-8]
	b	LBB3_1
LBB3_1:                                 ; %L8
	mov	w8, #1
                                        ; kill: def $x8 killed $w8
	lsl	x8, x8, #2
	add	x8, x8, #15
	and	x9, x8, #0xfffffffffffffff0
	mov	x8, sp
	subs	x8, x8, x9
	mov	sp, x8
	stur	x8, [x29, #-16]                 ; 8-byte Folded Spill
	ldur	w0, [x29, #-8]
	bl	_lennum
	mov	x1, x0
	mov	w0, #10
	bl	_pow
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	str	w0, [x8]
	ldr	w8, [x8]
	ldur	w9, [x29, #-4]
	mul	w8, w8, w9
	ldur	w9, [x29, #-8]
	add	w0, w8, w9
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_digitn                         ; -- Begin function digitn
	.p2align	2
_digitn:                                ; @digitn
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
	b	LBB4_1
LBB4_1:                                 ; %L9
	mov	w8, #1
                                        ; kill: def $x8 killed $w8
	lsl	x8, x8, #2
	add	x8, x8, #15
	and	x9, x8, #0xfffffffffffffff0
	mov	x8, sp
	subs	x8, x8, x9
	mov	sp, x8
	stur	x8, [x29, #-24]                 ; 8-byte Folded Spill
	ldur	w1, [x29, #-8]
	mov	w0, #10
	stur	w0, [x29, #-16]                 ; 4-byte Folded Spill
	bl	_pow
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	str	w0, [x8]
	ldur	w0, [x29, #-4]
	ldr	w1, [x8]
	bl	_mod
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	ldur	w9, [x29, #-16]                 ; 4-byte Folded Reload
	stur	w0, [x29, #-12]                 ; 4-byte Folded Spill
	ldur	w0, [x29, #-4]
	ldr	w8, [x8]
	sdiv	w1, w8, w9
	bl	_mod
	ldur	x9, [x29, #-24]                 ; 8-byte Folded Reload
	ldur	w10, [x29, #-16]                ; 4-byte Folded Reload
	mov	x8, x0
	ldur	w0, [x29, #-12]                 ; 4-byte Folded Reload
	subs	w8, w0, w8
	ldr	w9, [x9]
	sdiv	w9, w9, w10
	sdiv	w0, w8, w9
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_mergedigits                    ; -- Begin function mergedigits
	.p2align	2
_mergedigits:                           ; @mergedigits
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	.cfi_def_cfa_offset 16
	mov	x29, sp
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	sub	sp, sp, #80
	stur	w0, [x29, #-4]
	b	LBB5_1
LBB5_1:                                 ; %L10
	mov	w8, #1
                                        ; kill: def $x8 killed $w8
	stur	x8, [x29, #-32]                 ; 8-byte Folded Spill
	lsl	x8, x8, #2
	add	x8, x8, #15
	and	x9, x8, #0xfffffffffffffff0
	mov	x8, sp
	subs	x8, x8, x9
	mov	sp, x8
	stur	x8, [x29, #-40]                 ; 8-byte Folded Spill
	ldur	w0, [x29, #-4]
	bl	_lennum
	ldur	x9, [x29, #-40]                 ; 8-byte Folded Reload
	ldur	x8, [x29, #-32]                 ; 8-byte Folded Reload
	str	w0, [x9]
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
	b	LBB5_2
LBB5_2:                                 ; %L34
	ldur	x8, [x29, #-40]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	subs	w8, w8, #1
	cset	w8, ne
	tbnz	w8, #0, LBB5_4
	b	LBB5_3
LBB5_3:                                 ; %L11
	ldur	w0, [x29, #-4]
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
LBB5_4:                                 ; %L32
                                        ; =>This Inner Loop Header: Depth=1
	ldur	x9, [x29, #-40]                 ; 8-byte Folded Reload
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	ldr	w9, [x9]
	subs	w8, w8, w9
	cset	w8, ge
	tbnz	w8, #0, LBB5_10
	b	LBB5_5
LBB5_5:                                 ; %L12
                                        ;   in Loop: Header=BB5_4 Depth=1
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	mov	w9, #1
                                        ; kill: def $x9 killed $w9
	stur	x9, [x29, #-72]                 ; 8-byte Folded Spill
	lsl	x9, x9, #2
	add	x9, x9, #15
	and	x10, x9, #0xfffffffffffffff0
	mov	x9, sp
	subs	x9, x9, x10
	mov	sp, x9
	stur	x9, [x29, #-56]                 ; 8-byte Folded Spill
	ldur	w0, [x29, #-4]
	ldr	w1, [x8]
	bl	_digitn
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	ldur	x9, [x29, #-72]                 ; 8-byte Folded Reload
	ldur	x10, [x29, #-56]                ; 8-byte Folded Reload
	str	w0, [x10]
	lsl	x9, x9, #2
	add	x9, x9, #15
	and	x10, x9, #0xfffffffffffffff0
	mov	x9, sp
	subs	x9, x9, x10
	mov	sp, x9
	stur	x9, [x29, #-64]                 ; 8-byte Folded Spill
	ldur	w0, [x29, #-4]
	ldr	w8, [x8]
	add	w1, w8, #1
	bl	_digitn
	ldur	x9, [x29, #-72]                 ; 8-byte Folded Reload
	ldur	x8, [x29, #-64]                 ; 8-byte Folded Reload
	ldur	x10, [x29, #-56]                ; 8-byte Folded Reload
	str	w0, [x8]
	lsl	x9, x9, #2
	add	x9, x9, #15
	and	x11, x9, #0xfffffffffffffff0
	mov	x9, sp
	subs	x9, x9, x11
	mov	sp, x9
	stur	x9, [x29, #-48]                 ; 8-byte Folded Spill
	ldr	w8, [x8]
	ldr	w10, [x10]
	add	w8, w8, w10
	str	w8, [x9]
	b	LBB5_6
LBB5_6:                                 ; %L33
                                        ;   in Loop: Header=BB5_4 Depth=1
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	subs	w8, w8, #1
	cset	w8, ne
	tbnz	w8, #0, LBB5_8
	b	LBB5_7
LBB5_7:                                 ; %L13
                                        ;   in Loop: Header=BB5_4 Depth=1
	ldur	x9, [x29, #-16]                 ; 8-byte Folded Reload
	ldur	x8, [x29, #-48]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	str	w8, [x9]
	b	LBB5_9
LBB5_8:                                 ; %L14
                                        ;   in Loop: Header=BB5_4 Depth=1
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	ldur	x9, [x29, #-48]                 ; 8-byte Folded Reload
	ldr	w0, [x9]
	ldr	w1, [x8]
	bl	_concat
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	str	w0, [x8]
	b	LBB5_9
LBB5_9:                                 ; %L15
                                        ;   in Loop: Header=BB5_4 Depth=1
	ldur	x9, [x29, #-24]                 ; 8-byte Folded Reload
	ldr	w8, [x9]
	add	w8, w8, #1
	str	w8, [x9]
	b	LBB5_4
LBB5_10:                                ; %L16
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	ldr	w0, [x8]
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_mergeloop                      ; -- Begin function mergeloop
	.p2align	2
_mergeloop:                             ; @mergeloop
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	.cfi_def_cfa_offset 16
	mov	x29, sp
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	sub	sp, sp, #48
	stur	w0, [x29, #-4]
	b	LBB6_1
LBB6_1:                                 ; %L39
	ldur	w8, [x29, #-4]
	subs	w8, w8, #0
	cset	w8, ge
	tbnz	w8, #0, LBB6_3
	b	LBB6_2
LBB6_2:                                 ; %L17
	mov	w0, #-1
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
LBB6_3:                                 ; %L18
	mov	w8, #1
                                        ; kill: def $x8 killed $w8
	lsl	x9, x8, #2
	add	x9, x9, #15
	and	x10, x9, #0xfffffffffffffff0
	mov	x9, sp
	subs	x9, x9, x10
	mov	sp, x9
	stur	x9, [x29, #-32]                 ; 8-byte Folded Spill
	str	wzr, [x9]
	lsl	x9, x8, #2
	add	x9, x9, #15
	and	x10, x9, #0xfffffffffffffff0
	mov	x9, sp
	subs	x9, x9, x10
	mov	sp, x9
	stur	x9, [x29, #-24]                 ; 8-byte Folded Spill
	str	wzr, [x9]
	lsl	x8, x8, #2
	add	x8, x8, #15
	and	x9, x8, #0xfffffffffffffff0
	mov	x8, sp
	subs	x8, x8, x9
	mov	sp, x8
	stur	x8, [x29, #-16]                 ; 8-byte Folded Spill
	str	wzr, [x8]
	b	LBB6_4
LBB6_4:                                 ; %L35
                                        ; =>This Inner Loop Header: Depth=1
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	subs	w8, w8, #0
	cset	w8, ne
	tbnz	w8, #0, LBB6_14
	b	LBB6_5
LBB6_5:                                 ; %L19
                                        ;   in Loop: Header=BB6_4 Depth=1
	ldur	w0, [x29, #-4]
	bl	__print_int
	ldur	x9, [x29, #-32]                 ; 8-byte Folded Reload
	ldur	w8, [x29, #-4]
	str	w8, [x9]
	ldur	w0, [x29, #-4]
	bl	_mergedigits
	ldur	x9, [x29, #-16]                 ; 8-byte Folded Reload
	stur	w0, [x29, #-4]
	ldr	w8, [x9]
	add	w8, w8, #1
	str	w8, [x9]
	b	LBB6_6
LBB6_6:                                 ; %L36
                                        ;   in Loop: Header=BB6_4 Depth=1
	ldur	x8, [x29, #-32]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	ldur	w9, [x29, #-4]
	subs	w8, w8, w9
	cset	w8, ne
	tbnz	w8, #0, LBB6_8
	b	LBB6_7
LBB6_7:                                 ; %L20
                                        ;   in Loop: Header=BB6_4 Depth=1
	ldur	x9, [x29, #-24]                 ; 8-byte Folded Reload
	mov	w8, #1
	str	w8, [x9]
	b	LBB6_4
LBB6_8:                                 ; %L21
                                        ;   in Loop: Header=BB6_4 Depth=1
	mov	w8, #1
                                        ; kill: def $x8 killed $w8
	lsl	x8, x8, #2
	add	x8, x8, #15
	and	x9, x8, #0xfffffffffffffff0
	mov	x8, sp
	subs	x8, x8, x9
	mov	sp, x8
	stur	x8, [x29, #-40]                 ; 8-byte Folded Spill
	ldur	w0, [x29, #-4]
	bl	_lennum
	ldur	x8, [x29, #-40]                 ; 8-byte Folded Reload
	str	w0, [x8]
	b	LBB6_9
LBB6_9:                                 ; %L37
                                        ;   in Loop: Header=BB6_4 Depth=1
	ldur	x8, [x29, #-40]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	subs	w8, w8, #8
	cset	w8, lt
	tbnz	w8, #0, LBB6_11
	b	LBB6_10
LBB6_10:                                ; %L22
                                        ;   in Loop: Header=BB6_4 Depth=1
	ldur	x9, [x29, #-24]                 ; 8-byte Folded Reload
	mov	w8, #2
	str	w8, [x9]
	b	LBB6_4
LBB6_11:                                ; %L38
                                        ;   in Loop: Header=BB6_4 Depth=1
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	ldr	w8, [x8]
	subs	w8, w8, #20
	cset	w8, le
	tbnz	w8, #0, LBB6_13
	b	LBB6_12
LBB6_12:                                ; %L23
                                        ;   in Loop: Header=BB6_4 Depth=1
	ldur	x9, [x29, #-24]                 ; 8-byte Folded Reload
	mov	w8, #3
	str	w8, [x9]
	b	LBB6_4
LBB6_13:                                ; %L24
                                        ;   in Loop: Header=BB6_4 Depth=1
	ldur	x8, [x29, #-24]                 ; 8-byte Folded Reload
	str	wzr, [x8]
	b	LBB6_4
LBB6_14:                                ; %L25
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
	mov	x29, sp
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	sub	sp, sp, #48
	b	LBB7_1
LBB7_1:                                 ; %L26
	adrp	x8, _runtests@PAGE
	str	wzr, [x8, _runtests@PAGEOFF]
	b	LBB7_2
LBB7_2:                                 ; %L40
	adrp	x8, _runtests@PAGE
	ldr	w8, [x8, _runtests@PAGEOFF]
	subs	w8, w8, #0
	cset	w8, eq
	tbnz	w8, #0, LBB7_4
	b	LBB7_3
LBB7_3:                                 ; %L27
	mov	w0, #2
	mov	w1, #5
	stur	w1, [x29, #-20]                 ; 4-byte Folded Spill
	bl	_pow
	bl	__print_int
	mov	w0, #3
	stur	w0, [x29, #-40]                 ; 4-byte Folded Spill
	mov	w1, #1
	stur	w1, [x29, #-36]                 ; 4-byte Folded Spill
	bl	_pow
	bl	__print_int
	ldur	w1, [x29, #-40]                 ; 4-byte Folded Reload
	mov	w0, #13
	bl	_mod
	bl	__print_int
	mov	w0, #12
	mov	w1, #345
	bl	_concat
	bl	__print_int
	mov	w0, #9
	bl	_lennum
	bl	__print_int
	mov	w0, #10
	bl	_lennum
	bl	__print_int
	mov	w8, #1
                                        ; kill: def $x8 killed $w8
	stur	x8, [x29, #-16]                 ; 8-byte Folded Spill
	lsl	x8, x8, #2
	add	x8, x8, #15
	and	x9, x8, #0xfffffffffffffff0
	mov	x8, sp
	subs	x8, x8, x9
	mov	sp, x8
	stur	x8, [x29, #-32]                 ; 8-byte Folded Spill
	mov	w0, #57920
	movk	w0, #1, lsl #16
	str	w0, [x8]
	bl	__print_int
	ldur	x8, [x29, #-32]                 ; 8-byte Folded Reload
	ldr	w0, [x8]
	bl	_lennum
	bl	__print_int
	ldur	w1, [x29, #-36]                 ; 4-byte Folded Reload
	ldur	x8, [x29, #-32]                 ; 8-byte Folded Reload
	ldr	w0, [x8]
	bl	_digitn
	bl	__print_int
	ldur	x8, [x29, #-32]                 ; 8-byte Folded Reload
	ldur	w1, [x29, #-20]                 ; 4-byte Folded Reload
	ldr	w0, [x8]
	bl	_digitn
	bl	__print_int
	ldur	x8, [x29, #-16]                 ; 8-byte Folded Reload
	lsl	x8, x8, #2
	add	x8, x8, #15
	and	x9, x8, #0xfffffffffffffff0
	mov	x8, sp
	subs	x8, x8, x9
	mov	sp, x8
	stur	x8, [x29, #-8]                  ; 8-byte Folded Spill
	mov	w9, #4396
	str	w9, [x8]
	ldr	w0, [x8]
	bl	__print_int
	ldur	x8, [x29, #-8]                  ; 8-byte Folded Reload
	ldr	w0, [x8]
	bl	_mergedigits
	bl	__print_int
	mov	w0, #7
	bl	_mergedigits
	bl	__print_int
	b	LBB7_5
LBB7_4:                                 ; %L28
	mov	w0, #1467
	bl	_mergeloop
	bl	__print_int
	mov	w0, #1792
	bl	_mergeloop
	bl	__print_int
	mov	w0, #1537
	bl	_mergeloop
	bl	__print_int
	b	LBB7_5
LBB7_5:                                 ; %L29
	mov	w0, #0
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_runtests                       ; @runtests
.zerofill __DATA,__common,_runtests,4,2
.subsections_via_symbols
