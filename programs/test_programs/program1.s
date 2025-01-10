	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:                                ; %entry
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	.cfi_def_cfa_offset 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	b	LBB0_1
LBB0_1:                                 ; %L1
	adrp	x8, _x@PAGE
	mov	w9, #10
	str	w9, [x8, _x@PAGEOFF]
	ldr	w9, [x8, _x@PAGEOFF]
	add	w9, w9, #1
	str	w9, [x8, _x@PAGEOFF]
	ldr	w8, [x8, _x@PAGEOFF]
	add	w0, w8, #1035
	bl	__print_int
	mov	w0, #0
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_x                              ; @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
