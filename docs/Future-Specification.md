# Wabbish Future Features

As a complement to the implemented [Wabbish Specification](Wabbish-Specification.md), potential future features. See also the [TODO](TODO.md) list for quick ideas-- this is just where I flesh them out in more detail.

The first three are Wabbi language features discussed in class that I did not get around to implementin.

## X. [not implemented] Optional Variable Value

Variables can be declared without an initializer.  If missing, assume the
initial value is 0.

```
var x;

print x;    // Prints 0
```

## X. [not implemented] Zero-argument functions

Functions can take no arguments. For example:

```
func f() {
    return 42;
}

print f();
```

## X. [not implemented] Isolated Expressions

Isolated expressions appearing as a statement are allowed.  The
expression evaluates, but the value is disregarded.  The primary use
is writing functions that print things. For example:

```
func printval(x) {
     print x;
}

printval(10);
```

## X. [not implemented] Command-Line Argument

Compiled programs (with the help of a bit of wrapper code built into the compiler) accept one command-line argument, and pass it to the Wabbish program in the special reserved variable `arg`. If no command-line argument is present, `arg` has a value of 0. For example, this program would display the square of the passed argument:

```
var square = 0;
square = arg * arg;
print(square);
```







