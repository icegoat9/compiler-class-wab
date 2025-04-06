/* 
   When we compile LLVM assembly down to machine code, we need to connect our language's 
   input() to an existing machine-specific character-reading library / scanf implementation.
   
   Include this file with final compilation with Clang. For example:

   clang program.ll helper/scan.c -o program.exe
*/

#include <stdio.h>

int _scan_int() {
  printf("Input a number:");
  int i;
  scanf("%d", &i);
  return i;
}
