#!/bin/sh

# compile .wb code -> LLVM code -> executable (same process as compile.sh)
# But then also run it

if [ $# -eq 0 ]; then
    echo ""
    echo "Usage: $0 <filename.wb>    (you may also omit the .wb extension)"
    echo "For example:"
    echo "  $0 programs/test_programs/program1.wb"
    echo ""
    exit 1
fi

# First, compile the code
./compile.sh $1

FILE="$1"
# replace extension with .exe
EXE=${FILE%.*}.exe
#echo "${BLUE}$EXE$RESETCOLOR"
$EXE

