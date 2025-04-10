	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0
	.globl	_setx                           ; -- Begin function setx
	.p2align	2
_setx:                                  ; @setx
	.cfi_startproc
; %bb.0:                                ; %entry
	sub	sp, sp, #16
	.cfi_def_cfa_offset 16
	str	w0, [sp, #12]
	b	LBB0_1
LBB0_1:                                 ; %L1
	ldr	w9, [sp, #12]
	adrp	x8, _x@PAGE
	str	w9, [x8, _x@PAGEOFF]
	ldr	w0, [x8, _x@PAGEOFF]
	add	sp, sp, #16
	ret
	.cfi_endproc
                                        ; -- End function
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
	b	LBB1_1
LBB1_1:                                 ; %L2
	adrp	x8, _x@PAGE
	str	x8, [sp, #8]                    ; 8-byte Folded Spill
	ldr	w0, [x8, _x@PAGEOFF]
	bl	__print_int
	mov	w0, #123
	bl	_setx
	bl	__print_int
	ldr	x8, [sp, #8]                    ; 8-byte Folded Reload
	ldr	w0, [x8, _x@PAGEOFF]
	bl	__print_int
	mov	w0, #0
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_x                              ; @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
