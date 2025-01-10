#!/bin/sh

# compile .wb code -> intermediate representation -> transpile to simple Python
# outputs to the terminal not a file

if [ $# -eq 0 ]; then
    echo ""
    echo "Usage: $0 <filename.wb>    (you may also omit the .wb extension)"
    echo "For example:"
    echo "  $0 programs/pow.wb > programs/pow.py"
    echo "  python3 programs/pow.py"
    echo ""
    exit 1
fi

FILEPATH="$1"
# remove extension if present (will assume .wb)
FILEPATH=${FILEPATH%.*}
FILE=$(BASENAME $FILEPATH)

BLUE="\033[1;34m"
RESETCOLOR="\033[0m"

# echo simplified version of commands run, without all the relative path prefixes
echo "${BLUE}python3 compile_to_python.py $FILE.wb$RESETCOLOR"
python3 compiler/compile_to_python.py $FILEPATH.wb

# Versions that write to file directly (not used)
#echo "${BLUE}python3 compile_to_python.py $FILE.wb > ${FILE}_gen.py$RESETCOLOR"
#python3 compiler/compile_to_python.py $FILEPATH.wb > ${FILEPATH}_gen.py

