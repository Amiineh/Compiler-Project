import csv
from scanner import Scanner
import grammar
from error_handler import ErrorHandler, Scanner_error, Semantic_error
from constants import Non_Terminals
from semantic_analyzer import SemanticAnalyzer
from Utils import Stack
from symbolTable import Symbol_table
from memory_manager import MemoryManager


class Parser(object):
    def __init__(self, file_name):
        self.scanner = Scanner(file_name)
        self.error_handler = ErrorHandler(self.scanner)
        self.semantic_stack = Stack()
        self.symbol_table = Symbol_table()
        self.memory_manager = MemoryManager(start= 1000)
        self.semantic_analyzer = SemanticAnalyzer(semantic_stack=self.semantic_stack ,
                                                  memory_manager= self.memory_manager ,
                                                  symbol_table= self.symbol_table ,
                                                  error_handler= self.error_handler)
        self.stack = [0]
        with open('parse_table.csv', 'r') as f:
            self.parse_table = [{k: v for k, v in row.items()}
                                for row in csv.DictReader(f, skipinitialspace=True)]
        self.next_token = None

    def run(self):
        error_detected = False
        while True:
            if self.next_token is None:
                try:
                    self.next_token = self.scanner.get_next_token()
                except Scanner_error as err:
                    self.error_handler.simple_error(err.args[0])
                    return 1

            action = self.parse_table[int(self.stack[-1])][self.next_token[0]]
            if action == 'acc':
                if not error_detected:
                    self.print_to_output()
                    return 0
                return 2

            if action == '':
                self.error_handler.report_error(self.next_token[0], "the rest of statement",
                                                self.scanner.startTokenIndex)
                error_detected = True
                try:
                    self.error_handler_panic_mode()
                except Scanner_error as err:
                    self.error_handler.simple_error(err.args[0])
                    return 1

            elif action[0] is 's':
                # shift:
                self.stack.append(self.next_token[0])
                self.stack.append(int(action[1:]))
                self.next_token = None

            elif action[0] is 'r':
                # reduce
                grammar_num = int(action[1:])
                for _ in range(2 * len(grammar.RHS[grammar_num])):
                    self.stack.pop()
                self.stack.append(grammar.LHS[int(action[1:])])
                self.stack.append(self.parse_table[int(self.stack[-2])][self.stack[-1]])

                if not error_detected:
                    for action in grammar.actions[grammar_num]:
                        if action[0] == '#':
                            eval("self.code_generator.%s(self.scanner.last_token)" % action[1:])
                        elif action[0] == '@':
                            try:
                                eval("self.semantic_analyzer.%s(self.scanner.last_token)" % action[1:])
                            except Semantic_error as err:
                                self.error_handler.error(err.args[0], self.scanner.startTokenIndex)
                                error_detected = True

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
            try:
                self.next_token = self.scanner.get_next_token()
            except Scanner_error as err:
                raise err

            for non_terminal in Non_Terminals:
                if self.parse_table[int(self.stack[-1])][non_terminal] is not '' and \
                        self.next_token[0] in grammar.follow[non_terminal]:
                    self.stack.append(non_terminal)
                    self.stack.append(self.parse_table[int(self.stack[-2])][self.stack[-1]])
                    return

    def print_to_output(self):
        # todo
        pass


if __name__ == "__main__":
    # for i in range(1, 19):
    #     print ('\n' + str(i))
        parser = Parser('./__tests__/' + str(1) +'.cpp')
        parser.run()
#
#     import sys
#     if len(sys.argv) != 2:
#         print("Usage: python parser.py filename")
#         exit(1)
#     import os
#     if not os.path.exists(sys.argv[1]):
#         print("File does not exists")
#         exit(1)
#     try:
#         Parser(sys.argv[1]).run()
#     except (OSError, UnicodeDecodeError):
#         print("Invalid file")
#         exit(1)
