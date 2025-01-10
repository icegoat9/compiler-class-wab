	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:                                ; %entry
	sub	sp, sp, #32
	.cfi_def_cfa_offset 32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	b	LBB0_1
LBB0_1:                                 ; %L1
	adrp	x9, _x@PAGE
	mov	w8, #1
	str	w8, [x9, _x@PAGEOFF]
	b	LBB0_2
LBB0_2:                                 ; %L4
                                        ; =>This Inner Loop Header: Depth=1
	adrp	x8, _x@PAGE
	ldr	w8, [x8, _x@PAGEOFF]
	subs	w8, w8, #10
	cset	w8, gt
	tbnz	w8, #0, LBB0_4
	b	LBB0_3
LBB0_3:                                 ; %L2
                                        ;   in Loop: Header=BB0_2 Depth=1
	adrp	x8, _x@PAGE
	str	x8, [sp, #8]                    ; 8-byte Folded Spill
	ldr	w0, [x8, _x@PAGEOFF]
	bl	__print_int
	ldr	x9, [sp, #8]                    ; 8-byte Folded Reload
	ldr	w8, [x9, _x@PAGEOFF]
	add	w8, w8, #1
	str	w8, [x9, _x@PAGEOFF]
	b	LBB0_2
LBB0_4:                                 ; %L3
	mov	w0, #0
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_x                              ; @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
