# todo: comment
# todo: a[5] + 2
# todo: a = -x[4]   ->  handle error
# todo: if tokens have finished (after $)   ->  return error

import re
from constants import otherTokens
from constants import operators
from constants import keyWords
from constants import whitespace
from constants import openingTokens
from constants import Terminals
from constants import closingTokens
from error_handler import ErrorHandler, Scanner_error

# TODO: remove this
from symbolTable import Symbol_table

OTHER = "other_token"
ID = "ID"
NUM = "NUM"


# class state(object):
#     def __init__(self):
#         self.next = {}  # dictionry with key of Token and value of an state
#         self.sub_DFA_name = None



class Scanner(object):
    def __init__(self, file_name):
        self.symbolTable = Symbol_table()  # TODO: symbolTable should be input of scanner
        self.currentIndex = 0
        self.startTokenIndex = 0
        self.error_handler = ErrorHandler(self)
        input_file = open(file_name)
        self.inputCode = input_file.read()
        self.lastToken = None

    def get_char(self):
        if self.currentIndex >= len(self.inputCode):
            return -1
        char = self.inputCode[self.currentIndex]
        self.currentIndex += 1
        return char

    def get_back(self):
        self.currentIndex -= 1

    def get_next_token(self):
        if self.lastToken == "EOF":
            self.lastToken = "$"
            return "$" , "$"
        if self.lastToken == "$":
            self.error_handler.scanner_error("end of file", self.currentIndex)
            raise Scanner_error("")
        self.startTokenIndex = self.currentIndex
        char = self.get_char()
        if char == "=":
            return self.handle_equal()

        if char == "+" or char == "-":
            if self.lastToken in operators or self.lastToken in openingTokens or self.lastToken in otherTokens:
                return self.handle_num()
            else:
                return self.return_token(char, OTHER)

        elif char.isdigit():
            return self.handle_num()

        elif char in Terminals:
            return self.return_token(char , OTHER)

        elif char.isalpha():
            return self.handle_id()

        elif char == "/":
            return self.handle_comment()

        elif char in whitespace:
            return self.get_next_token()

        else:
            print("problem in input character")

    def handle_equal(self):
        nextChar = self.get_char()
        if nextChar == -1:
            return
        if nextChar == "=":
            currentToken = "=="
            return self.return_token("==", OTHER)
        else:
            self.get_back()
            return self.return_token("=", OTHER)

    def handle_num(self):
        currentNum = self.inputCode[self.currentIndex - 1]
        while self.inputCode[self.currentIndex - 1].isdigit() or self.inputCode[self.currentIndex - 1] == "+" or self.inputCode[self.currentIndex - 1] == "-":
            newChar = self.get_char()
            if newChar == -1:
                # print("end of file")
                # self.error_handler.scanner_error("Unexpected end of file" , self.currentIndex -1)
                # raise Scanner_error("Unexpected EOF.")
                return self.return_token(currentNum, NUM)
            if newChar.isdigit():
                currentNum += newChar
            elif newChar in Terminals or newChar in whitespace:
                self.get_back()
                return self.return_token(currentNum, NUM)
            else:
                self.error_handler.scanner_error("invalid character in number" , self.currentIndex)
                raise Scanner_error("")

    def handle_id(self):
        currentID = self.inputCode[self.currentIndex - 1]
        while self.inputCode[self.currentIndex - 1].isdigit() or self.inputCode[self.currentIndex - 1].isalpha():
            newChar = self.get_char()
            if newChar == -1:
                # print("end of file")
                return self.return_token(currentID, ID)
            if newChar.isdigit() or newChar.isalpha():
                currentID += newChar
            elif newChar in Terminals or newChar in whitespace:
                self.get_back()
                return self.return_token(currentID, ID)
            else:
                self.error_handler.scanner_error("invalid character in identifier" , self.currentIndex)
                raise Scanner_error("")

    def handle_comment(self):
        newChar = self.get_char()
        if newChar != "*":
            self.error_handler.scanner_error("invalid character" , self.currentIndex)
            raise Scanner_error("")

        newChar = self.get_char()
        while newChar != "*" and newChar != -1:
            newChar = self.get_char()
        if newChar == -1:
            self.error_handler.scanner_error("Unexpected end of file" , self.currentIndex -1)
            raise Scanner_error("")

        elif newChar == "*":
            newChar = self.get_char()
            if newChar == "/":
                return self.get_next_token()
            elif newChar == -1:
                self.error_handler.scanner_error("Unexpected end of file", self.currentIndex - 1)
                raise Scanner_error("")
            else:
                self.error_handler.scanner_error("invalid charactor", self.currentIndex)
                raise Scanner_error("")

    def return_token(self, token, type):  # type can be NUM , ID , OTHER
        self.lastToken = token
        if type == OTHER:
            # print("return token , ", token)
            return token , token
        elif type == NUM:
            # print("return number, ", token)
            return NUM , int(re.sub(r'[^\d-]+', '',token))

        elif type == ID:
            if token in keyWords:
                # print("return keyWord , ", token)
                # maybe error handling for this part
                return token , token
            else:
                # print("return identifier, ", token)
                # maybe error handling for this part
                return ID, self.symbolTable.find(token)
        else:
            print("problem: token is not in category: ", token)

    def get_place(self , place):
        return self.inputCode[:place].count('\n') + 1, place- self.inputCode[:place].rfind('\n')

