	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:                                ; %entry
	sub	sp, sp, #48
	.cfi_def_cfa_offset 48
	stp	x29, x30, [sp, #32]             ; 16-byte Folded Spill
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	b	LBB0_1
LBB0_1:                                 ; %L1
	adrp	x8, _x@PAGE
	str	x8, [sp, #8]                    ; 8-byte Folded Spill
	mov	w9, #5
	str	w9, [x8, _x@PAGEOFF]
	adrp	x10, _y@PAGE
	str	x10, [sp, #16]                  ; 8-byte Folded Spill
	mov	w9, #3
	str	w9, [x10, _y@PAGEOFF]
	ldr	w0, [x8, _x@PAGEOFF]
	bl	__print_int
	ldr	x8, [sp, #16]                   ; 8-byte Folded Reload
	ldr	w0, [x8, _y@PAGEOFF]
	bl	__print_int
	ldr	x8, [sp, #8]                    ; 8-byte Folded Reload
	ldr	x9, [sp, #16]                   ; 8-byte Folded Reload
	ldr	w8, [x8, _x@PAGEOFF]
	ldr	w9, [x9, _y@PAGEOFF]
	sdiv	w0, w8, w9
	bl	__print_int
	ldr	x8, [sp, #8]                    ; 8-byte Folded Reload
	ldr	x9, [sp, #16]                   ; 8-byte Folded Reload
	ldr	w8, [x8, _x@PAGEOFF]
	ldr	w10, [x9, _y@PAGEOFF]
	sdiv	w9, w8, w10
	mul	w9, w9, w10
	subs	w0, w8, w9
	bl	__print_int
	ldr	x8, [sp, #8]                    ; 8-byte Folded Reload
	ldr	x9, [sp, #16]                   ; 8-byte Folded Reload
	ldr	w10, [x8, _x@PAGEOFF]
	mov	w8, #0
	str	w8, [sp, #28]                   ; 4-byte Folded Spill
	subs	w8, w8, w10
	ldr	w9, [x9, _y@PAGEOFF]
	sdiv	w0, w8, w9
	bl	__print_int
	ldr	x10, [sp, #8]                   ; 8-byte Folded Reload
	ldr	x9, [sp, #16]                   ; 8-byte Folded Reload
	ldr	w8, [sp, #28]                   ; 4-byte Folded Reload
	ldr	w10, [x10, _x@PAGEOFF]
	subs	w8, w8, w10
	ldr	w10, [x9, _y@PAGEOFF]
	sdiv	w9, w8, w10
	mul	w9, w9, w10
	subs	w0, w8, w9
	bl	__print_int
	ldr	x8, [sp, #8]                    ; 8-byte Folded Reload
	ldr	x10, [sp, #16]                  ; 8-byte Folded Reload
	ldr	w9, [sp, #28]                   ; 4-byte Folded Reload
	ldr	w8, [x8, _x@PAGEOFF]
	ldr	w10, [x10, _y@PAGEOFF]
	subs	w9, w9, w10
	sdiv	w0, w8, w9
	bl	__print_int
	ldr	x8, [sp, #8]                    ; 8-byte Folded Reload
	ldr	x9, [sp, #16]                   ; 8-byte Folded Reload
	ldr	w10, [sp, #28]                  ; 4-byte Folded Reload
	ldr	w8, [x8, _x@PAGEOFF]
	subs	w8, w10, w8
	ldr	w9, [x9, _y@PAGEOFF]
	subs	w10, w10, w9
	sdiv	w10, w8, w10
	mneg	w9, w9, w10
	subs	w0, w8, w9
	bl	__print_int
	ldr	x8, [sp, #8]                    ; 8-byte Folded Reload
	ldr	x9, [sp, #16]                   ; 8-byte Folded Reload
	ldr	w10, [sp, #28]                  ; 4-byte Folded Reload
	ldr	w8, [x8, _x@PAGEOFF]
	subs	w8, w10, w8
	ldr	w9, [x9, _y@PAGEOFF]
	subs	w10, w10, w9
	sdiv	w10, w8, w10
	mneg	w9, w9, w10
	subs	w0, w8, w9
	bl	__print_int
	ldr	w0, [sp, #28]                   ; 4-byte Folded Reload
	ldp	x29, x30, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #48
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_x                              ; @x
.zerofill __DATA,__common,_x,4,2
	.globl	_y                              ; @y
.zerofill __DATA,__common,_y,4,2
.subsections_via_symbols
