#!/bin/sh

# compile .wb code -> LLVM code -> executable
# WIP version that links in an argc/argv C wrapper (not yet working)

if [ $# -eq 0 ]; then
    echo ""
    echo "Usage: $0 <filename.wb>    (you may also omit the .wb extension)"
    echo "For example:"
    echo "  $0 programs/test_programs/program1.wb"
    echo "  programs/test_programs/program1.exe"
    echo ""
    exit 1
fi

FILEPATH="$1"
# remove extension if present (will assume .wb)
FILEPATH=${FILEPATH%.*}
FILE=$(BASENAME $FILEPATH)

BLUE="\033[1;34m"
RED="\033[1;31m"
RESETCOLOR="\033[0m"
#FILEPATH=${FILE%/*}

echo "${RED}Warning: WIP testing, argument-parsing mode not fully implemented.$RESETCOLOR"

# echo simplified version of commands run, without all the relative path prefixes
# -c flag compiles in "expect command-line arguments" mode
echo "${BLUE}compile_ast.py -c $FILE.wb > $FILE.ll$RESETCOLOR"
python3 compiler/compile_ast.py -c $FILEPATH.wb > $FILEPATH.ll

# Run clang, disable "overriding the module target triple" OSX warning
# Include helper C functions that implement basic system I/O
# Also generate machine code in .s file for manual inspection if desired
echo "${BLUE}clang -S $FILE.ll -o $FILE.s$RESETCOLOR"
clang -Wno-override-module -S $FILEPATH.ll -o $FILEPATH.s
echo "${BLUE}clang $FILE.ll runtime.c args.c -o $FILE.exe$RESETCOLOR"
clang -Wno-override-module $FILEPATH.ll helper/runtime.c helper/args.c -o $FILEPATH.exe


