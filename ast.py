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


class (AST):
    def __init__(self):

    def __str__(self):


class (AST):
    def __init__(self):

    def __str__(self):