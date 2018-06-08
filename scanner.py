from TokenList import Tokens
from TokenList import otherTokens
from TokenList import operators
from TokenList import keyWords
from TokenList import whitespace

# TODO: remove this
from symbolTable import SymbolTable

OTHER = "other_token"
ID = "ID"
NUM = "NUM"


class state(object):
    def __init__(self):
        self.next = {}  # dictionry with key of Token and value of an state
        self.sub_DFA_name = None


file_name = "testFile.txt"


class scanner(object):
    def __init__(self):
        self.symbolTable = SymbolTable()  # TODO: symbolTable should be input of scanner
        self.currentIndex = 0
        self.startTokenIndex = 0
        input_file = open(file_name)
        self.inputCode = input_file.read()
        self.lastToken = None
        print(otherTokens)

        print("scanner creation")

    def get_char(self):
        if self.currentIndex >= len(self.inputCode):
            return -1
        char = self.inputCode[self.currentIndex]
        self.currentIndex += 1
        print("get new char , ", char, "index: ", self.currentIndex)
        return char

    def get_back(self):
        print("get back", "index: ", self.currentIndex)

        self.currentIndex -= 1

    def get_next_token(self):
        if self.lastToken == "EOF":
            return
        self.startTokenIndex = self.currentIndex
        char = self.get_char()
        if char == "=":
            self.handle_equal()

        if char == "+" or char == "-":
            if self.lastToken in operators or self.lastToken in otherTokens:
                print("charactor is number , ", char)
                self.handle_num()
            else:
                print("charactor is token , ", char)
                self.return_token(char, OTHER)

        elif char.isdigit():
            print("charactor is digit ", char)
            self.handle_num()

        elif char in otherTokens or char in operators:
            print("charactor is token , " , char)
            self.return_token(char , OTHER)

        elif char.isalpha():
            print("charactor is letter ", char)
            self.handle_id()

        elif char == "/":
            print("charactor is BACKSLASH")
            self.handle_comment()

        elif char in whitespace:
            print("whiteSpace")
            return self.get_next_token()

        else:
            print("problem in input charactor")

    def handle_equal(self):
        nextChar = self.get_char()
        if nextChar == -1:
            print("file ended , error in scanner. need NUM or ID after token =")
            return
        if nextChar == "=":
            currentToken = "=="
            self.return_token("==", OTHER)
        else:
            self.get_back()
            self.return_token("=", OTHER)

    def handle_num(self):
        currentNum = self.inputCode[self.currentIndex - 1]
        while self.inputCode[self.currentIndex - 1].isdigit() or self.inputCode[self.currentIndex - 1] == "+" or self.inputCode[self.currentIndex - 1] == "-":
            newChar = self.get_char()
            if newChar == -1:
                print("end of file")
                return self.return_token(currentNum, NUM)
            if newChar.isdigit():
                currentNum += newChar
            else:
                print("non digit character after a num")
                self.get_back()
                return self.return_token(currentNum, NUM)

    def handle_id(self):
        currentID = self.inputCode[self.currentIndex - 1]
        while self.inputCode[self.currentIndex - 1].isdigit() or self.inputCode[self.currentIndex - 1].isalpha():
            newChar = self.get_char()
            if newChar == -1:
                print("end of file")
                return self.return_token(currentID, ID)
            if newChar.isdigit() or newChar.isalpha():
                currentID += newChar
            else:
                print("non digit or letter character in an identifier")
                self.get_back()
                return self.return_token(currentID, ID)

    def handle_comment(self):
        print("handle comment")

    def return_token(self, token, type):  # type can be NUM , ID , OTHER
        self.lastToken = token
        if type == OTHER:
            print("return token , ", token)
            return token
        elif type == NUM:
            print("return number, ", token)
            return token
        elif type == ID:
            if token in keyWords:
                print("return keyWord , ", token)
                # maybe error handling for this part
                return token
            else:
                print("return identifier, ", token)
                # maybe error handling for this part
                return token, self.symbolTable.find(token)
        else:
            print("problem: token is not in category: ", token)


SC = scanner()
token = ""
while token != "EOF":
    token = SC.get_next_token()

