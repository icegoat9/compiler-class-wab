# Compiler Passes via Example

The exact details of this will evolve over time as I modify the compiler, but to complement the bullet-point list of compiler steps in the [README](/README.md) and the details in the code, here's one simple program taken through each compiler pass:

## Source code (programs/test_programs/fact_for.wb):
```
/// factorial example
func fact(n) {
    var result=1;
    for x=1,n {
        result=result*x;
    }
    return result;
}

for x=1,9 {
    print fact(x);
}

```
## Tokenized:
```
[Token(toktype='FUNC', tokvalue='func', sourceline=4, sourcecol=4),
 Token(toktype='NAME', tokvalue='fact', sourceline=4, sourcecol=9),
 Token(toktype='LPAREN', tokvalue='(', sourceline=4, sourcecol=10),
 Token(toktype='NAME', tokvalue='n', sourceline=4, sourcecol=11),
 Token(toktype='RPAREN', tokvalue=')', sourceline=4, sourcecol=12),
 Token(toktype='LBRACE', tokvalue='{', sourceline=4, sourcecol=14),
 Token(toktype='VAR', tokvalue='var', sourceline=5, sourcecol=7),
 Token(toktype='NAME', tokvalue='result', sourceline=5, sourcecol=14),
 Token(toktype='ASSIGN', tokvalue='=', sourceline=5, sourcecol=16),
 Token(toktype='INTEGER', tokvalue='1', sourceline=5, sourcecol=18),
 Token(toktype='SEMI', tokvalue=';', sourceline=5, sourcecol=19),
 Token(toktype='FOR', tokvalue='for', sourceline=6, sourcecol=7),
 Token(toktype='NAME', tokvalue='x', sourceline=6, sourcecol=9),
 Token(toktype='ASSIGN', tokvalue='=', sourceline=6, sourcecol=11),
 Token(toktype='INTEGER', tokvalue='1', sourceline=6, sourcecol=13),
 Token(toktype='COMMA', tokvalue=',', sourceline=6, sourcecol=14),
 Token(toktype='NAME', tokvalue='n', sourceline=6, sourcecol=15),
 Token(toktype='LBRACE', tokvalue='{', sourceline=6, sourcecol=17),
 Token(toktype='NAME', tokvalue='result', sourceline=7, sourcecol=14),
 Token(toktype='ASSIGN', tokvalue='=', sourceline=7, sourcecol=16),
 Token(toktype='NAME', tokvalue='result', sourceline=7, sourcecol=23),
 Token(toktype='TIMES', tokvalue='*', sourceline=7, sourcecol=25),
 Token(toktype='NAME', tokvalue='x', sourceline=7, sourcecol=27),
 Token(toktype='SEMI', tokvalue=';', sourceline=7, sourcecol=28),
 Token(toktype='RBRACE', tokvalue='}', sourceline=8, sourcecol=5),
 Token(toktype='RETURN', tokvalue='return', sourceline=9, sourcecol=10),
 Token(toktype='NAME', tokvalue='result', sourceline=9, sourcecol=17),
 Token(toktype='SEMI', tokvalue=';', sourceline=9, sourcecol=18),
 Token(toktype='RBRACE', tokvalue='}', sourceline=10, sourcecol=1),
 Token(toktype='FOR', tokvalue='for', sourceline=12, sourcecol=3),
 Token(toktype='NAME', tokvalue='x', sourceline=12, sourcecol=5),
 Token(toktype='ASSIGN', tokvalue='=', sourceline=12, sourcecol=7),
 Token(toktype='INTEGER', tokvalue='1', sourceline=12, sourcecol=9),
 Token(toktype='COMMA', tokvalue=',', sourceline=12, sourcecol=10),
 Token(toktype='INTEGER', tokvalue='9', sourceline=12, sourcecol=11),
 Token(toktype='LBRACE', tokvalue='{', sourceline=12, sourcecol=13),
 Token(toktype='PRINT', tokvalue='print', sourceline=13, sourcecol=9),
 Token(toktype='NAME', tokvalue='fact', sourceline=13, sourcecol=14),
 Token(toktype='LPAREN', tokvalue='(', sourceline=13, sourcecol=15),
 Token(toktype='NAME', tokvalue='x', sourceline=13, sourcecol=16),
 Token(toktype='RPAREN', tokvalue=')', sourceline=13, sourcecol=17),
 Token(toktype='SEMI', tokvalue=';', sourceline=13, sourcecol=18),
 Token(toktype='RBRACE', tokvalue='}', sourceline=14, sourcecol=1)]
```
## Parsed into an AST (Abstract Syntax Tree):
```
Program(statements=[
  Function(name=Name(str='fact'), 
    params=[Name(str='n')], 
    statements=[
      DeclareValue(left=Name(str='result'), 
        right=Integer(n=1)), 
      For(name=Name(str='x'), 
        startval=Integer(n=1), 
        endval=Name(str='n'), 
        statements=[
          Assign(left=Name(str='result'), 
            right=Multiply(left=Name(str='result'), 
              right=Name(str='x')))]), 
          Return(value=Name(str='result'))]), 
  For(name=Name(str='x'), 
    startval=Integer(n=1), 
    endval=Integer(n=9), 
    statements=[
      Print(value=CallFn(name=Name(str='fact'), 
        params=[Name(str='x')]))])])
```

### Human Formatted Output

For steps beyond this point we'll display the AST run through a formatter to display a human-readable equivalent (the internal data structure each compiler pass acts remains in the above format).

Running the above AST through the formatter should give us code that looks like our input (other than commands and differences in whitespace, which the tokenizer ignored):

```
func fact(n) {
   var result = 1;
   for x = 1,n {
      result = result * x;
   }
   return result;
}

for x = 1,9 {
   print fact(x);
}
```

### if..elif..else rewrite

not relevant on this particular program.

### for loop rewrite:
```
func fact(n) {
   var result = 1;
   var x = 1;
   while x <= n {
      result = result * x;
      x = x + 1;
   }
   return result;
}

var x = 1;
while x <= 9 {
   print fact(x);
   x = x + 1;
}
```

### fold constants

pre-compute constant math: not relevant for this program.

### deinit

```
func fact(n) {
   var result;
   result = 1;
   var x;
   x = 1;
   while x <= n {
      result = result * x;
      x = x + 1;
   }
   return result;
}

var x;
x = 1;
while x <= 9 {
   print fact(x);
   x = x + 1;
}
```

### unscript
```
func fact(n) {
   var result;
   result = 1;
   var x;
   x = 1;
   while x <= n {
      result = result * x;
      x = x + 1;
   }
   return result;
}

var x;
func main() {
   x = 1;
   while x <= 9 {
      print fact(x);
      x = x + 1;
   }
}
```

### resolve scope
```
func fact(n) {
   local result;
   local[result] = 1;
   local x;
   local[x] = 1;
   while local[x] <= local[n] {
      local[result] = local[result] * local[x];
      local[x] = local[x] + 1;
   }
   return local[result];
}

global x;
func main() {
   global[x] = 1;
   while global[x] <= 9 {
      print fact(global[x]);
      global[x] = global[x] + 1;
   }
}
```

### defaultreturns
```
func fact(n) {
   local result;
   local[result] = 1;
   local x;
   local[x] = 1;
   while local[x] <= local[n] {
      local[result] = local[result] * local[x];
      local[x] = local[x] + 1;
   }
   return local[result];
}

global x;
func main() {
   global[x] = 1;
   while global[x] <= 9 {
      print fact(global[x]);
      global[x] = global[x] + 1;
   }
   return 0;
}
```

### expr_instructions
```
func fact(n) {
   local result;
   local[result] = EXPR([PUSH(1)]);
   local x;
   local[x] = EXPR([PUSH(1)]);
   while EXPR([LOAD_LOCAL('x'), LOAD_LOCAL('n'), LTE()]) {
      local[result] = EXPR([LOAD_LOCAL('result'), LOAD_LOCAL('x'), MUL()]);
      local[x] = EXPR([LOAD_LOCAL('x'), PUSH(1), ADD()]);
   }
   return EXPR([LOAD_LOCAL('result')]);
}

global x;
func main() {
   global[x] = EXPR([PUSH(1)]);
   while EXPR([LOAD_GLOBAL('x'), PUSH(9), LTE()]) {
      print EXPR([LOAD_GLOBAL('x'), CALL('fact',1)]);
      global[x] = EXPR([LOAD_GLOBAL('x'), PUSH(1), ADD()]);
   }
   return EXPR([PUSH(0)]);
}
```

### statement_instructions
```
func fact(n) {
   STATEMENT([
      LOCAL('result')
   ])
   STATEMENT([
      PUSH(1)
      STORE_LOCAL('result')
   ])
   STATEMENT([
      LOCAL('x')
   ])
   STATEMENT([
      PUSH(1)
      STORE_LOCAL('x')
   ])
   while EXPR([LOAD_LOCAL('x'), LOAD_LOCAL('n'), LTE()]) {
      STATEMENT([
         LOAD_LOCAL('result')
         LOAD_LOCAL('x')
         MUL()
         STORE_LOCAL('result')
      ])
      STATEMENT([
         LOAD_LOCAL('x')
         PUSH(1)
         ADD()
         STORE_LOCAL('x')
      ])
   }
   STATEMENT([
      LOAD_LOCAL('result')
      RETURN()
   ])
}

global x;
func main() {
   STATEMENT([
      PUSH(1)
      STORE_GLOBAL('x')
   ])
   while EXPR([LOAD_GLOBAL('x'), PUSH(9), LTE()]) {
      STATEMENT([
         LOAD_GLOBAL('x')
         CALL('fact',1)
         PRINT()
      ])
      STATEMENT([
         LOAD_GLOBAL('x')
         PUSH(1)
         ADD()
         STORE_GLOBAL('x')
      ])
   }
   STATEMENT([
      PUSH(0)
      RETURN()
   ])
}
```
### block convert
```
func fact(n) {
   BLOCK(label='L1', [
      LOCAL('result')
      PUSH(1)
      STORE_LOCAL('result')
      LOCAL('x')
      PUSH(1)
      STORE_LOCAL('x')
   ])
   while EXPR([LOAD_LOCAL('x'), LOAD_LOCAL('n'), LTE()]) {
      BLOCK(label='L2', [
         LOAD_LOCAL('result')
         LOAD_LOCAL('x')
         MUL()
         STORE_LOCAL('result')
         LOAD_LOCAL('x')
         PUSH(1)
         ADD()
         STORE_LOCAL('x')
      ])
   }
   BLOCK(label='L3', [
      LOAD_LOCAL('result')
      RETURN()
   ])
}

global x;
func main() {
   BLOCK(label='L4', [
      PUSH(1)
      STORE_GLOBAL('x')
   ])
   while EXPR([LOAD_GLOBAL('x'), PUSH(9), LTE()]) {
      BLOCK(label='L5', [
         LOAD_GLOBAL('x')
         CALL('fact',1)
         PRINT()
         LOAD_GLOBAL('x')
         PUSH(1)
         ADD()
         STORE_GLOBAL('x')
      ])
   }
   BLOCK(label='L6', [
      PUSH(0)
      RETURN()
   ])
}
```
### block flow
```
func fact(n) {
   BLOCK(label='L1', [
      LOCAL('result')
      PUSH(1)
      STORE_LOCAL('result')
      LOCAL('x')
      PUSH(1)
      STORE_LOCAL('x')
      GOTO(label='L7')
   ])
   BLOCK(label='L7', [
      LOAD_LOCAL('x')
      LOAD_LOCAL('n')
      LTE()
      CBRANCH(iftrue='L2', iffalse='L3')
   ])
   BLOCK(label='L2', [
      LOAD_LOCAL('result')
      LOAD_LOCAL('x')
      MUL()
      STORE_LOCAL('result')
      LOAD_LOCAL('x')
      PUSH(1)
      ADD()
      STORE_LOCAL('x')
      GOTO(label='L7')
   ])
   BLOCK(label='L3', [
      LOAD_LOCAL('result')
      RETURN()
   ])
}

global x;
func main() {
   BLOCK(label='L4', [
      PUSH(1)
      STORE_GLOBAL('x')
      GOTO(label='L8')
   ])
   BLOCK(label='L8', [
      LOAD_GLOBAL('x')
      PUSH(9)
      LTE()
      CBRANCH(iftrue='L5', iffalse='L6')
   ])
   BLOCK(label='L5', [
      LOAD_GLOBAL('x')
      CALL('fact',1)
      PRINT()
      LOAD_GLOBAL('x')
      PUSH(1)
      ADD()
      STORE_GLOBAL('x')
      GOTO(label='L8')
   ])
   BLOCK(label='L6', [
      PUSH(0)
      RETURN()
   ])
}
```

### LLVM initial codegen
```
func fact(n) {
   BLOCK(label='L1', [
      LLVM '%result = alloca i32'
      LLVM 'store i32 1, i32* %result'
      LLVM '%x = alloca i32'
      LLVM 'store i32 1, i32* %x'
      LLVM 'br label %L7'
   ])
   BLOCK(label='L7', [
      LLVM '%.r1 = load i32, i32* %x'
      LLVM '%.r2 = load i32, i32* %n'
      LLVM '%.r3 = icmp sle i32 %.r1, %.r2'
      LLVM 'br i1 %.r3, label %L2, label %L3'
   ])
   BLOCK(label='L2', [
      LLVM '%.r4 = load i32, i32* %result'
      LLVM '%.r5 = load i32, i32* %x'
      LLVM '%.r6 = mul i32 %.r4, %.r5'
      LLVM 'store i32 %.r6, i32* %result'
      LLVM '%.r7 = load i32, i32* %x'
      LLVM '%.r8 = add i32 %.r7, 1'
      LLVM 'store i32 %.r8, i32* %x'
      LLVM 'br label %L7'
   ])
   BLOCK(label='L3', [
      LLVM '%.r9 = load i32, i32* %result'
      LLVM 'ret i32 %.r9'
   ])
}

global x;
func main() {
   BLOCK(label='L4', [
      LLVM 'store i32 1, i32* @x'
      LLVM 'br label %L8'
   ])
   BLOCK(label='L8', [
      LLVM '%.r10 = load i32, i32* @x'
      LLVM '%.r11 = icmp sle i32 %.r10, 9'
      LLVM 'br i1 %.r11, label %L5, label %L6'
   ])
   BLOCK(label='L5', [
      LLVM '%.r12 = load i32, i32* @x'
      LLVM '%.r13 = call i32 (i32) @fact(i32 %.r12)'
      LLVM 'call i32 (i32) @_print_int(i32 %.r13)'
      LLVM '%.r14 = load i32, i32* @x'
      LLVM '%.r15 = add i32 %.r14, 1'
      LLVM 'store i32 %.r15, i32* @x'
      LLVM 'br label %L8'
   ])
   BLOCK(label='L6', [
      LLVM 'ret i32 0'
   ])
}
```
### LLVM add function entry
```
func fact(.arg_n) {
   BLOCK(label='entry', [
      LLVM '%n = alloca i32'
      LLVM 'store i32 %.arg_n, i32* %n'
      LLVM 'br label %L1'
   ])
   BLOCK(label='L1', [
      LLVM '%result = alloca i32'
      LLVM 'store i32 1, i32* %result'
      LLVM '%x = alloca i32'
      LLVM 'store i32 1, i32* %x'
      LLVM 'br label %L7'
   ])
   BLOCK(label='L7', [
      LLVM '%.r1 = load i32, i32* %x'
      LLVM '%.r2 = load i32, i32* %n'
      LLVM '%.r3 = icmp sle i32 %.r1, %.r2'
      LLVM 'br i1 %.r3, label %L2, label %L3'
   ])
   BLOCK(label='L2', [
      LLVM '%.r4 = load i32, i32* %result'
      LLVM '%.r5 = load i32, i32* %x'
      LLVM '%.r6 = mul i32 %.r4, %.r5'
      LLVM 'store i32 %.r6, i32* %result'
      LLVM '%.r7 = load i32, i32* %x'
      LLVM '%.r8 = add i32 %.r7, 1'
      LLVM 'store i32 %.r8, i32* %x'
      LLVM 'br label %L7'
   ])
   BLOCK(label='L3', [
      LLVM '%.r9 = load i32, i32* %result'
      LLVM 'ret i32 %.r9'
   ])
}

global x;
func main() {
   BLOCK(label='entry', [
      LLVM 'br label %L4'
   ])
   BLOCK(label='L4', [
      LLVM 'store i32 1, i32* @x'
      LLVM 'br label %L8'
   ])
   BLOCK(label='L8', [
      LLVM '%.r10 = load i32, i32* @x'
      LLVM '%.r11 = icmp sle i32 %.r10, 9'
      LLVM 'br i1 %.r11, label %L5, label %L6'
   ])
   BLOCK(label='L5', [
      LLVM '%.r12 = load i32, i32* @x'
      LLVM '%.r13 = call i32 (i32) @fact(i32 %.r12)'
      LLVM 'call i32 (i32) @_print_int(i32 %.r13)'
      LLVM '%.r14 = load i32, i32* @x'
      LLVM '%.r15 = add i32 %.r14, 1'
      LLVM 'store i32 %.r15, i32* @x'
      LLVM 'br label %L8'
   ])
   BLOCK(label='L6', [
      LLVM 'ret i32 0'
   ])
}
```
### LLVM string output
```
declare i32 @_print_int(i32)

define i32 @fact(i32 %.arg_n) {
entry:
    %n = alloca i32
    store i32 %.arg_n, i32* %n
    br label %L1
L1:
    %result = alloca i32
    store i32 1, i32* %result
    %x = alloca i32
    store i32 1, i32* %x
    br label %L7
L7:
    %.r1 = load i32, i32* %x
    %.r2 = load i32, i32* %n
    %.r3 = icmp sle i32 %.r1, %.r2
    br i1 %.r3, label %L2, label %L3
L2:
    %.r4 = load i32, i32* %result
    %.r5 = load i32, i32* %x
    %.r6 = mul i32 %.r4, %.r5
    store i32 %.r6, i32* %result
    %.r7 = load i32, i32* %x
    %.r8 = add i32 %.r7, 1
    store i32 %.r8, i32* %x
    br label %L7
L3:
    %.r9 = load i32, i32* %result
    ret i32 %.r9
}
@x = global i32 0

define i32 @main() {
entry:
    br label %L4
L4:
    store i32 1, i32* @x
    br label %L8
L8:
    %.r10 = load i32, i32* @x
    %.r11 = icmp sle i32 %.r10, 9
    br i1 %.r11, label %L5, label %L6
L5:
    %.r12 = load i32, i32* @x
    %.r13 = call i32 (i32) @fact(i32 %.r12)
    call i32 (i32) @_print_int(i32 %.r13)
    %.r14 = load i32, i32* @x
    %.r15 = add i32 %.r14, 1
    store i32 %.r15, i32* @x
    br label %L8
L6:
    ret i32 0
}
```

### ...and we're done

This helps me remember by example what each step is supposed to do, though not necessarily how or why (I recall that the variable scoping, recursive control flow descent, and translation to assembly-style stack and branch/goto structures were all a bit mind-bending at the time, and would need some re-review if I were picking that part of the code up again).