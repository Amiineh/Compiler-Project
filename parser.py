import csv
from scanner import Scanner
import grammar
from error_handler import ErrorHandler
from constants import Non_Terminals

# todo: add try catch for scanner.get_next_token()

class Parser(object):
    def __init__(self, file_name):
        self.scanner = Scanner(file_name)
        self.error_handler = ErrorHandler(self.scanner)

        self.stack = [0]
        with open('parse_table.csv', 'r') as f:
            self.parse_table = [{k: v for k, v in row.items()}
                                for row in csv.DictReader(f, skipinitialspace=True)]
        self.next_token = None

    def run(self):
        while True:

            # print (self.stack)

            if self.next_token is None:
                self.next_token = self.scanner.get_next_token()

            action = self.parse_table[int(self.stack[-1])][self.next_token[0]]
            if action == 'acc':
                break

            if action == '':
                self.error_handler.report_error(self.next_token[0], "the rest of statement", self.scanner.startTokenIndex)
                self.error_handler_panic_mode()

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
                self.stack.append(self.parse_table[int(self.stack[-2])][self.stack[-1]])

    def is_empty_goto_table(self, state):
        for item in Non_Terminals:
            if self.parse_table[int(state)][item] is not '':
                return False
        return True

    def error_handler_panic_mode(self):
        while self.is_empty_goto_table(self.stack[-1]):
            self.stack.pop()
            self.stack.pop()

        while True:
            self.next_token = self.scanner.get_next_token()

            for non_terminal in Non_Terminals:
                if self.parse_table[int(self.stack[-1])][non_terminal] is not '' and \
                                self.next_token[0] in grammar.follow[non_terminal]:
                    self.stack.append(non_terminal)
                    self.stack.append(self.parse_table[int(self.stack[-2])][self.stack[-1]])
                    # self.next_token = self.scanner.get_next_token()
                    return

            # self.next_token = self.scanner.get_next_token()

if __name__ == "__main__":
    parser = Parser('./--tests--/17.cpp')
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


