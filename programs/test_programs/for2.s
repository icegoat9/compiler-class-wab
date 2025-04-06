	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
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
	b	LBB0_1
LBB0_1:                                 ; %L1
	adrp	x9, _i@PAGE
	mov	w8, #1                          ; =0x1
	str	w8, [x9, _i@PAGEOFF]
	b	LBB0_2
LBB0_2:                                 ; %L4
                                        ; =>This Inner Loop Header: Depth=1
	adrp	x8, _i@PAGE
	ldr	w8, [x8, _i@PAGEOFF]
	subs	w8, w8, #10
	cset	w8, gt
	tbnz	w8, #0, LBB0_4
	b	LBB0_3
LBB0_3:                                 ; %L2
                                        ;   in Loop: Header=BB0_2 Depth=1
	adrp	x9, _i@PAGE
	str	x9, [sp, #8]                    ; 8-byte Folded Spill
	ldr	w8, [x9, _i@PAGEOFF]
	ldr	w9, [x9, _i@PAGEOFF]
	mul	w0, w8, w9
	bl	__print_int
	ldr	x9, [sp, #8]                    ; 8-byte Folded Reload
	ldr	w8, [x9, _i@PAGEOFF]
	add	w8, w8, #1
	str	w8, [x9, _i@PAGEOFF]
	b	LBB0_2
LBB0_4:                                 ; %L3
	mov	w0, #0                          ; =0x0
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_i                              ; @i
.zerofill __DATA,__common,_i,4,2
.subsections_via_symbols
