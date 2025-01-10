/* 
   When we compile LLVM assembly down to machine code, we need to connect our language's print()
   to an existing machine-specific print library.
   
   Include this file with final compilation with Clang. For example:

   clang program.ll helper/runtime.c -o program.exe
*/

#include <stdio.h>

int _print_int(int x) {
  printf("Output: %i\n", x);
  return 0;
}
