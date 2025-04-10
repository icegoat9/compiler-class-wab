	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0
	.globl	_printval                       ; -- Begin function printval
	.p2align	2
_printval:                              ; @printval
	.cfi_startproc
; %bb.0:                                ; %entry
	sub	sp, sp, #32
	.cfi_def_cfa_offset 32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	str	w0, [sp, #12]
	b	LBB0_1
LBB0_1:                                 ; %L1
	ldr	w0, [sp, #12]
	bl	__print_int
	ldr	w0, [sp, #12]
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
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
	adrp	x8, _y@PAGE
	str	x8, [sp]                        ; 8-byte Folded Spill
	mov	w9, #0
	str	w9, [sp, #12]                   ; 4-byte Folded Spill
	str	wzr, [x8, _y@PAGEOFF]
	mov	w0, #2
	bl	_printval
	ldr	x8, [sp]                        ; 8-byte Folded Reload
	str	w0, [x8, _y@PAGEOFF]
	mov	w0, #5
	bl	_printval
	ldr	x8, [sp]                        ; 8-byte Folded Reload
	ldr	w8, [x8, _y@PAGEOFF]
	add	w0, w8, #10
	bl	_printval
	ldr	w0, [sp, #12]                   ; 4-byte Folded Reload
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_y                              ; @y
.zerofill __DATA,__common,_y,4,2
.subsections_via_symbols
