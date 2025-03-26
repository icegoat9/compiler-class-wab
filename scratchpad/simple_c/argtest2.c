/*
   Testing some very basic C programs to inspect generated LLVM for I/O
*/
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  printf("Arg 1: %d\n",atoi(argv[1]));  /* an error if no args */
}
