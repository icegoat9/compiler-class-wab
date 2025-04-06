	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	mov	x29, sp
	sub	sp, sp, #16
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	b	LBB0_1
LBB0_1:                                 ; %L1
	adrp	x9, _i@PAGE
	mov	w8, #1                          ; =0x1
	str	w8, [x9, _i@PAGEOFF]
	b	LBB0_2
LBB0_2:                                 ; %L8
                                        ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB0_7 Depth 2
	adrp	x8, _i@PAGE
	ldr	w8, [x8, _i@PAGEOFF]
	subs	w8, w8, #9
	cset	w8, gt
	tbnz	w8, #0, LBB0_11
	b	LBB0_3
LBB0_3:                                 ; %L9
                                        ;   in Loop: Header=BB0_2 Depth=1
	adrp	x8, _i@PAGE
	ldr	w8, [x8, _i@PAGEOFF]
	subs	w8, w8, #3
	cset	w8, gt
	tbnz	w8, #0, LBB0_5
	b	LBB0_4
LBB0_4:                                 ; %L2
                                        ;   in Loop: Header=BB0_2 Depth=1
	adrp	x8, _i@PAGE
	ldr	w0, [x8, _i@PAGEOFF]
	bl	__print_int
	b	LBB0_10
LBB0_5:                                 ; %L10
                                        ;   in Loop: Header=BB0_2 Depth=1
	adrp	x8, _i@PAGE
	ldr	w8, [x8, _i@PAGEOFF]
	subs	w8, w8, #6
	cset	w8, gt
	tbnz	w8, #0, LBB0_9
	b	LBB0_6
LBB0_6:                                 ; %L3
                                        ;   in Loop: Header=BB0_2 Depth=1
	mov	w8, #1                          ; =0x1
	mov	w9, #1                          ; =0x1
                                        ; kill: def $x9 killed $w9
	lsl	x9, x9, #2
	add	x9, x9, #15
	and	x10, x9, #0xfffffffffffffff0
	mov	x9, sp
	subs	x9, x9, x10
	mov	sp, x9
	stur	x9, [x29, #-8]                  ; 8-byte Folded Spill
	str	w8, [x9]
	b	LBB0_7
LBB0_7:                                 ; %L11
                                        ;   Parent Loop BB0_2 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	ldur	x8, [x29, #-8]                  ; 8-byte Folded Reload
	ldr	w8, [x8]
	subs	w8, w8, #3
	cset	w8, gt
	tbnz	w8, #0, LBB0_10
	b	LBB0_8
LBB0_8:                                 ; %L4
                                        ;   in Loop: Header=BB0_7 Depth=2
	ldur	x9, [x29, #-8]                  ; 8-byte Folded Reload
	adrp	x8, _i@PAGE
	ldr	w10, [x8, _i@PAGEOFF]
	mov	w8, #10                         ; =0xa
	mul	w8, w8, w10
	ldr	w9, [x9]
	add	w0, w8, w9
	bl	__print_int
	ldur	x9, [x29, #-8]                  ; 8-byte Folded Reload
	ldr	w8, [x9]
	add	w8, w8, #1
	str	w8, [x9]
	b	LBB0_7
LBB0_9:                                 ; %L5
                                        ;   in Loop: Header=BB0_2 Depth=1
	adrp	x8, _i@PAGE
	ldr	w9, [x8, _i@PAGEOFF]
	mov	w8, #100                        ; =0x64
	mul	w0, w8, w9
	bl	__print_int
	b	LBB0_10
LBB0_10:                                ; %L6
                                        ;   in Loop: Header=BB0_2 Depth=1
	adrp	x9, _i@PAGE
	ldr	w8, [x9, _i@PAGEOFF]
	add	w8, w8, #1
	str	w8, [x9, _i@PAGEOFF]
	b	LBB0_2
LBB0_11:                                ; %L7
	mov	w0, #0                          ; =0x0
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_i                              ; @i
.zerofill __DATA,__common,_i,4,2
.subsections_via_symbols
