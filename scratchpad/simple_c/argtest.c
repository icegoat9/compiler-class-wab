/*
   Testing some very basic C programs to inspect generated LLVM for I/O
*/

#include <stdio.h>

/* note: rather than include, write a streamlined int-only atoi() in C? */
#include <stdlib.h> 

int main(int argc, char **argv) {
  printf("arguments: %d\n",argc-1);
  if (argc > 1) {
    int arg = atoi(argv[1]);
    printf("arg #1: %d\n",arg);
 }
}
