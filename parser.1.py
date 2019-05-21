import sys
from indent import Indent
import ast

class Parser:

    TYPE = ['INT', 'FLOAT', 'CHAR','BOOL']
    STATEMENT_STARTERS = ['SEMICOLON', 'LBRACE', 'IDENTIFIER', 'IF', 'WHILE']
    REL_OP = ['LT', 'LTE', 'GT', 'GTE']
    NUM_OP = ['ADD','SUB']
    MUL_OP = ['MUL', 'DIV']
    LITERAL = ['INTEGER_LIT', 'FLOAT_LIT', 'CHAR_LIT']
    declarations_count = 0
    def __init__(self, verbose=False):
        self.indentator = Indent(True)
        self.tokens = []
        self.errors = 0

    def show_next(self, n=1):
        try:
            return self.tokens[n - 1]
        except IndexError:
            print('ERROR: no more tokens left!')
            sys.exit(1)

    def expect(self, kind):
        actualToken = self.show_next()
        actualKind = actualToken.kind
        actualPosition = actualToken.position
        if actualKind == kind:
            return self.accept_it()
        else:
            print('Error at {}: expected {}, got {} instead'.format(str(actualPosition), kind, actualKind))
            sys.exit(1)

    # same as expect() but no error if not correct kind
    def maybe(self, kind):
        if self.show_next().kind == kind:
            return self.accept_it()

    def accept_it(self):
        token = self.show_next()
        output = str(token.kind) + ' ' + token.value
        self.indentator.say(output)
        return self.tokens.pop(0)

    def remove_comments(self):
        result = []
        in_comment = False
        for token in self.tokens:
            if token.kind == 'COMMENT':
                pass
            elif token.kind == 'LCOMMENT':
                in_comment = True
            elif token.kind == 'RCOMMENT':
                in_comment = False
            else:
                if not in_comment:
                    result.append(token)
        return result

    def parse(self, tokens):
        self.tokens = tokens
        self.tokens = self.remove_comments()
        self.parse_program()

    def parse_program(self):
        self.indentator.indent('Parsing Program')
        self.expect('INT')
        self.expect('IDENTIFIER')
        self.expect('LPAREN')
        self.expect('RPAREN')
        self.expect('LBRACE')
        self.parse_declarations()
        self.parse_statements()
        self.expect('RBRACE')
        self.indentator.dedent()
        if (self.errors == 1):
            print('WARNING: 1 error found!')
        elif (self.errors > 1):
            print('WARNING: ' + str(self.errors) + ' errors found!')
        else:
            print('parser: syntax analysis successful!')

    def parse_declaration(self): # done
        self.indentator.indent('Parsing Declaration')
        self.parse_type()
        self.expect('IDENTIFIER')
        if self.show_next().kind == 'LBRACK':
            self.accept_it()
            self.expect('INTEGER_LIT')
            self.expect('RBRACK')

        while self.show_next().kind == 'COMMA':
            self.accept_it()
            self.expect('IDENTIFIER')
            if self.show_next().kind == 'LBRACK':
                self.accept_it()
                self.expect('INTEGER_LIT')
                self.expect('RBRACK')
    
        self.expect('SEMICOLON')
        self.indentator.dedent()

    def parse_declarations(self): # done
        self.indentator.indent('Parsing Declarations')
        
        while self.show_next().kind in self.TYPE: 
             self.parse_declaration()
        self.indentator.dedent()
        

    def parse_type(self): # done
        # check what is the type of the identifier
        self.indentator.indent('Parsing Type')
        if self.show_next().kind in self.TYPE:
            self.accept_it()
        else:
            print("parsing error for type")
        self.indentator.dedent()
    
    def parse_statements(self): # done
        self.indentator.indent('Parsing Statements')

        # parse statement consist to check if there is a statement !
        while self.show_next().kind in self.STATEMENT_STARTERS:
            self.parse_statement()

        self.indentator.dedent()

    def parse_statement(self): # done
        self.indentator.indent('Parsing Statement')
        nextstatement = self.show_next().kind
        # parse statement consist to check if there is a statement !
        # ; | Block | Assignement | IfStatement | WhileStatement
        if nextstatement == 'SEMICOLON':
            self.expect('SEMICOLON')

        elif nextstatement == 'IDENTIFIER':
            self.parse_assignement_statement() 

        elif nextstatement == 'LBRACE':
            self.parse_block_statement()

        elif nextstatement == 'IF':
            self.parse_if_statement()

        elif nextstatement == 'WHILE':
            self.parse_while_statement()
        else:
            self.parse_expression()
        self.indentator.dedent() 

    def parse_assignement_statement(self): # done
        self.indentator.indent('Parsing Assignement Statement')
        self.expect('IDENTIFIER')
        if self.show_next().kind == 'LBRACK':
            self.accept_it()
            self.parse_expression()
            self.expect('RBRACK')
        
        # self.expect('ASSIGN')
        self.parse_expression()
        self.expect('SEMICOLON')
        self.indentator.dedent() 

    def parse_block_statement(self): #done
        self.indentator.indent('Block statement')
        self.expect('LBRACE')
        self.parse_statements()
        self.expect('RBRACE')
        self.indentator.dedent()
  
    def parse_if_statement(self): #done
        self.indentator.indent('Parsing if statement')
        self.expect('IF')
        self.expect('LPAREN')
        self.parse_expression()
        self.expect('RPAREN')
        self.parse_statement()
        if self.show_next().kind == 'ELSE':
            self.accept_it()
            self.parse_statement()
        self.indentator.dedent()

    def parse_while_statement(self): # done
        self.indentator.indent('Parsing While statement')
        self.expect('WHILE')
        self.expect('LPAREN')
        self.parse_expression()
        self.expect('RPAREN')
        self.parse_statement()
        self.indentator.dedent()

    def parse_expression(self): # done
        self.indentator.indent('parsing Expression')
        self.parse_conjunction()
        if (self.show_next().kind == 'DBAR'): 
            self.accept_it()
            self.parse_conjunction()
        self.indentator.dedent()

    def parse_conjunction(self): # done
        self.indentator.indent('parsing conjunction')
        self.parse_equality()
        if (self.show_next().kind == 'DAMPERSAND'):
            self.accept_it()
            self.parse_equality()
        self.indentator.dedent()


    def parse_equality(self): # done
        #self.indentator.indent('parsing equality')
        EQOP = ['EQ', 'NEQ']
        print(str(self.show_next().kind))
        lhs=self.parse_relation()
        if self.show_next().kind in EQOP:
            op=self.accept_it()
            rhs=self.parse_relation()
            return Binary(lhs,op,rhs)    
        return lhs

    def parse_relation(self): # done
        self.indentator.indent('parsing relation')
        e1=self.parse_addition()
        while self.show_next().kind in self.REL_OP:
            op=self.accept_it()
            e2=self.parse_addition()
            e1=Binary(e1,op,e2)
        return e1

    def parse_addition(self): # done
        self.indentator.indent('parsing addition')
        t1=self.parse_term()
        while self.show_next().kind in self.NUM_OP:
            op=self.accept_it()
            t2=self.parse_term()
            t1=lit(t1,op,t2)
        return e1
    def parse_term(self): # done
        self.indentator.indent('parsing term')
        e1=self.parse_factor()
        if self.show_next().kind in self.MUL_OP:
            term=self.accept_it()
            e2=self.parse_factor()
            e1=lit(e1,op,e2)
        return e1
        
        
    def parse_term(self): # done
        self.indentator.indent('parsing term')
        self.parse_factor()
        if self.show_next().kind in self.MUL_OP:
            self.accept_it()
            self.parse_factor()
        self.indentator.dedent()
        
    def parse_factor(self): # done
        self.indentator.indent('parsing factor')
        TAB = ['SUB', 'NOT']
        if self.show_next().kind in TAB:
            self.accept_it()
        self.parse_primary()

        self.indentator.dedent()
        
    def parse_primary(self): # done
        self.indentator.indent('parsing primary')
        # Identifier[[Expression]] | Literal | (Expression) | Type(Expression)
        if self.show_next().kind == 'IDENTIFIER':
            self.accept_it()
        elif self.show_next().kind == 'LBRACKET':
            self.accept_it()
            self.parse_expression()
            self.expect('RBRACKET')
        elif self.show_next().kind in self.LITERAL:
            self.accept_it()
        elif self.show_next().kind == "LPAREN":
            self.accept_it()
            self.parse_expression()
            self.expect('RPAREN')
        # else: 
            # sys.exit()
        self.indentator.dedent()
        
    '''
    def parse_lteral(self):
        self.self.indentator.indent('parsing literal')
        if (self.show_next().kind == "INTEGER_LIT" or self.show_next() == "FLOAT_LIT" or self.show_next().kind == "CHAR_LIT" or self.show_next().kind == "BOOLEAN_LIT"):
            self.accept_it()
        self.indentator.dedent()
    
    def parse_identifier(self):
        self.indentator.indent('parsing Identifier')
        # Letter { Letter | Digit }
        if(self.show_next().kind == "IDENTIFIER"):
            self.accept_it()
            while (
                self.show_next().kind == "IDENTIFIER" or 
                self.show_next().kind == "INTEGER_LIT"
                ):
                self.accept_it()
                self.indentator.dedent()
        else:
            sys.exit()
        self.indentator.dedent()
        '''