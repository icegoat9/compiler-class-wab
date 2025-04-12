# parser_ast.py
"""The major first step of parsing the output of the tokenizer into a data structure (AST) that represents
the overall user program.

Later compiler steps will each manipulate, simplify, and transform this AST. Because this parser becomes more
complex and lengthy as the language definition expands, we will try to shift as much AST analysis as possible
into these separate later passes. For example, this compiler may understand an If..Elif..Else structure enough
to represent it as an IfElifElse() class object, then a later compiler pass might rewrite that into a simpler
set of nested If..Else structures so that not all downstream compiler passes need to understand it.

Much of the structure of this parser is based around looking just one or two tokens ahead and using that to
determine what program operation is happening, then filling in the data model based on the few surrounding tokens.
For example, if the parser looks one token ahead and sees a '+', it expects that it is in the middle of adding
two values and fills in the data model based on that. Because the language definition is relatively explicit
(requiring parentheses to set the order of operations for nested math rather than automatically determining it by
operator precedence over arbitrarily complex expressions), this minimal lookahead approach should work for
correctly-written programs.

Similarly, the language definition involves ; at the end of statements, and the parser checks for the presence
of these as one way to catch syntax errors.

This is one of the main places in the compiler where new language features are defined and implemented.
"""
#
# Cleanup TODO
# [X] docstrings
# [X] conceptual description / high-level comments
# [X] assertion-based unit tests

# TODO
# [ ] Write a lot of bad / broken programs, and refine parser error messages in those cases
# [ ] Consider catching the raw Python exception from bad parsing and just returning the more concise
#       parser error message with line/column and details (stack trace is often irrelevant at this step)
# [X] Extend function parsing to handle multiple arguments
# [X] Start Wab7 Step6, look into addition and multiply in parse_term (commented out bits infinite loop, hmm)
# [X]   Then remove deprecated older parse_add, etc
# [ ] Maybe, similar to refactor of parse_add -> parse_term, refactor the parse_conditions?
#       But not needed since, unlike + and *, conditions can't appear in random terms e.g. x = 2 < 3 is invalid,
#       we don't need to inspect a term to check if it's a condition, we only see them in known places If and While
# [ ] Should we split out the unary negation operator parsing here, by parsing it into a Negate(x) object and then
#       having a later compiler pass that swaps it for Subtract(0,x), just to split functionality out of the
#       parser to later passes when possible?
# [X] Test on sample test programs in tests/ (Wab7_Testing section)
# [X] Inspect parsing of fact.wb and factre.wb
# [X] Review the formal PEG syntax for Wab, check vs this parser
#      https://github.com/dabeaz-course/compilers_2024_03/blob/main/docs/Wab-Specification.md#10-formal-syntax
# [X] Revise hacky NONE token used in readahead() -- maybe just integrate readahead() into checkahead() since that's its only caller

import os
from model import *
from format import *
from printcolor import *
from tokenizer import *
from includes import *
from pprint import pprint
from debughelper import *


def parse_program(tokens: list[Token]) -> Program:
    """Parse a program (a list of tokens) to generate a Program AST object."""
    p = Parser(tokens)
    return Program(p.parse_statements())


###########################
## Parser class


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.n = 0
        """index to current token being analyzed."""

    # get token at current pointer if it's of toktype (if not, error)
    def expect(self, toktype) -> Token:
        #        try:
        tok = self.tokens[self.n]
        #        except IndexError:
        #            raise SyntaxError(f"Expected '{token_text[toktype]}', got end of file.")
        if tok.toktype == toktype:
            self.n += 1
            return tok
        else:
            raise SyntaxError(
                f"(line {tok.sourceline}, col {tok.sourcecol}) Expected '{token_text[toktype]}', got '{token_text[tok.toktype]}'"
            )

    # Check if the token N steps ahead (default: current token) is of type toktype,
    #   without advancing the program parsing counter n, unlike expect()
    def checkahead(self, toktype: str, lookahead: int = 0) -> bool:
        n = self.n + lookahead
        if n >= len(self.tokens):
            # don't allow lookahead beyond end of tokens, TODO: TBD if we should throw an error
            #  rather than just return False-- check how callers use this return value!
            #  (we won't for now because of a statement like x=5 at end of file: the parser
            #   will peek ahead past the 5 to see if there's a '+' or '*' operator and we don't
            #   want that to raise an exception, though in a proper program if that's the last
            #   statement in the program there should be a ';' after the 5 and that wouldn't fail)
            # raise RuntimeError("attempt to checkahead() beyond end of token list")
            return False
        else:
            return self.tokens[n].toktype == toktype

    def parse_statements(self) -> list[Statement]:
        statements = []
        # TODO: think about all the possible exit conditions
        while self.n < len(self.tokens) and not self.checkahead("RBRACE"):
            statements.append(self.parse_statement())
        return statements

    #######################################################
    # Parsing more general expressions and statements

    def parse_statement(self) -> Statement:
        if self.checkahead("PRINT"):
            if self.checkahead("STRCONST", 1):
                return self.parse_printstr()
            else:
                return self.parse_print()
        elif self.checkahead("VAR"):
            return self.parse_declare()
        elif self.checkahead("NAME") and self.checkahead("ASSIGN", 1):
            # If this token is a name and the next token is an '='
            return self.parse_assign()
        elif self.checkahead("IF"):
            return self.parse_if_elif()
        elif self.checkahead("WHILE"):
            return self.parse_while()
        elif self.checkahead("FOR"):
            return self.parse_for()
        elif self.checkahead("FUNC"):
            return self.parse_func()
        elif self.checkahead("RETURN"):
            return self.parse_return()
        else:
            # If none of the above, check if we have a single expression as statement, e.g. 1=1; or fn(5);
            # Note that this could incorrectly trigger on assignment statements such as x=1; except those were dispatched to parse_assign() earlier
            expr = self.parse_expression()
            #printcolor(expr)  # DEBUG
            self.expect("SEMI")
            return ExprStatement(expr)
            ## The below error handling is no longer relevant
            # raise SyntaxError(
            #     "(line %d, col %d) Unhandled Statement '%s'"
            #     % (self.tokens[self.n].sourceline, self.tokens[self.n].sourcecol, self.tokens[self.n].tokvalue)
            # )

    ## WORK IN PROGRESS
    # "A term can be a number like 1, a name like xyz, a parenthesized expression like (1),
    #    or a function call like f(x,y,z). TODO: a unary op term such as -5 or -x
    def parse_term(self) -> Expression:
        term = None
        if self.checkahead("LPAREN"):
            self.expect("LPAREN")
            term = self.parse_expression()
            self.expect("RPAREN")
        elif self.checkahead("INTEGER"):
            term = self.parse_integer()
        elif self.checkahead("SUB"):
            # unary negation operator since not in the middle of a binop expression
            # (if we were processing '5-4', this sectin of code would trigger on INTEGER not SUB, and then below would trigger on SUB)
            self.expect("SUB")
            term = self.parse_term()
            # raise SyntaxError("Error: Unary negation operator - not fully implemented, buggy, aborting")
            return Subtract(Integer(0), term)
        elif self.checkahead("NAME"):
            if self.checkahead("LPAREN", 1):
                term = self.parse_callfn()
            else:
                term = self.parse_name()
        else:
            raise SyntaxError(
                "(line %d, col %d) '%s [...]' not parseable as term"
                % (self.tokens[self.n].sourceline, self.tokens[self.n].sourcecol, self.tokens[self.n].tokvalue)
            )
        return term


    def parse_expression(self) -> Expression:
        # TODO: handle expressions more complex than a single term, and also () terms
        # Special cases: before returning term, see if it's part of a binary operation
        term = self.parse_term()
        # print(term) # debug
        if self.checkahead("PLUS"):
            self.expect("PLUS")
            term2 = self.parse_term()
            return Add(term, term2)
        elif self.checkahead("TIMES"):
            self.expect("TIMES")
            term2 = self.parse_term()
            return Multiply(term, term2)
        elif self.checkahead("SUB"):
            self.expect("SUB")
            term2 = self.parse_term()
            return Subtract(term, term2)
        elif self.checkahead("DIV"):
            self.expect("DIV")
            term2 = self.parse_term()
            return Divide(term, term2)
        elif self.checkahead("MOD"):
            self.expect("MOD")
            term2 = self.parse_term()
            return Modulo(term, term2)
        else:
            return term

    def parse_relation(self) -> Relation:
        # Look ahead one token to see what the comparison op is
        optype = self.tokens[self.n + 1].toktype
        if self.checkahead("EQ", 1):
            return self.parse_relation_eq()
        elif self.checkahead("LT", 1):
            return self.parse_relation_lt()
        elif self.checkahead("LTE", 1):
            return self.parse_relation_lte()
        elif self.checkahead("GT", 1):
            return self.parse_relation_gt()
        elif self.checkahead("GTE", 1):
            return self.parse_relation_gte()
        elif self.checkahead("NEQ", 1):
            return self.parse_relation_neq()
        else:
            raise SyntaxError(
                "(line %d, col %d) unknown comparison operator %s"
                % (self.tokens[self.n].sourceline, self.tokens[self.n].sourcecol, optype)
            )

    ###################################################
    ## Parsing specific expressions and statements

    def parse_print(self) -> Print:
        self.expect("PRINT")
        body = self.parse_expression()
        self.expect("SEMI")
        return Print(body)

    def parse_printstr(self) -> PrintStr:
        self.expect("PRINT")
        tok = self.expect("STRCONST")
        self.expect("SEMI")
        return PrintStr(tok.tokvalue)

    def parse_return(self) -> Return:
        self.expect("RETURN")
        body = self.parse_expression()
        self.expect("SEMI")
        return Return(body)

    def parse_declare(self) -> Declare:
        self.expect("VAR")
        var = self.expect("NAME")
        if self.checkahead("SEMI"):
            self.expect("SEMI")
            return Declare(Name(var.tokvalue))
        else:
            self.expect("ASSIGN")
            value = self.parse_expression()
            self.expect("SEMI")
            return DeclareValue(Name(var.tokvalue), value)

    def parse_assign(self) -> Assign:
        var = self.expect("NAME")
        self.expect("ASSIGN")
        value = self.parse_expression()
        self.expect("SEMI")
        return Assign(Name(var.tokvalue), value)

    def parse_while(self) -> While:
        self.expect("WHILE")
        test = self.parse_relation()
        self.expect("LBRACE")
        body = self.parse_statements()
        self.expect("RBRACE")
        return While(test, body)

    # for i=1,10 { }
    def parse_for(self) -> For:
        self.expect("FOR")
        var_init = self.expect("NAME")
        self.expect("ASSIGN")
        value_init = self.parse_expression()
        self.expect("COMMA")
        value_end = self.parse_expression()
        self.expect("LBRACE")
        body = self.parse_statements()
        self.expect("RBRACE")
        return For(Name(var_init.tokvalue), 
                   value_init,
                   value_end,
                   body)



    def parse_if_simple(self) -> IfElse:  # obsolete, replaced by more general below
        self.expect("IF")
        test = self.parse_relation()
        self.expect("LBRACE")
        ifbody = self.parse_statements()
        self.expect("RBRACE")
        if self.checkahead("ELSE"):
            self.expect("ELSE")
            self.expect("LBRACE")
            elsebody = self.parse_statements()
            self.expect("RBRACE")
        else:
            elsebody = []
        return IfElse(test, ifbody, elsebody)

    def parse_if_elif(self) -> IfElifElse:
        self.expect("IF")
        test = self.parse_relation()
        self.expect("LBRACE")
        ifbody = self.parse_statements()
        self.expect("RBRACE")
        eliflist = []
        while self.checkahead("ELIF"):
            self.expect("ELIF")
            eliftest = self.parse_relation()
            self.expect("LBRACE")
            elifbody = self.parse_statements()
            self.expect("RBRACE")
            eliflist.append(IfElse(eliftest, elifbody, []))
        elsebody = []
        if self.checkahead("ELSE"):
            self.expect("ELSE")
            self.expect("LBRACE")
            elsebody = self.parse_statements()
            self.expect("RBRACE")
        return IfElifElse(test, ifbody, eliflist, elsebody)

    def parse_func(self) -> Function:
        self.expect("FUNC")
        name = self.expect("NAME")
        self.expect("LPAREN")
        params = []
        while self.n < len(self.tokens) and not self.checkahead("RPAREN"):
            params.append(Name(self.expect("NAME").tokvalue))
            if not self.checkahead("RPAREN"):
                # if a ')' is not the following character, expect a comma... TODO: cleaner integration
                self.expect("COMMA")
        self.expect("RPAREN")
        self.expect("LBRACE")
        body = self.parse_statements()
        self.expect("RBRACE")
        return Function(Name(name.tokvalue), params, body)

    def parse_integer(self) -> Integer:
        tok = self.expect("INTEGER")
        return Integer(int(tok.tokvalue))

    def parse_name(self) -> Name:
        tok = self.expect("NAME")
        return Name(tok.tokvalue)

    def parse_callfn(self) -> CallFn:
        name = self.expect("NAME")
        self.expect("LPAREN")
        params = []
        while self.n < len(self.tokens) and not self.checkahead("RPAREN"):
            params.append(self.parse_expression())
            if not self.checkahead("RPAREN"):
                # if a ')' is not the following character, expect a comma... TODO: cleaner integration
                self.expect("COMMA")
        self.expect("RPAREN")
        return CallFn(Name(name.tokvalue), params)

    def parse_relation_eq(self) -> Relation:
        left = self.parse_expression()
        self.expect("EQ")
        right = self.parse_expression()
        return Relation(RelationOp("=="), left, right)

    def parse_relation_lt(self) -> Relation:
        left = self.parse_expression()
        self.expect("LT")
        right = self.parse_expression()
        return Relation(RelationOp("<"), left, right)

    def parse_relation_gt(self) -> Relation:
        left = self.parse_expression()
        self.expect("GT")
        right = self.parse_expression()
        return Relation(RelationOp(">"), left, right)

    def parse_relation_lte(self) -> Relation:
        left = self.parse_expression()
        self.expect("LTE")
        right = self.parse_expression()
        return Relation(RelationOp("<="), left, right)

    def parse_relation_gte(self) -> Relation:
        left = self.parse_expression()
        self.expect("GTE")
        right = self.parse_expression()
        return Relation(RelationOp(">="), left, right)

    def parse_relation_neq(self) -> Relation:
        left = self.parse_expression()
        self.expect("NEQ")
        right = self.parse_expression()
        return Relation(RelationOp("!="), left, right)


################################
# Parse from file

def parse_file(filename, debug: bool = False) -> Program:
    """Load filename, tokenize and parse it, return AST"""
    tokens = tokenize_file(filename, debug)
    # expand any includes if present
    tokens = expand_includes(tokens, os.path.dirname(filename))
    if debug:
        printcolor("-- PREPROCESSED, after processing and tokenizing any #includes:")
        pprint(tokens)
    # TODO: run preprocessor such as includes.py here, which will itself call tokenize_file()
    program = parse_program(tokens)
    if debug:
        printcolor("-- PARSED PROGRAM:")
        print(program)
        printcolor("-- FORMATTED PROGRAM:")
        print(format_program(program))
    return program


######################################################
# Tests (if run directly vs. imported as module)

if __name__ == "__main__":
    header = f"***  Running tests in {os.path.basename(__file__)}  ***"
    print("*" * len(header))
    print(header)
    print("*" * len(header))
    print("Testing individual parse functions, e.g. parse_print(), parse_while()")

    # assert Parser(tokenize("1 + 2")).parse_add() == Add(Integer(1), Integer(2))
    # assert Parser(tokenize("1 * 2")).parse_multiply() == Multiply(Integer(1), Integer(2))
    assert Parser(tokenize("1 == 2")).parse_relation_eq() == Relation(RelationOp("=="), Integer(1), Integer(2))
    assert Parser(tokenize("1 < 2")).parse_relation_lt() == Relation(RelationOp("<"), Integer(1), Integer(2))
    # assert Parser(tokenize("<")).parse_relation_op() == RelationOp("<")
    assert Parser(tokenize("1 < 2")).parse_relation() == Relation(RelationOp("<"), Integer(1), Integer(2))

    assert Parser(tokenize("print 1;")).parse_print() == Print(Integer(1))
    assert_equal_verbose(Parser(tokenize("print 1;")).parse_print(), Print(Integer(1)))
    assert Parser(tokenize("var x = 1;")).parse_declare() == DeclareValue(Name("x"), Integer(1))
    assert Parser(tokenize("var x;")).parse_declare() == Declare(Name("x"))
    assert Parser(tokenize("while 1 < 1 { }")).parse_while() == While(
        Relation(RelationOp("<"), Integer(1), Integer(1)), []
    )
    assert Parser(tokenize("x = 1;")).parse_assign() == Assign(Name("x"), Integer(1))
    assert Parser(tokenize("if 1 == 1 { } else { }")).parse_if_simple() == IfElse(
        Relation(RelationOp("=="), Integer(1), Integer(1)), [], []
    )
    assert Parser(tokenize("if 1 == 1 { } elif 1 == 2 { } elif 1 == 3 { } else { }")).parse_if_elif() == IfElifElse(
        Relation(RelationOp("=="), Integer(1), Integer(1)),
        [],
        [
            IfElse(Relation(RelationOp("=="), Integer(1), Integer(2)), [], []),
            IfElse(Relation(RelationOp("=="), Integer(1), Integer(3)), [], []),
        ],
        [],
    )
    assert Parser(tokenize("return 1;")).parse_return() == Return(Integer(1))
    assert_equal_verbose(Parser(tokenize("func f(x) { }")).parse_func(), Function(Name("f"), [Name("x")], []))

    assert_equal_verbose(Parser(tokenize("print 1;")).parse_statement(), Print(Integer(1)))

    # assert_equal_verbose(Parser(tokenize("func f(x) { }")).parse_func(), Function(Name("f"), [Name("xs")], []))  #intentional error

    printcolor("PASSED", ansicode.green)

    print("Testing generic parse_statement() for various inputs...")
    tests = {
        "print 1;": Print(Integer(1)),
        "var x = 1;": DeclareValue(Name("x"), Integer(1)),
        "var x;": Declare(Name("x")),
        "while 1 < 1 { }": While(Relation(RelationOp("<"), Integer(1), Integer(1)), []),
        "x = 1;": Assign(Name("x"), Integer(1)),
        "if 1 == 1 { } else { }": IfElifElse(Relation(RelationOp("=="), Integer(1), Integer(1)), [], [], []),
        "return 1;": Return(Integer(1)),
        "func f(x) { }": Function(Name("f"), [Name("x")], []),
        "while 1 < 1 { var x = 1; print 1; }": While(
            Relation(RelationOp("<"), Integer(1), Integer(1)),
            [DeclareValue(Name("x"), Integer(1)), Print(Integer(1))],
        ),
        "for i = 1, 2 { print i; }": For(Name("i"), Integer(1), Integer(2), [Print(Name("i"))]),
        "func f(x, y) { print 1; }": Function(Name("f"), [Name("x"), Name("y")], [Print(Integer(1))]),
        "x;": ExprStatement(Name("x")),
        "1 + 2;": ExprStatement(Add(Integer(1), Integer(2))),
        "(1 + 2);": ExprStatement(Add(Integer(1), Integer(2))),
        "f(5,x);": ExprStatement(CallFn(Name("f"), [Integer(5), Name("x")])),
        'print "hello x=5";': PrintStr("hello x=5"),
    }
    for text, tokens in tests.items():
        #print(Parser(tokenize(text)).parse_statement())
        assert_equal_verbose(Parser(tokenize(text)).parse_statement(), tokens)

    printcolor("PASSED", ansicode.green)

    print("Testing parse_expression()...")
    tests = {
        "1": Integer(1),
        "x": Name("x"),
        "f(5,x)": CallFn(Name("f"), [Integer(5), Name("x")]),
        "(1)": Integer(1),
        "(f(5,x))": CallFn(Name("f"), [Integer(5), Name("x")]),
        "1 + 2": Add(Integer(1), Integer(2)),
        "x + 5": Add(Name("x"), Integer(5)),
        "(3 + 4)": Add(Integer(3), Integer(4)),
        "(3 + 4) * 5": Multiply(Add(Integer(3), Integer(4)), Integer(5)),
        "1 - (2 / 3)": Subtract(Integer(1), Divide(Integer(2), Integer(3))),
        "-2": Subtract(Integer(0), Integer(2)),
        # though it's unclear if below is behavior we want, allowing double unary ops...
        "--2": Subtract(Integer(0), Subtract(Integer(0), Integer(2))),
        "-x": Subtract(Integer(0), Name("x")),
        "-(1 + 2)": Subtract(Integer(0), Add(Integer(1), Integer(2))),
        "3 + -4": Add(Integer(3), Subtract(Integer(0), Integer(4))),
        "-5 + 6": Add(Subtract(Integer(0), Integer(5)), Integer(6)),
        "5 % 3": Modulo(Integer(5), Integer(3)),
    }
    for text, tokens in tests.items():
        assert_equal_verbose(Parser(tokenize(text)).parse_expression(), tokens)

    printcolor("PASSED", ansicode.green)

    print("Testing Parser.parse_statements() and wrapper parse_program()...")
    assert_equal_verbose(
        Parser(tokenize("print 1; print xyz; print (2); print f(1, x, (2 * 3) + xyz);")).parse_statements(),
        [
            Print(Integer(1)),
            Print(Name("xyz")),
            Print(Integer(2)),
            Print(CallFn(Name("f"), [Integer(1), Name("x"), Add(Multiply(Integer(2), Integer(3)), Name("xyz"))])),
        ],
    )

    assert_equal_verbose(
        parse_program(tokenize("print 1; print xyz; print (2); print f(1, x, (2 * 3) + xyz);")),
        Program(
            [
                Print(Integer(1)),
                Print(Name("xyz")),
                Print(Integer(2)),
                Print(CallFn(Name("f"), [Integer(1), Name("x"), Add(Multiply(Integer(2), Integer(3)), Name("xyz"))])),
            ]
        ),
    )

    printcolor("PASSED", ansicode.green)

    print("Testing parse_program() on files in test/ folder...")

    tests = {
        "tests/program1.wb": Program(
            [
                DeclareValue(Name("x"), Integer(10)),
                Assign(Name("x"), Add(Name("x"), Integer(1))),
                Print(Add(Multiply(Integer(23), Integer(45)), Name("x"))),
            ]
        ),
        "tests/program2.wb": Program(
            [
                DeclareValue(Name("x"), Integer(3)),
                DeclareValue(Name("y"), Integer(4)),
                DeclareValue(Name("min"), Integer(0)),
                IfElifElse(
                    Relation(RelationOp("<"), Name("x"), Name("y")),
                    [Assign(Name("min"), Name("x"))],
                    [],
                    [Assign(Name("min"), Name("y"))],
                ),
                Print(Name("min")),
            ]
        ),
        "tests/program3.wb": Program(
            [
                DeclareValue(Name("result"), Integer(1)),
                DeclareValue(Name("x"), Integer(1)),
                While(
                    Relation(RelationOp("<"), Name("x"), Integer(10)),
                    [
                        Assign(Name("result"), Multiply(Name("result"), Name("x"))),
                        Assign(Name("x"), Add(Name("x"), Integer(1))),
                    ],
                ),
                Print(Name("result")),
            ]
        ),
        "tests/program4.wb": Program(
            [
                Function(
                    Name("add1"),
                    [Name("x")],
                    [Assign(Name("x"), Add(Name("x"), Integer(1))), Return(Name("x"))],
                ),
                DeclareValue(Name("x"), Integer(10)),
                Print(Add(Multiply(Integer(23), Integer(45)), CallFn(Name("add1"), [Name("x")]))),
                Print(Name("x")),
            ]
        ),
        "tests/elif.wb": Program(
            [
                DeclareValue(Name("x"), Integer(1)),
                IfElifElse(
                    Relation(RelationOp(">"), Name("x"), Integer(2)),
                    [Print(Integer(99))],
                    [
                        IfElse(Relation(RelationOp("=="), Name("x"), Integer(2)), [Print(Integer(2))], []),
                        IfElse(Relation(RelationOp("=="), Name("x"), Integer(1)), [Print(Integer(1))], []),
                    ],
                    [Print(Integer(0))],
                ),
            ]
        ),
    }
    rootpath = os.path.dirname(__file__)
    for inputfile, target in tests.items():
        prog = parse_file(os.path.join(rootpath,inputfile), debug=False)
        assert_equal_verbose(prog, target)

    printcolor("PASSED", ansicode.green)

    # demonstrate parser error messages
    testparseerrors = False
    if testparseerrors:
        print("Testing the parsing errors returned for some known-bad programs:")
        # test error messages (with line numbers?) returned when parsing various incorrect code
        tests = [
            "while 2 < 3 {\n  print 1 ;",  # missing closing brace
            "for i=1;i<5;i=i+1 {\n  print 1 ;",  # missing third semicolon
            "var x=5;\nx = 2 < 3;\nprint x;",  # comparison used as value / term
            "print 2 + 3;\nfoo;",  # standalone string foo (update: now valid as ExprStatement)
            "print if 2 < 3 {} else {};",
            "if 2 < 3 {\n  print 1;\n}\nprint 5;",  # missing else (update: now valid)
            "x +;",  # missing value after '+'
            "x+5=7;",  # invalid format
            "x+3",  # no semicolon
        ]
        for test in tests:
            print("\n" + test)
            try:
                parse_program(tokenize(test))
                printcolor(">>Did not find parsing error in this program (but expected one)", ansicode.red)
            except Exception as e:
                printcolor(">>Parsing error (as expected): %s" % e, ansicode.blue)
                # raise e
        # test parsing of wrong order of operations, which is incorrect syntax
        # print(parse_program(tokenize("print 2 + 3 * 4;\nprint 2 * 3 + 4;")))
