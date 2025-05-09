# model.py
"""Class definitions for the overall Program model / abstract syntax tree, used in nearly every
part of the compiler and one of the most important decisions in how the overall parser and compiler
passes are structured.

Some of these classes include a few variables, some are empty classes primarily used for type hinting and
error checking.

Note: There's currently a bit of inconsistency in where human-readable formatting for classes is defined:
that's primarily handled in format.py, but a few classes define __str__ or __repr__ methods here to configure
how they are printed to the user.
"""
#
# Cleanup TODO
# [X] docstrings
# [ ] overall clean up individual classes, name consistently (see some FIX and TODO items)
# [ ]   Declare vs GlobalVar name difference
# [ ] organize classes into logical groups, possible with a table of contents
# [ ] consistency in use of __str__/__repr__ vs. format.py module
# [ ] EXPR __repr__ with parentheses for enclosed list?
# [ ] think about Negate operator vs. not

# Open Questions, approaches to data structures
# [ ] FIX: Scope uses Name vs str types in some methods
# [X] Variable(Name('x')) or Variable('x')? or Variable(name,val)?
# [ ]    is the data type / class of x in "x=5" same as in "x+1"?
# [ ] Operator("+") or Operator(MathOp("+")) or Operator(BinOp("+")) or PlusOp()?
# [ ]   Rename MathOp to BinaryOp / etc
# [ ] Make LessThan and Equality subclasses? Maybe not useful.
# [X] In general, make some more hierarchical classes (mathop, etc)
# [X] Should Function() take a list of Variables or a list of Names as parameters?
# [ ] Rename SUB token to MINUS here and in tokenizer, and so on, as it isn't always subtract? (e.g. as unary operator)
# [ ] Future idea: return not just local vs global in scopes but _which_ scope it's defined in? No-- handled by parsing recursively.

from dataclasses import dataclass

class Statement:
    pass

# placeholder for expressions without typing implemented yet
DUMMYTYPE = "DUMMYTYPE"

@dataclass
class Expression:
    wtype : str

@dataclass
class Name(Expression):
    str : str

## Scope stuff

class Scope:
    #TODO: FIX: declare() takes Name but getscope() takes str
    def __init__(self, parent = None):
        self.variables = set()
        self.parent = parent
    
    def declare(self, name: Name):
        self.variables.add(name.str)

    def isglobalscope(self):
        return self.parent is None

    def getscope(self, name: str):
        if name in self.variables:
            if self.isglobalscope():
                return 'global'
            else:
                return 'local'
        elif self.isglobalscope():
            # we are the global scope and variable is not found!
            # TODO(?) raise error here or return None and let callers raise error?
            return None
#            raise RuntimeError("variable %s not found in any scope!")
        else:
            return self.parent.getscope(name)

    def new_child_scope(self):
        # make a child, typically to pass into a new definition block
        return Scope(parent = self)


## Expressions

@dataclass
class Integer(Expression):
    n : int

# Variable references (e.g., 'x')
class GlobalName(Name): pass
class LocalName(Name): pass

@dataclass
class Declare(Statement):
    name : Name

# Variable declarations  (e.g., 'var x')
# May want to rename GlobalDeclare for consistency, or rename Declare() above to Var(), etc...
class GlobalVar(Declare): pass
class LocalVar(Declare): pass
    
@dataclass
class DeclareValue(Statement):
    left : Name
    right : Expression

# Original idea here was to have a special class for variables separate from Name, primarily so
#  that we can insist the left side of an Assign is a Variable rather than any Expression... 
#  but tricky, not sure.
# Drawback: this means we'd have a lot of Variable(Name('x')) rather than Name('x') in
#  every expression (math, function calls, assignment, etc) which gets cluttered.
# Commenting out for now, actually, and go with the simpler Name()
#@dataclass
#class Variable(Expression):
#    name : Name

@dataclass 
class MathOp(Expression):
    left : Expression
    right : Expression

class Add(MathOp): pass
class Multiply(MathOp): pass
class Subtract(MathOp): pass
class Divide(MathOp): pass
class Modulo(MathOp): pass

@dataclass
class UnaryOp(Expression):
    left: Expression

# class Negate(UnaryOp): pass

# TODO: is this obsolete given the MathOp class above?
@dataclass
class Multiply(Expression):
    left : Expression
    right : Expression

@dataclass
class Assign(Statement):
    left : Name
    right : Expression

# Is this operator (e.g. < or =) an Expression, or something else?
@dataclass
class RelationOp:
    name: str

# Not used yet
class RelationLT(RelationOp): pass
class RelationEq(RelationOp): pass

# Is this a Expression (it is a true-of-false), or something else?
@dataclass
class Relation(Expression):
    op: RelationOp
    left : Expression
    right : Expression

@dataclass
class CallFn(Expression):
    name: Name
    params: list[Expression]

## Statements

@dataclass
class Print(Statement):
    value : Expression

@dataclass
class PrintStr(Statement):
    txt : str

@dataclass
class StrConstNum:
    n : int
    txt : str

@dataclass
class PrintStrConstNum(Statement):
    n : int

@dataclass
class Return(Statement):
    value: Expression

@dataclass
class IfElse(Statement):
    condition: Relation
    iflist: list[Statement]
    elselist: list[Statement]

@dataclass
class IfElifElse(Statement):
    condition: Relation
    iflist: list[Statement]
    elifs: list[IfElse]
    elselist: list[Statement]

@dataclass
class While(Statement):
    condition: Relation
    statements: list[Statement]

@dataclass
class For(Statement):
    name: Name
    startval: Expression
    endval: Expression
    statements: list[Statement]

@dataclass
class Function(Statement):
    name: Name
    params: list[Name]
    statements: list[Statement]

@dataclass
class ExprStatement(Statement):
    value : Expression


## Top-level object representing an entire program
@dataclass
class Program:
    statements : list[Statement]


################################################
# The 'machine'

@dataclass
class INSTRUCTION():
    pass

@dataclass
class PUSH(INSTRUCTION):
    value: int
    def __repr__(self):
        return f"PUSH({self.value})"

class ADD(INSTRUCTION): pass
class MUL(INSTRUCTION): pass
class SUB(INSTRUCTION): pass
class DIV(INSTRUCTION): pass
class MOD(INSTRUCTION): pass
class LT(INSTRUCTION): pass
class EQ(INSTRUCTION): pass
class LTE(INSTRUCTION): pass
class GT(INSTRUCTION): pass
class GTE(INSTRUCTION): pass
class NEQ(INSTRUCTION): pass

@dataclass
class LOAD_GLOBAL(INSTRUCTION):
    name: str
    def __repr__(self):
        return f"LOAD_GLOBAL('{self.name}')"

@dataclass
class LOAD_LOCAL(INSTRUCTION):
    name: str
    def __repr__(self):
        return f"LOAD_LOCAL('{self.name}')"

@dataclass
class CALL(INSTRUCTION):
    name: str
    n: int
    def __repr__(self):
        return f"CALL('{self.name}',{self.n})"


@dataclass
class EXPR(Expression):
    instructions: list[INSTRUCTION]
    # Adding this to make output more compact
    #def __repr__(self):    
    #    return f'EXPR({self.instructions})'

# Statements
    
@dataclass
class STORE_LOCAL(INSTRUCTION):
    name : str    
    def __repr__(self):
        return f"STORE_LOCAL('{self.name}')"

@dataclass
class STORE_GLOBAL(INSTRUCTION):
    name : str
    def __repr__(self):
        return f"STORE_GLOBAL('{self.name}')"


@dataclass
class PRINT(INSTRUCTION):
    pass    

@dataclass
class PRINT_STR_CONST(INSTRUCTION):
    n : int  # index of global string const

@dataclass
class STRCONST(INSTRUCTION):
    n : int
    str : str

@dataclass
class RETURN(INSTRUCTION):
    pass

@dataclass
class LOCAL(INSTRUCTION):
    name : str
    def __repr__(self):
        return f"LOCAL('{self.name}')"


@dataclass
class STATEMENT(Statement):
    instructions: list[INSTRUCTION]

@dataclass
class BLOCK(Statement):
    label : str
    instructions: list[INSTRUCTION]

@dataclass
class GOTO(INSTRUCTION):
    label: str

@dataclass
class CBRANCH(INSTRUCTION):
    iftrue: str
    iffalse: str

@dataclass
class LLVM(INSTRUCTION):
    op: str
    def __repr__(self):
        return f"LLVM '{self.op}'"

