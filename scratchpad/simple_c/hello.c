/*
   Testing some very basic C programs to inspect generated LLVM for I/O
*/
#include <stdio.h>
int main() {
  const char *str = "constant string.";
  printf("Hello, world.");
  printf("%s\n", str);
}
