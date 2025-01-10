"""Quick helper functions to print text in color using ANSI codes."""

class ansicode:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
    reset = '\033[0m'
    bold = '\033[01m'
    underline = '\033[04m'

def printcolor(obj, col: str = ansicode.lightblue):
    """Print object (converted to str) using specified color or formatting.
    Color defaults to light blue if not specified."""
    print(col + str(obj) + ansicode.reset)

def print_colorheader(header, data = None, col: str = ansicode.lightblue):
    """Print header in color, then data in regular text color on new line.
    Header color defaults to light blue if not specified."""
    print(col + str(header) + ansicode.reset)
    print(data)

if __name__ == "__main__":
    printcolor('Hello', ansicode.lightblue)
    printcolor('World', ansicode.red)
    printcolor('Generic', ansicode.reset)

