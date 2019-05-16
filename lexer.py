import re
import sys
from token import Token

regexExpressions = [
    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),
    (r'for\b', 'FOR'),
    (r'if\b', 'IF'),
    (r'else\b', 'ELSE'),
    (r'break\b', 'BREAK'),
    (r'while\b', 'WHILE'),
    (r'return\b', 'RETURN'),
    (r'struct\b', 'STRUCT'),
    (r'typedef\b', 'TYPEDEF'),
    (r'sizeof\b', 'SIZEOF'),
    (r'switch\b', 'SWITCH'),
    (r'case\b', 'CASE'),
    (r'default\b', 'DEFAULT'),
    (r'do\b', 'DO'),
    (r'void\b', 'VOID'),
    (r'goto\b', 'GOTO'),
    (r'int\b', 'INT'),
    (r'char\b', 'CHAR'),
    (r'short\b', 'SHORT'),
    (r'long\b', 'LONG'),
    (r'float\b', 'FLOAT'),
    (r'double\b', 'DOUBLE'),
    (r'signed\b', 'SIGNED'),
    (r'unsigned\b', 'UNSIGNED'),
    (r'\(', 'LPAREN'),
    (r'\)', 'RPAREN'),
    (r'\{', 'LBRACE'),
    (r'\}', 'RBRACE'),
    (r'\[', 'LBRACKET'),
    (r'\]', 'RBRACKET'),
    (r'\;', 'SEMICOLON'),
    (r'\:', 'COLON'),
    (r'\,', 'COMMA'),
    (r'\/\*', 'LCOMMENT'),
    (r'\*\/', 'RCOMMENT'),
    (r'\/\/(.*)', 'COMMENT'),
    (r'\.', 'DOT'),
    (r'\=\=', 'EQ'),
    (r'\=', 'ASSIGN'),
    (r'\+\+', 'ADDADD'),
    (r'\+\=', 'ADDEQ'),
    (r'\+', 'ADD'),
    (r'\-\-', 'SUBSUB'),
    (r'\-\=', 'SUBEQ'),
    (r'\-', 'SUB'),
    (r'\*', 'MUL'),
    (r'\%', 'MOD'), 
    (r'\/', 'DIV'),
    (r'\!\=', 'NEQ'),
    (r'\!', 'NOT'),
    (r'\|\|', 'DBAR'),
    (r'\<', 'LT'),
    (r'\<\=', 'LTE'),
    (r'\>', 'GT'),
    (r'\>\=', 'GTE'),
    (r'\&', 'AMPERSAND'),
    (r'\&\&', 'DAMPERSAND'),
    (r'\#', 'SHARP'),
    (r'[a-zA-Z]\w*', 'IDENTIFIER'),
    (r'\d+\.\d+', 'FLOAT_LIT'),
    (r'\d+', 'INTEGER_LIT'), # le '+' signifie 1 ou plus digit
    (r'\"[^\"]*\"', 'STRING_LIT'),
    (r'\'[^\"]*\'', 'CHAR_LIT'),
    (r'/^(?:(1|y(?:es)?|t(?:rue)?|on)|(0|n(?:o)?|f(?:alse)?|off))$/i', 'BOOLEAN_LIT'),
    (r'\w+(\.\w+)+', 'SELECTED_NAME')
]


class Lexer:

    def __init__(self):
        self.tokens = []

    # inputText = open("testFile.c").readlines()
    def lex(self, inputText):

        lineNumber = 0
        for line in inputText:
            lineNumber += 1
            position = 0
            while position < len(line):
                match = None
                for tokenRegex in regexExpressions:
                    pattern, tag = tokenRegex
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        data = match.group(0)
                        if tag:
                            token = Token(tag, data, [lineNumber, position])
                            self.tokens.append(token)
                        break
                if not match:
                    print(inputText[position])
                    print("no match")
                    sys.exit(1)
                else:
                    position = match.end(0)
        print("lexer: analysis successful!")
        return self.tokens