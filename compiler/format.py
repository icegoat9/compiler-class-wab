# format.py
"""Code formatter for the compiler project.

Displays the AST representation of the program in a human-readable format, to aid with compiler
development, debugging, and understanding the status of the AST. This needs to be able to operate on
all intermediate compiler steps, and have human-readable expressions of all classes and data structures
involved."""

# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [ ] add assertion-based unit tests? but this will be brittle as format output is for human
#     consumption and I may tweak it over time, there isn't a clear "correct output"
# [X]rewrite with python "%s %s" % (foo, bar) approach?
# [X] rewrite this file with Python match/case syntax like other modules
# [X] how to format indents / nesting for a whole block
# [X] adding braces
# [X] Where to place parentheses around an expression vs not
# [X]  in formatting, add at all but top level-- check somehow if expression is nested in another?
# [ ] formatting STATEMENT and BLOCK type, seeing CALL(name='fact', n=1) vs desired CALL('fact',1)
#     (TBD, maybe handle this through __str__ or __repr__ properties of some classes?)

from model import *
from printcolor import *

FORMAT_TAB = "   "  # string per indentation level
FORMAT_DEBUG = False

# Format a complete program
def format_program(program: Program) -> str:
    return fmt_statements(program.statements)

# Format a list of statements
# 'indent' is the # of indent levels deep in a program
def fmt_statements(statements: list[Statement], indent: int = 0) -> str:
    """Format a list of statements one by one. Called either on the top-level program, or on the
    bodies of statements that contain other statements such as IfElse.
    
    The indent parameter is the number of indent levels deep we are in a program (increase
    it when parsing the body of a flow control structure to visually indent its contents).
    """
    code = ""
    for s in statements:
        code += FORMAT_TAB * indent
        code += fmt_statement(s, indent)
    return code

def fmt_statement(s: Statement, indent: int = 0) -> str:
    """Format a single statement as a string, including formatting all expressions and 
    child statements (e.g. body of a While loop) within it.
    
    The indent parameter is the number of indent levels deep we are in a program (increase
    it when parsing the body of a flow control structure to visually indent its contents).
    """
    match s:
        case Print(x):
            return "print %s;\n" % fmt_expr(x)
        case Assign(left, right):
            return "%s = %s;\n" % (fmt_expr(left), fmt_expr(right))
        case DeclareValue(left, right):
            return "var %s = %s;\n" % (fmt_expr(left), fmt_expr(right))
        case GlobalVar(name):
            return "global %s;\n" % fmt_expr(name)
        case LocalVar(name):
            return "local %s;\n" % fmt_expr(name)
        case Declare(name):
            return "var %s;\n" % fmt_expr(name)
        case IfElse(condition, iflist, elselist):
            return "if %s {\n%s%s} else {\n%s%s}\n" % (
                fmt_expr(condition),
                fmt_statements(iflist, indent + 1),
                FORMAT_TAB * indent,
                fmt_statements(elselist, indent + 1),
                FORMAT_TAB * indent,
            )
        case IfElifElse(condition, iflist, elifs, elselist):
            out = "if %s {\n%s%s" % (fmt_expr(condition), fmt_statements(iflist, indent + 1), FORMAT_TAB * indent)
            for e in elifs:
                out += "} elif %s {\n%s%s" % (
                    (fmt_expr(e.condition), fmt_statements(e.iflist, indent + 1), FORMAT_TAB * indent)
                )
            out += "} else {\n%s%s}\n" % (
                fmt_statements(elselist, indent + 1),
                FORMAT_TAB * indent,
            )
            return out
        case While(condition, statements):
            return "while %s {\n%s%s}\n" % (
                fmt_expr(condition),
                fmt_statements(statements, indent + 1),
                FORMAT_TAB * indent,
            )
        case For(init, condition, increment, statements):
            return "for %s %s; %s {\n%s%s}\n" % (
                fmt_statement(init).rstrip(),  # remove newline
                fmt_expr(condition),
                fmt_statement(increment).rstrip(),  # remove newline
                fmt_statements(statements, indent + 1),
                FORMAT_TAB * indent,
            )
        case Return(x):
            return "return %s;\n" % fmt_expr(x)
        case Function(name, params, statements):
            # apply fmt_expr() to each parameter in list, then join with ,
            paramstr = ", ".join(map(fmt_expr, params))
            return "func %s(%s) {\n%s}\n\n" % (fmt_expr(name), paramstr, fmt_statements(statements, 1))
        # case PRINT():
        #    return "PRINT()"
        case STATEMENT(lst):
            # Big to-do: figure out cleaner EXPR and STATEMENT FORMATTING (or modify class to have __repr__)
            return (
                "STATEMENT([\n"
                + FORMAT_TAB * (indent + 1)
                + ("\n" + FORMAT_TAB * (indent + 1)).join([str(x) for x in lst])
                + "\n"
                + FORMAT_TAB * indent
                + "])\n"
            )
        case BLOCK(label, lst):
            # Big to-do: figure out cleaner EXPR and STATEMENT FORMATTING (or modify class to have __repr__)
            return (
                "BLOCK(label='%s', [\n" % label
                + FORMAT_TAB * (indent + 1)
                + ("\n" + FORMAT_TAB * (indent + 1)).join([str(x) for x in lst])
                + "\n"
                + FORMAT_TAB * indent
                + "])\n"
            )
        case _:
            raise RuntimeError(f"Can't format {s}")


def fmt_expr(e: Expression, nested: bool = False) -> str:
    """Format a single expression as a string.

    Set nested=True if this expression is itself a subexpression of (i.e. one argument of)
    a binary operation such as +,-,*,/, to print parentheses around this expression in that
    case, without cluttering the output with parentheses around single-depth math expressions."""
    if FORMAT_DEBUG:
        print(e)
    match e:
        case Integer(n):
            return str(n)
        case GlobalName(x):
            return "global[%s]" % x
        case LocalName(x):
            return "local[%s]" % x
        case Name(x) | RelationOp(x):
            return x
        #        case Negate(left):
        #            strtxt = "-%s" % (fmt_expr(left, nested=True))
        #            if nested:
        #                strtxt = "(%s)" % strtxt
        #            return strtxt
        case Add(left, right):
            strtxt = "%s + %s" % (fmt_expr(left, nested=True), fmt_expr(right, nested=True))
            if nested:
                strtxt = "(%s)" % strtxt
            return strtxt
        case Multiply(left, right):
            strtxt = "%s * %s" % (fmt_expr(left, nested=True), fmt_expr(right, nested=True))
            if nested:
                strtxt = "(%s)" % strtxt
            return strtxt
        case Subtract(left, right):
            strtxt = "%s - %s" % (fmt_expr(left, nested=True), fmt_expr(right, nested=True))
            if nested:
                strtxt = "(%s)" % strtxt
            return strtxt
        case Divide(left, right):
            strtxt = "%s / %s" % (fmt_expr(left, nested=True), fmt_expr(right, nested=True))
            if nested:
                strtxt = "(%s)" % strtxt
            return strtxt
        #    elif isinstance(e, Variable):
        #        return fmt_expr(e.name)
        case Relation(op, left, right):
            return "%s %s %s" % (fmt_expr(left, nested=True), fmt_expr(op), fmt_expr(right, nested=True))
        case CallFn(name, params):
            # apply fmt_expr() to each parameter in list, then join with ,
            paramstr = ", ".join(map(fmt_expr, params))
            return "%s(%s)" % (fmt_expr(name), paramstr)
        # Now add cases for 'expression instructions' , the 'machine' section of model.py
        # Note: looking at someone else's approach, realized I don't have to call out each case and
        #       can use repr(e) for all INSTRUCTIONs
        #      case PUSH(val):
        #          return "PUSH(%d)" % val
        #      case LT():
        #          return "LT()"
        #      case EQ():
        #          return "EQ()"
        #      case ADD():
        #          return "ADD()"
        #      case CALL(fname, pnum):
        #          return "CALL('%s',%d)" % (fname, pnum)
        #      case LOAD_LOCAL(name):
        #          return "LOAD_LOCAL('%s')" % name
        #      case LOAD_GLOBAL(name):
        #          return "LOAD_GLOBAL('%s')" % name
        case LLVM(op):
            return "LLVM('%s')" % op
        case INSTRUCTION():
            return repr(e)
        case EXPR(lst):
            # return repr(e)
            # TODO: not sure how to best represent this cleanly
            # return "EXPR(%s)" % ", ".join([repr(x) for x in lst])
            return "EXPR([%s])" % ", ".join([fmt_expr(x) for x in lst])
        case _:
            raise RuntimeError(f"Can't format {e}")
