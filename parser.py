import csv
from scanner import Scanner
import grammar
from TokenList import Non_Terminals


class Parser(object):
    def __init__(self, file_name):
        self.scanner = Scanner(file_name)
        self.stack = [0]
        with open('parse_table.csv', 'r') as f:
            self.parse_table = [{k: v for k, v in row.items()}
                                for row in csv.DictReader(f, skipinitialspace=True)]
        self.next_token = None

    def run(self):
        while True:

            print (self.stack)


            if self.next_token is None:
                try:
                    self.next_token = self.scanner.get_next_token()
                except:
                    # todo: scanner error
                    return 1

            
            action = self.parse_table[self.stack[-1]][self.next_token[0]]
            print ("action: ", action)
            if action == '':
                # todo: error handler
                return 1

            elif action[0] is 's':
                # shift:
                self.stack.append(self.next_token[0])
                self.stack.append(int(action[1:]))
                self.next_token = None

            elif action[0] is 'r':
                # reduce
                for _ in range(2*len(grammar.RHS[int(action[1:])])):
                    self.stack.pop()
                self.stack.append(grammar.LHS[int(action[1:])])
                self.stack.append(int(self.parse_table[self.stack[-2]][self.stack[-1]]))


if __name__ == "__main__":
    parser = Parser('./--tests--/testFile.txt')
    parser.run()

    # import sys
    # if len(sys.argv) != 2:
    #     print("Usage: python parser.py filename")
    #     exit(1)
    # import os
    # if not os.path.exists(sys.argv[1]):
    #     print("File does not exists")
    #     exit(1)
    # try:
    #     Parser(sys.argv[1]).run()
    # except (OSError, UnicodeDecodeError):
    #     print("Invalid file")
    #     exit(1)


