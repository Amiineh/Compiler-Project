
from TokenList import Tokens

class scanner(object):
    def __init__(self):
        self.currentIndex = 0
        self.startTokenIndex= 0
        input_file = open(file_name)
        self.inputCode = input_file.read()
        self.lastToken = None

    def get_char(self):
        char = self.inputFile[self.currentIndex]
        self.currentIndex +=1
        return char

    def get_next_token(self):
        return 2

    def return_token(self):
        return 4

