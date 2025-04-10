# Wabbish

Wabbish is my name for a slight variant on the Wab / Wabbi / Wabbit languages created by [Dave Beazley](http://dabeaz.com/) for his [Writing-a-Compiler Class](https://www.dabeaz.com/compiler.html)

During that class and in a bit of work afterward, I completed a compiler for a language somewhere between the  Wab and Wabbi language specs, but then started playing around and adding other features, so I'm making this forked version of the Wab/Wabbi language spec page to keep track of what my particular compiler implements and avoid looking at similar but slightly different documentation for the original languages.

*Much of the language spec below is copied from a mix of the Wab and Wabbi language specs.*

## 1. Wabbish Overview

Wabbish has a standard set of features you're used to in programming including
numbers, variables, conditionals, loops, and functions.  Here is a
sample Wabbish program that prints the first 10 factorials:

```
func fact(n) {
    var result = 1;
    var x = 1;
    while x < n {
       result = result * x;
       x = x + 1;
    }
    return result * n;
}

var n = 0;
while n < 10 {
   print fact(n);
   n = n + 1;
}
```

## 2. Program Structure

A Wabbish program consists of a sequence of statements and
definitions. Code executes top-to-bottom like a script.  Simple
statements are terminated by a semicolon. For
example:

```
print 3;
var a = 4;
print 3*a;
```

A comment is denoted by `//` and extends to the end of the line. For example:

```
var a = 4;    // This is a comment
```

Statements involving control flow expect blocks of statements enclosed in
braces.  For example:

```
if a < b {
   print a;
} else {
   print b;
}
```

## 3. Datatypes

Wabbish only supports a single integer datatype.  All math operations and variables
work with integers only.

## 4. Variables

Variables are declared using the `var` keyword and may be given an initial value.  For example:

```
var x = 0;
var y;
```

Variable names must start with a letter, but may include letters and
numbers afterwards.  The following words are reserved and may not be
used as a variable name:

```
elif else func if print return var while for
```

Variables are managed in two different scopes.  Any variable declared
at the top-level is a global variable.  Global variables may be accessed
from anywhere in a program.  A variable that's declared inside a code block
(function, if-statement, while-loop) is a local variable.

**CAUTION:** Variables that are declared without being initialized have undefined behavior if they are used before assignment: there are currently no compiler features to catch this behavior.

## 5. Printing

To print a value, use the `print` statement.  For example:

```
print 3;
print x;
print 3 + x;
```

## 6. Math operations

The `+`, `-`, `*`, `/`, and `%` operators are supported.  In addition, 
unary negation is provided.  Thus, these are all valid:

```
var x = 10;
var y = 3;

print x + y;    // 13
print x - y;    // 7
print x * y;    // 30
print x / y;    // 3
print x % y;    // 1
print -x;       // -10
```

The division operator truncates the result so `10/3` is `3`.

The modulo operator is currently based on truncated division, so when one of the operands is negative, the output matches the sign of the first operand: `-5 % 3` returns `-2` (rather than `1` as it would in languages that use [floored division](https://en.wikipedia.org/wiki/Modulo#Variants_of_the_definition)). **CAUTION:** I may reverse this behavior in the future, which will change the behavior when exactly one of the operands is negative.

Operators only operate on pairs of values.  If you want to write a more complex expression, you need to use parentheses.  For example:

```
var x = 2 + 3;        // Valid 
var x = 2 + 3 + 4;    // Invalid!
var x = 2 + (3 + 4);  // Valid!

print 6 * x * x + 3 * x - 8           // Invalid!
print (((6 * x) * x) + (3 * x)) - 8   // Valid!
```

## 6. Relations

The following relational operators are supported.

```
x < y
x <= y
x > y
x >= y
x == y
x != y
```

Relations may only be used within the test of an `if` or `while` statement (see below).
They may not be mixed with ordinary expressions.

## 7. Conditionals

Use `if` to write a conditional. For example:

```
if a < b {
   statement1;
   statement2;
} else {
   statement3;
   statement4;
}
```

A valid **relation** (see above) must immediately follow the `if` keyword. A reminder that in Wabbish the only data type is integers (not booleans), so you may not use an expression instead of a relation. For example statements such as `if x {` or `if 2 * 2 {` or `if True {` are invalid.

If you have a conditional you always want to run (perhaps for testing), a statement such as `if 1 == 1 {` is valid, however, as `1 == 1` is a relation.

### 7.1 Variant Conditionals

A branch may be empty, thus you may write:

```
if a < b {
   statement1;
   statement2;
} else {
}
```

The `else` branch is optional, so the following is an even simpler way to write the above:

```
if a < b {
   statement1;
   statement2;
}
```

Wabbish also allows any number of else-if branches using the `elif { }` structure, for example:

```
if a < b {
   statement1;
} elif a > b {
   statement2;
} elif a = b {
   statement3;
} else {
   statement4;
}
```

## 8. Loops

Use `while` to write a loop.  For example:

```
while a < b {
    statement1;
    statement2;
}
```

Like `if`, a relation must appear after the `while` keyword.

### 8.1 For Loops

Use `for` to create a simple loop with an incrementing index. The below loop runs 10 times:

```
for i = 1,10 {
  print i * i;
}
```

**Note: The implementation is in-development and has some known bugs:** In particular, under the hood the implementation declares index variable i, so the compiler will raise an error if i has previously been declared in the current scope. This for example limits the ability to reuse the same index variable in multiple for loops in a program.

## 9. Functions

A function is defined using `func` like this:

```
func f(x, y) {
    statement1;
    statement2;
    ...
    return result;
}
```

Functions only take integer arguments and return an integer.

The `return` statement is used to return a value.  If control
reaches the end of a function without encountering a `return`
statement, 0 is returned.

Any variable defined inside a function is local to that function (i.e.,
the name is not visible to code outside). This includes the names of
the function parameters.

Wabbish does not allow functions to be defined inside any code block
enclosed by braces.  This means that functions can only be defined at the
"top level" and not inside the body of an if-statement, while-loop, or
other function definition.

To call a function, use parentheses and supply input argument value(s). For
example:

```
print f(2, 3);
var y = f(x);
```

Functions may be freely used in math expressions.  So, a statement like
this is valid:

```
print f(2,3) + f(4,5);     // OK
```

as is the statement:

```
print f(2 + 3, 4 + 5);    // OK
```

### 9.1 Functions Without Arguments

Functions that take zero arguments (mostly relevant if their purpose is to run I/O operations such as PRINT) should be supported, but this has not yet been thoroughly tested.

## 10. Isolated Expressions

Isolated expressions appearing as a statement are allowed.  The expression evaluates, but the value is disregarded.  The primary use is writing functions whose purpose is to execute I/O operations. For example:

```
func printval(x) {
     print x;
}

printval(10);
```

Examples of other expression statements which are valid syntax, but useless:

```
1 + 1;
x;
```

**CAUTION:** Isolated expressions have only been tested lightly.

## 11. Command-line Arguments

An experimental compile mode (with flag -arg) gives the user program access to up to two command-line arguments when it is run.

In particular, top-level user code has access to special system variables `argc`, `arg1`, and `arg2` without need to declare them.

`argc` holds the number of command-line arguments passed to the executable (typically 0, 1, or 2, though if three or more arguments are passed argc will hold that number though it's unlikely to be relevant).

`arg1` and `arg2` will hold the first two arguments passed (set to 0 for any omitted arguments: argc can be used to determine if arg1 and/or arg2 are valid to distinguish between "argument omitted" and "0 passed as argument"). These parameters are converted to integers (positive or negative).

**Note:** These system arg variables are provided with top-level local scope, not global scope. That is, they are accessible in top-level user code, but not within any user-defined functions.


## 12. Formal Syntax

The following grammar is a description of Wabbish syntax written as a PEG
(Parsing Expression Grammar). Tokens are specified in ALLCAPS and are
assumed to be returned by the tokenizer.  In this specification, the
following syntax is used:

```
{ e }   --> Zero or more repetitions of e.
e1 / e2 --> First match of e1 or e2.
[ e ]   --> Optional expression
```

A program consists of zero or more statements followed by the
end-of-file (EOF).  Here is the grammar:

```
program : statements EOF

statements : { statement }         ; Note: { ... } means repetition

statement : print_statement
          / variable_definition
          / if_statement
          / while_statement
          / for_statement
          / func_definition
          / return_statement
          / assignment_statement
          / expr_statement

print_statement : PRINT expression SEMI

variable_definition : VAR NAME ASSIGN expression SEMI

assignment_statement : NAME ASSIGN expression SEMI

if_statement : IF relation LBRACE statements RBRACE { ELIF relation LBRACE statements RBRACE } [ ELSE LBRACE statements RBRACE ]

while_statement : WHILE relation LBRACE statements RBRACE

for_statement : FOR init SEMI relation SEMI increment SEMI LBRACE statements RBRACE

func_definition : FUNC NAME LPAREN parameters RPAREN LBRACE statements RBRACE

parameters : [ NAME { COMMA NAME } ]

return_statement : RETURN expression SEMI

expr_statement : expression SEMI

expression : term PLUS term
           / term MINUS term
           / term TIMES term
           / term DIVIDE term
           / term MODULO term
           / term

relation : expression LT expression
         / expression LE expression
         / expression GT expression
         / expression GE expression
         / expression EQ expression
         / expression NE expression      

term : INTEGER
     / NAME LPAREN arguments RPAREN
     / NAME
     / LPAREN expression RPAREN
     / MINUS term

arguments : [ expression { COMMA expression } ]
```

The following tokens are defined:

```
NAME    = [a-zA-Z][a-zA-Z0-9]*
INTEGER = [0-9]+
PLUS    = "+"
MINUS   = "-"
TIMES   = "*"
DIVIDE  = "/"
MODULO  = "%"
LT      = "<"
LE      = "<="
GT      = ">"
GE      = ">="
EQ      = "=="
NE      = "!="
ASSIGN  = "="
LPAREN  = "("
RPAREN  = ")"
LBRACE  = "{"
RBRACE  = "}"
SEMI    = ";"
COMMA   = ","
ELSE    = "else"
ELIF    = "elif"
IF      = "if"
FUNC    = "func"
PRINT   = "print"
RETURN  = "return"
VAR     = "var"
WHILE   = "while"
FOR     = "for"
```


# Possible Future Specifications

[Future-Specification.md](Future-Specification.md)
