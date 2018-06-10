from constants import Commands, Value_type
from Utils import Stack


class Code_generator(object):
    def __init__(self, symbol_table, semantic_stack, memory_manager):
        self.symbol_table = symbol_table
        self.semantic_stack = semantic_stack
        self.memory_manager = memory_manager
        self.program_block = []
        self.program_block.append("")

    def add(self):
        tmp = self.memory_manager.get_temp(Value_type.INT)
        self.program_block.append(make_command(Commands.ADD,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def sub(self):
        tmp = self.memory_manager.get_temp(Value_type.INT)
        self.program_block.append(make_command(Commands.SUB,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def and_op(self):
        tmp = self.memory_manager.get_temp(Value_type.BOOL)
        self.program_block.append(make_command(Commands.AND,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)


    def assign(self):
        self.program_block.append(make_command(Commands.ASSIGN,
                                               self.semantic_stack[-1],
                                               self.semantic_stack[-2]))
        self.semantic_stack.pop(2)

    def eq(self):
        tmp = self.memory_manager.get_temp(Value_type.BOOL)
        self.program_block.append(make_command(Commands.EQ,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def jpf(self):
        self.program_block[self.semantic_stack[-1]] = make_command(Commands.JPF,
                                                                   self.semantic_stack[-2],
                                                                   len(self.program_block))
        self.semantic_stack.pop(2)

    def jp(self):
        self.program_block[self.semantic_stack[-1]] = make_command(Commands.JP,
                                                                   len(self.program_block))
        self.semantic_stack.pop(1)

    def lt(self):
        tmp = self.memory_manager.get_temp(Value_type.BOOL)
        self.program_block.append(make_command(Commands.LT,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def mult(self):
        tmp = self.memory_manager.get_temp(Value_type.INT)
        self.program_block.append(make_command(Commands.MULT,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def not_op(self):
        tmp = self.memory_manager.get_temp(Value_type.BOOL)
        self.program_block.append(make_command(Commands.NOT,
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop()
        self.semantic_stack.push(tmp)

    def print_op(self):
        self.program_block.append(make_command(Commands.PRINT,
                                               self.semantic_stack[-1]))
        self.semantic_stack.pop(1)

    def label(self):
        self.semantic_stack.push(len(self.program_block))

    def save(self):
        self.semantic_stack.push(len(self.program_block))
        self.program_block.append('')

    def end_while(self):
        self.program_block.append(make_command(Commands.JP,
                                               self.semantic_stack[-3]))
        self.program_block[self.semantic_stack[-1]] = make_command(Commands.JPF,
                                                                   self.semantic_stack[-2],
                                                                   len(self.program_block))
        self.semantic_stack.pop(3)

    def jpf_save(self):
        i = len(self.program_block)
        self.program_block[self.semantic_stack[-1]] = make_command(Commands.JPF,
                                                                   self.semantic_stack[-2],
                                                                   i+1)

        self.semantic_stack.pop(2)
        self.semantic_stack.push(i)
        self.program_block.append('')



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