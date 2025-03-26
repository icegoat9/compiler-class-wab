/*
   Testing some very basic C programs to inspect generated LLVM for I/O
   Integrating in way that we could have user code in main_user()
*/

#include <stdio.h>
#include <stdlib.h>

int _print_int(int x) {
  printf("Output: %i\n", x);
  return 0;
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
