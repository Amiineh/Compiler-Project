from constants import Commands, Value_type
from Utils import Stack


class Code_generator(object):
    def __init__(self, symbol_table, semantic_stack, memory_manager):
        self.symbol_table = symbol_table
        self.semantic_stack = semantic_stack
        self.memory_manager = memory_manager
        self.program_block = []
        self.program_block.append("")

    def add(self, last_token):
        tmp = self.memory_manager.get_temp(Value_type.INT)
        self.program_block.append(make_command(Commands.ADD,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def sub(self, last_token):
        tmp = self.memory_manager.get_temp(Value_type.INT)
        self.program_block.append(make_command(Commands.SUB,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def and_operation(self, current_token):
        tmp = self.memory_manager.get_temp(Value_type.BOOL)
        self.program_block.append(make_command(Commands.AND,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def assign(self, last_token):
        self.program_block.append(make_command(Commands.ASSIGN,
                                               self.semantic_stack[-1],
                                               self.semantic_stack[-2]))
        self.semantic_stack.pop(2)

    def rel_equal(self, current_token):
        tmp = self.memory_manager.get_temp(Value_type.BOOL)
        self.program_block.append(make_command(Commands.EQ,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def rel_less(self, current_token):
        tmp = self.memory_manager.get_temp(Value_type.BOOL)
        self.program_block.append(make_command(Commands.LT,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def end_while(self, current_token):
        self.program_block.append(make_command(Commands.JP,
                                               self.semantic_stack[-3]))
        self.program_block[self.semantic_stack[-1]] = make_command(Commands.JPF,
                                                                   self.semantic_stack[-2],
                                                                   len(self.program_block))
        self.semantic_stack.pop(3)

    def label(self, current_token):
        self.semantic_stack.push(len(self.program_block))

    def save(self, current_token):
        self.semantic_stack.push(len(self.program_block))
        self.program_block.append('')

    def jpf_save(self, current_token):
        self.save(current_token)
        self.program_block[self.semantic_stack[-2]] = make_command(Commands.JPF,
                                                                   self.semantic_stack[-3],
                                                                   len(self.program_block))
        tmp = self.semantic_stack[-1]
        self.semantic_stack.pop(3)
        self.semantic_stack.push(tmp)

def make_command(command, first=None, second=None, third=None):
    row = "( " + command.value + ", " + str(first)
    if second is not None:
        row += ', ' + str(second)
    else:
        return row + ', , )'
    if third is not None:
        row += ', ' + str(third)
    else:
        return row + ', )'
    return row + " )"