# helper.py
"""Helper debugging functions for compiler, not essential to function."""

from model import *
from printcolor import *
from format import *

# Helper function that displays the items that failed an assertion, colorfully
def assert_equal_verbose(a, b, formatprogram = True):
    if a != b:
        if isinstance(a, Program) and isinstance(b,Program) and formatprogram:
            a = format_program(a)
            b = format_program(b)
        print(
            "%s%s%s   is not equal to\n%s%s%s"
            % (ansicode.blue, str(a), ansicode.reset, ansicode.red, str(b), ansicode.reset)
        )
    assert a == b

