This directory contains miscellaneous code fragments that implement key I/O interfaces
such as printing values to the terminal and reading command-line arguments (we're not implementing an entire set of machine-specific standard libraries ourselves).

Generally, we'd include these during the final compilation step from LLVM (machine-independent
assembly code) to machine-specific assembly by Clang, for example:

`clang program.ll helper/runtime.c -o program.exe`

