from enum import Enum

class Tokens(Enum) :
    EOF = 'EOP'
    ID = 'ID'
    SEMICOLON = ';'
    OPEN_BRACKET = '['
    CLOSE_BRACKET = ']'
    NUM = 'NUM'
    INT = 'int'
    VOID = 'void'
    OPEN_PARENTHESES = '('
    CLOSE_PARENTHESES = ')'
    OPEN_CURLY_BRACKET = '{'
    CLOSE_CURLY_BRACKET = '}'
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    RETURN = "return"
    LESS = "<"
    EQUAL_EQUAL = "=="
    PLUS = "+"
    MINUS = "-"
    MULT = "*"
    COLON = ","
    EQUAL = "="
