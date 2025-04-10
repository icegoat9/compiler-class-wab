# Wabbish Future Features

As a complement to the implemented [Wabbish Specification](Wabbish-Specification.md), potential future features. See also the [TODO](TODO.md) list for quick ideas-- this is just where I flesh planned behavior and syntax out in more detail.

## X. [not implemented] Terminal Input

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
## X.






