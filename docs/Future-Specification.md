# Wabbish Future Features

As a complement to the implemented [Wabbish Specification](Wabbish-Specification.md), potential future features. See also the [TODO](TODO.md) list for quick ideas-- this is just where I flesh planned behavior and syntax out in more detail.

## X. Modulo % operator [work in progress]

This is partially implemented, but with a 'truncated division' definition, I plan to update it to use 'floored division', so that for example `-1 % 2` = `1` rather than `-1`.

```
var a = 5;
var b = 3;
var q = a / b;
var r = a % b;   // new modulo operator
```

This can already be implemented in a user function since we already have integer division, e.g. `a - (a / b) * b`, but it will be useful enough when we add an array data type to consider implementing it in the language. TBD whether we'll translate it to the above form in an early compiler pass, or compile it to the LLVM instruction `srem`.

## X. Terminal Input [idea, not implemented]

This might be a bit silly to implement before even the notion of data types, strings, or arrays, but it might enable some interesting little interactive programs. Tentative idea:

### Option 1: Character input 

The `input` command reads one keypress from the keyboard and returns its ASCII value, or returns 0 if no key has been pressed. This would wrap a helper function using a standard library such as getchar().

For example, this program could build up a number from keys pressed:

```
var num = 0;
var key = 0;
while key != 13 {               // until Enter is pressed
  key = input();
  if key >= 48 {                // '0' character
    if key <= 58 {              // '9' character
      num = num * 10;
      num = num + (key - 48);
      print(num);
    }
  }
}
print(num);
```

### Option 2: Number input 

The `input` command reads a sequence of digits and a newline from input and passes them to the program as an int. This would wrap a helper function using a standard library such as scanf(). This might including printing a prompt to the user to enter a number.

Example syntax:

```
var num = 0;
num = input();
print(num);
```
## X. Array data types [idea, not implemented]

We start with a simple single-dimensional, fixed-length integer array data type, with array indexes starting at 1 (like Lua, different than C).

They are declared with brackets indicating the length, and individual elements can be assigned or read using brackets, e.g.

```
var x[10];
x[1] = 7;
x[5] = 70;
print x[1] + x[5];
```

The built-in function len() returns the length of an array, for example:

```
for i=1,len(x) {
  print x[i];
}
```

Other than len(), statements and expressions can only operate on integers (e.g. array elements), not arrays themselves. So for example:

```
var x[10];
x[1] = 7;       // valid
var y = x[1];   // valid
var y = x;      // invalid
var y[10] = x;  // invalid

func foo(n) {
  var a[n];
  a[1] = 7;
  return a[1]; // valid
  return a;    // invalid
}

foo(x[1]);  //valid
foo(x);     //invalid
```

### Out-of-range behavior

One initial idea is to make all arrays into circular buffers: indices to an array are automatically passed to modulo to wrap around to the beginning and avoid accessing memory outside the array.

### String handling

In the future, if we implement different data types such as float and char, a string could be represented as an array of char values. Even just this would allow user code implementations of functions such as int_to_str() and a very limited printf(), as well as enable more useful command-line arguments and keyboard input handling.





