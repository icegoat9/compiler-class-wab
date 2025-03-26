/*
   Testing some very basic C programs to inspect generated LLVM for I/O
*/
#include <stdio.h>
#include <stdlib.h>

int _print_int(int x) {
  printf("Output: %i\n", x);
  return 0;
}

int main(int argc, char **argv) {
  _print_int(argc);
  _print_int(atoi(argv[1]));  /* an error if no args */
}
