from enum import Enum

# class Tokens(Enum) :
#     EOF = 'EOP'
#     ID = 'ID'
#     SEMICOLON = ';'
#     OPEN_BRACKET = '['
#     CLOSE_BRACKET = ']'
#     NUM = 'NUM'
#     INT = 'int'
#     VOID = 'void'
#     OPEN_PARENTHESES = '('
#     CLOSE_PARENTHESES = ')'
#     OPEN_CURLY_BRACKET = '{'
#     CLOSE_CURLY_BRACKET = '}'
#     IF = "if"
#     ELSE = "else"
#     WHILE = "while"
#     RETURN = "return"
#     LESS = "<"
#     EQUAL_EQUAL = "=="
#     PLUS = "+"
#     MINUS = "-"
#     MULT = "*"
#     COLON = ","
#     EQUAL = "="

Non_Terminals = ['declaration','params','compound_stmt','declaration_list',
                 'expression_stmt','fun_declaration','statement','selection_stmt',
                 'iteration_stmt','var','simple_expression','local_declarations','term','addop','relop',
                 'program','additive_expression','return_stmt','statement_list','factor',
                 'var_declaration','param','expression','param_list','call','args','arg_list']

Terminals = ['(',')','*','+','"','"','-',';','<','=', '[', ']', 'ID','EOF','if','int','NUM','==','return','else',
             'void','while','{','}','$', ',']


keyWords = {"EOF" , "int" , "void" , "if" , "else" , "while" , "return"}
operators = {"+" , "-" , "=" , "*" , "<" , "=="}
openingTokens = {"[" , "(" , "{"}
closingTokens = {"]" , ")" , "}"}
otherTokens = {";" , "," }
whitespace = {"\n" , " " , "\t" , "\r"}

class Commands(Enum):
    ADD = 'ADD'
    SUB = 'SUB'
    AND = 'AND'
    ASSIGN = 'ASSIGN'
    EQ = 'EQ'
    JPF = 'JPF'
    JP = 'JP'
    LT = 'LT'
    MULT = 'MULT'
    NOT = 'NOT'
    PRINT = 'PRINT'

class Value_type(Enum):
    VOID = "VOID"
    INT = "INT"
    BOOL = "BOOL"