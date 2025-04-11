	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0
	.globl	_printn                         ; -- Begin function printn
	.p2align	2
_printn:                                ; @printn
	.cfi_startproc
; %bb.0:                                ; %entry
	sub	sp, sp, #32
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	.cfi_def_cfa_offset 32
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	str	w0, [sp, #12]
	b	LBB0_1
LBB0_1:                                 ; %L1
	adrp	x0, l_.str.1@PAGE
	add	x0, x0, l_.str.1@PAGEOFF
	bl	_printf
	ldr	w0, [sp, #12]
	bl	__print_int
	b	LBB0_2
LBB0_2:                                 ; %L6
	ldr	w8, [sp, #12]
	subs	w8, w8, #100
	cset	w8, le
	tbnz	w8, #0, LBB0_4
	b	LBB0_3
LBB0_3:                                 ; %L2
	adrp	x0, l_.str.2@PAGE
	add	x0, x0, l_.str.2@PAGEOFF
	bl	_printf
	b	LBB0_5
LBB0_4:                                 ; %L3
	mov	w0, #-1                         ; =0xffffffff
	bl	__print_int
	b	LBB0_5
LBB0_5:                                 ; %L4
	mov	w0, #0                          ; =0x0
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
	stp	x29, x30, [sp, #16]             ; 16-byte Folded Spill
	.cfi_def_cfa_offset 32
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	b	LBB1_1
LBB1_1:                                 ; %L5
	adrp	x9, _x@PAGE
	str	x9, [sp, #8]                    ; 8-byte Folded Spill
	mov	w8, #7                          ; =0x7
	str	w8, [x9, _x@PAGEOFF]
	adrp	x0, l_.str.3@PAGE
	add	x0, x0, l_.str.3@PAGEOFF
	bl	_printf
	ldr	x8, [sp, #8]                    ; 8-byte Folded Reload
	ldr	w0, [x8, _x@PAGEOFF]
	bl	_printn
	mov	w0, #200                        ; =0xc8
	bl	_printn
	mov	w0, #0                          ; =0x0
	ldp	x29, x30, [sp, #16]             ; 16-byte Folded Reload
	add	sp, sp, #32
	ret
	.cfi_endproc
                                        ; -- End function
	.section	__TEXT,__cstring,cstring_literals
	.p2align	4, 0x0                          ; @.str.1
l_.str.1:
	.asciz	"function printn():\n"

l_.str.2:                               ; @.str.2
	.asciz	"quite large!\n"

l_.str.3:                               ; @.str.3
	.asciz	"hello, world.\n"

	.globl	_x                              ; @x
.zerofill __DATA,__common,_x,4,2
.subsections_via_symbols
