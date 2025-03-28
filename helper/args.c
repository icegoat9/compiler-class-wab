/* 
  WIP wrapper to pass up to two command-line arguments to user program,
  since our language doesn't support pointers, chars, or arrays.

  Arguments are passed as ints (the only data type our language supports at the moment)

  It also passes an "argc" (arg count) to our program, the number of command-line arguments
   (0 if no arguments, which is a -1 delta from the C argc meaning)
  If more than two arguments are passed, argc will list that number, but only the first two
   will be passed to the user program as we must pass them to static variable names rather than an array.
      
  To use, include this file with final compilation with Clang. For example:
  clang program.ll helper/runtime.c helper/args.c -o program.exe

  Also requires our compiler to wrap user code in function mainuser(), not main()
*/

#include <stdio.h>

// declaration for function of user code, that needs to be declared by user (or compiler)
void mainuser(int, int, int);

/* simplified atoi for ints only, without including stdlib */
int atoi(const char *num) {
    int value = 0;
    int neg = 0;
    if (num[0] == '-') {
      neg = 1;
      num++;
    }
    while (*num && *num >= '0' && *num <= '9') {
      value = 10 * value + (*num - '0');
      num++;
    }
    if (neg) {
        value = -value;
    }
    return value;
}

int main(int argc, char **argv) {
  int arg1 = 0;
  int arg2 = 0;
  if (argc > 1) {
    /* hard-coded to pass a fixed number of arguments to mainuser(), as ints */
    arg1 = atoi(argv[1]);
    if (argc > 2) {
      /* hard-coded to pass a fixed number of arguments to mainuser(), as ints */
      arg2 = atoi(argv[2]);
    }
  }
  /* argc-1 because a program run with no arguments has argc==1 in C (program name) */
  mainuser(argc-1, arg1, arg2);
}
