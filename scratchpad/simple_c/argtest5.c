/*
   Testing some very basic C programs to inspect generated LLVM for I/O
*/

#include <stdio.h>

int _print_int(int x) {
  printf("Output: %i\n", x);
  return 0;
}

/* simplified atoi without including stdlib */

int atoi(const char *num) {
    int value = 0;
    int neg = 0;
    // decimal
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

void main_user(int argc, int arg1) {
 _print_int(argc);
 _print_int(argc-1);
 _print_int(arg1);
}

int main(int argc, char **argv) {
  int arg1 = 0;
  if (argc > 1) {
    arg1 = atoi(argv[1]);
  }
  main_user(argc,arg1);
}
