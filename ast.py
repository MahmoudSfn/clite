class AST:
    def __init__(self, name):
        self.name = name

    def accept(self, visitor, arg):
        nom = self.__class__.__name__
        nomMethode = getattr(visitor, "visit" + nom)
        nomMethode(self, arg)

class Type(Ast):
    def __init__(self):
        self.val = None
        
    def __str__(self):
        return "type - {0}".format(self.val)

# types declaration:
class Int(AST):
    def __init__(self,val):
        self.val = val
    def __str__(self):
        return "int - {0}".format(self.val)

class Double(AST):
    def __init__(self,val):
        self.val = val
    def __str__(self):
        return "double - {0}".format(self.val)

class Float(AST):
    def __init__(self,val):
        self.val = val
    def __str__(self):
        return "float - {0}".format(self.val)

class Bool(AST):
    def __init__(self,val):
        self.val = val
    def __str__(self):
        return "float - {0}".format(self.val)
# endtypes

class Node(AST):
    def __init__(self):

    def __str__(self):

class Expression(AST):
    def __init__(self):
        self.simpleExpr = []
        self.operateurs = []
    
    def __str__(self):
        string = "Expression "
        i = 0
        for exp in self.simpleExpr:
            string = string + "\n   " + "{0}".format(exp)
            if(i<len(self.operateurs)):
                string = string + "\n   " + "{0}".format(self.operateurs)
            i+=1
        return string

class Assignment(AST):
    def __init__(self, left):
        self.left = left
        self.args = []
        self.operateurs = []

    def __str__(self):
        string = "Assignement "+"{0}".format(self.left)
        i=0
        for arg in self.args:
            string = string + "\n   " + "{0}".format(arg)
            if(i<len(self.operateurs)):
                string = string + "\n   " + "{0}".format(self.operateurs)
        return string

class IfStatement(Ast):
    def __init__(self,val):
        self.condition = val
        self.statements = []
        
    def __str__(self):
        string = "if\n condition - {0}".format(self.condition)
        for statement in self.statements:
            string = string + "\n - {0}".format(statement)
        return string

class ForStatement(Ast):
    def __init__(self, statement, expression):
        self.stmt = statement
        self.expr = expression
        self.statements = []
    
    def __str__(self):
        string = "for\n {0} {1} {2}".format(self.stmt, self.expr)
        for stmt in self.statements:
            string = string +"\n - {0}".format(stmt)
        return string

class WhileStatement(Ast):
    def __init__(self, expr):
        self.expr = expr
        self.statements = []
    def __str__(self):
        string = "while\n - {0}".format(self.expr)
        for stmt in self.statements:
            string = string + "\n - {0}".format(stmt)
        return string