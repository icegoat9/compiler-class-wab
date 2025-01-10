													;;; double-semicolon (;;) comments used to document what I believe is happening from some reading/searching
	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0	sdk_version 14, 2
	.globl	_square                         ; -- Begin function square
	.p2align	2
_square:                                ; @square
	.cfi_startproc
; %bb.0:									
	sub	sp, sp, #16					;; sp (stack pointer) -= 16, to a new unused memory location (if stack starts at high memory and expands toward low memory?)
	.cfi_def_cfa_offset 16  ;; ??
	str	w0, [sp, #12]				;; store value of reg w0 (the argument passed to this function) onto stack, at address sp+12 (4 bytes below previous top of stack)
													;;   basic question: why we moved the stack pointer by 16 rather than just by 4 if we're only using this one location on the stack
	ldr	w8, [sp, #12]				;; load value from address at sp+12 into w8 (i.e. w8 = w0)
	ldr	w9, [sp, #12]				;; similarly, w9 = w0
	mul	w0, w8, w9					;; w0 = w8*w9 (i.e. the original w0^2)
	add	sp, sp, #16					;; stack pointer += 16 (restore it to where it was before the function call)
	ret											;; return from function call. w0 now holds the squared value
	.cfi_endproc
                                        ; -- End function
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:
	mov w7, #0													;; (manually added): initialize w7 to 0, to use to accumulate sum of squares values
																			;; unclear if initialization is needed. also unclear which registers are available for general use
	sub	sp, sp, #48
	.cfi_def_cfa_offset 48
	stp	x29, x30, [sp, #32]             ; 16-byte Folded Spill
	add	x29, sp, #32
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	wzr, [x29, #-4]
	stur	w0, [x29, #-8]
	str	x1, [sp, #16]
	ldur	w8, [x29, #-8]
	subs	w8, w8, #2
	cset	w8, eq
	tbnz	w8, #0, LBB1_2
	b	LBB1_1
LBB1_1:
	ldr	x8, [sp, #16]
	ldr	x8, [x8]
	mov	x9, sp
	str	x8, [x9]
	adrp	x0, l_.str@PAGE
	add	x0, x0, l_.str@PAGEOFF
	bl	_printf
	mov	w8, #-1
	stur	w8, [x29, #-4]
	b	LBB1_7
LBB1_2:
	ldr	x8, [sp, #16]
	ldr	x0, [x8, #8]
	bl	_atoi
	str	w0, [sp, #8]
	str	wzr, [sp, #12]
	b	LBB1_3
LBB1_3:                                 ; =>This Inner Loop Header: Depth=1
																				;; generally, this block of code is checking if the loop has run the expected number of times
																				;;  and we can exit even if I don't understand it fully
	ldr	w8, [sp, #12]											;; w8 = sp + 12? (is this overall loop counter, but how would we know it's at this address?)
	ldr	w9, [sp, #8]											;; w9 = sp + 8? (is this the loop increment i.e. 1, but how would we know it's at this address?)
	subs	w8, w8, w9											;; w8 -= w9 (is this decrementing a loop counter?), unclear why subs and not sub
																				;;  but I documented LBB1_5 code below as incrementing a loop counter, they can't both be doing that...
	cset	w8, ge													;; set w8=1 if something (perhaps w8 itself?) >=0? does this also set w8=0 if that's not the case?
																				;; general intent of above line is to set a flag if we've iterated through the loop the right number of times to exit
	tbnz	w8, #0, LBB1_6									;; test and branch if nonzero: if w8 is 0 (meaning cset didn't fire and looping is done), jump out of for loop to LBB1+6
	b	LBB1_4															;; otherwise, branch/jump ahead (continue loop)
LBB1_4:                                 ;   in Loop: Header=BB1_3 Depth=1
	ldr	w0, [sp, #12]											;; load value from stack into reg w0 (w0 is special reg: will be argument to function call _square)
	bl	_square														;; call function
	mov	x9, sp														;; x9 = sp
                                        ; implicit-def: $x8
	mov	x8, x0														;; x8 = x0 (x0 is special reg: holds the output of the _square function call)
;;	add	x8, x8, #1												;; (manually added) (DEBUG): add 1 to x8 to see if that affects the value printed
	str	x8, [x9]													;; store value of x8 (i.e. x0) to address x9 (onto the stack)
	add x7, x7, x0												;; (manually added): use reg x7 to accumulate sum of square() outputs -- hopefully x7 isn't reserved for something else...
	adrp	x0, l_.str.1@PAGE								;; set x0 = address of some string in the code (perhaps the string passed to printf)-- how would we look that up?
	add	x0, x0, l_.str.1@PAGEOFF					;; don't quite understand... x0 += some page offset? seems like end result is x0 holds the address of the printf string parameter?
	bl	_printf														;; call printf() function (uses x0 as a parameter: address to string to print)
																				;; Q: how does output of square command get passed to printf? 
																				;;    it appears x9 is a special purpose register that holds an address printf() automatically pulls value from?
																				;;    in this case x9 points to a location on the stack that holds this former x0 (output of square() function)
	b	LBB1_5															;; branch (jump?) to LBB1_5
LBB1_5:                                 ;   in Loop: Header=BB1_3 Depth=1
	ldr	w8, [sp, #12]											;; load value from stack (is this the for loop counter)
	add	w8, w8, #1												;; w8 += 1
	str	w8, [sp, #12]											;; store back to stack
	b	LBB1_3															;; jump to LBB1_3
LBB1_6:
	;; (manually added): multiple lines of print code added here, extracted from above
	mov	x9, sp														;; x9 = current stack pointer
	str x7, [x9]													;; store sum-of-squares accumulated value to address x9 (i.e. onto stack), for printf to pick up
	adrp	x0, l_.str.1@PAGE								;; set x0 = address of some string in the code (perhaps the result string in the loop?)
	add	x0, x0, l_.str.1@PAGEOFF					;; x0 += some page offset (?), end result is x0 holds the address of the printf string parameter?
	bl	_printf														;; call printf() function (with x0 as a parameter, address to string), presumably x9 as well
	;; (manually added): end new print code
	stur	wzr, [x29, #-4]
	b	LBB1_7
LBB1_7:
	ldur	w0, [x29, #-4]
	ldp	x29, x30, [sp, #32]             ; 16-byte Folded Reload
	add	sp, sp, #48
	ret
	.cfi_endproc
                                        ; -- End function
	.section	__TEXT,__cstring,cstring_literals
l_.str:                                 ; @.str
	.asciz	"Usage: %s n\n"

l_.str.1:                               ; @.str.1
	.asciz	"%d\n"

.subsections_via_symbols
