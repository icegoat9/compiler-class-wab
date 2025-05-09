#!/bin/sh

# compile .wb code -> LLVM code -> executable

if [ $# -eq 0 ]; then
    echo ""
    echo "Usage: $0 <filename.wb> [-arg]     (.wb extension optional)"
    echo "For example:"
    echo "  $0 programs/test_programs/program1.wb"
    echo "  programs/test_programs/program1.exe"
    echo ""
    echo "If -arg is added, compile and link with command-line argument support."
    echo ""
    exit 1
fi

FILEPATH="$1"
# remove extension if present (will assume .wb)
FILEPATH=${FILEPATH%.*}
FILE=$(BASENAME $FILEPATH)

BLUE="\033[1;34m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
RESETCOLOR="\033[0m"
#FILEPATH=${FILE%/*}

if [ "$#" -gt 1 ] && [ $2 == "-arg" ]; then
    COMPILE_EXTRA="-c"
    LINK_EXTRA="helper/args.c"
    echo "${YELLOW}Caution:$RESETCOLOR Argument-parsing compiler mode not fully implemented and tested."
fi

# Run our custom compiler, generate LLVM output
# echo simplified version of commands run, without all the relative path prefixes
echo "${BLUE}compile_ast.py $COMPILE_EXTRA $FILE.wb > $FILE.ll$RESETCOLOR"
if python3 compiler/compile_ast.py $COMPILE_EXTRA $FILEPATH.wb > $FILEPATH.ll; then
    # check python3 return value, don't compile .ll to .exe if our compiler raised exception

    # Run clang, disable "overriding the module target triple" OSX warning
    # Include helper C functions that implement basic system I/O

    # Also generate machine code in .s file for manual inspection if desired
    # echo "${BLUE}clang -S $FILE.ll -o $FILE.s$RESETCOLOR"
    # clang -Wno-override-module -S $FILEPATH.ll -o $FILEPATH.s

    echo "${BLUE}clang $FILE.ll helper/runtime.c $LINK_EXTRA -o $FILE.exe$RESETCOLOR"
    clang -Wno-override-module $FILEPATH.ll helper/runtime.c $LINK_EXTRA -o $FILEPATH.exe
fi