/* 
   WIP wrapper to pass command-line argument(s) to user program
   (hard-coded to pass a set number of integer arguments)
   
   Since our language doesn't support pointers, chars, command-line arguments, and so on.
   
   To use, include this file with final compilation with Clang. For example:
   clang program.ll helper/runtime.c helper/args.c -o program.exe

   Also requires our compiler to wrap user code in function mainuser(), not main()
*/

#include <stdio.h>

// declaration for function of user code, that needs to be declared by user (or compiler)
void mainuser(int, int);

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
  if (argc > 1) {
    /* hard-coded to pass a fixed number of arguments to mainuser(), as ints */
    arg1 = atoi(argv[1]);
  }
  /* argc-1 because a program run with no arguments has argc==1 in C (program name) */
  mainuser(argc-1, arg1);
}
