# label_global.py
"""Manage a global index of 'what's the next block label available' for the machine code generation
process, to ensure that flow control that will be converted to JUMP / GOTO / BRANCH types of statements
can link to uniquely identified code blocks during the code generation process.

Used by at least basicblocks.py and controlflow.py
"""

# TODO?
# [X] Encapsulate this better, e.g. hint block_counter as private with _ prefix
from printcolor import *

_block_counter = 0

def init_global_label(n: int = 0) -> None:
    """Initialize labels to start at some number. Typically this is zero, but that can be overwritten
    to allow for example deterministic testing of a stage of the compiler whose output might otherwise
    depend on how many labels a previous compiler step had reserved."""
    global _block_counter
    _block_counter = n

def get_next_label(debug_force_L99: bool = False) -> str:
    """Return string of next label e.g. 'L1' or 'L2'.
    If debug is set True, always returns a specific label ('L99') which is useful for some
    deterministic unit tests of callers."""
    if debug_force_L99:
        return "L99"
    global _block_counter
    _block_counter += 1
    return "L%d" % _block_counter

######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    init_global_label(0)
    assert get_next_label() == "L1"
    assert get_next_label() == "L2"
    assert get_next_label(debug_force_L99=True) == "L99"
    assert get_next_label() == "L3"
    init_global_label(5)
    assert get_next_label() == "L6"
    printcolor("tests PASSED", ansicode.green)

