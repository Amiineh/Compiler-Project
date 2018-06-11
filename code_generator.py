from constants import Commands, Value_type
from Utils import Stack, Unit


class Code_generator(object):
    def __init__(self, symbol_table, semantic_stack, memory_manager):
        self.symbol_table = symbol_table
        self.semantic_stack = semantic_stack
        self.memory_manager = memory_manager
        self.program_block = []
        self.program_block.append("")

    def add(self):
        self.semantic_stack.push(Commands.ADD)

    def sub(self):
        self.semantic_stack.push(Commands.SUB)

    def assign(self):
        self.program_block.append(make_command(Commands.ASSIGN,
                                               self.semantic_stack[-1],
                                               self.semantic_stack[-2]))
        self.semantic_stack.pop(2)

    def eq(self):
        tmp = Unit(addressing_mode='', value=self.memory_manager.get_temp(Value_type.INT), type=Value_type.INT)
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
        tmp = Unit(addressing_mode='', value=self.memory_manager.get_temp(Value_type.INT), type= Value_type.INT)
        self.program_block.append(make_command(Commands.LT,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(tmp)

    def mult(self):
        tmp = Unit(addressing_mode='', value=self.memory_manager.get_temp(Value_type.INT), type=Value_type.INT)
        self.program_block.append(make_command(Commands.MULT,
                                               self.semantic_stack[-2],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(2)
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
        self.program_block.append(None)
        self.program_block[self.semantic_stack[-1]] = make_command(Commands.JPF,
                                                                   self.semantic_stack[-2],
                                                                   Unit(addressing_mode='#',
                                                                        value=len(self.program_block),
                                                                        type=Value_type.POINTER))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(i)

    def execute(self):
        tmp = Unit(addressing_mode='', value=self.memory_manager.get_temp(Value_type.INT), type=Value_type.INT)
        self.program_block.append(make_command(self.semantic_stack[-2],
                                               self.semantic_stack[-3],
                                               self.semantic_stack[-1],
                                               tmp))
        self.semantic_stack.pop(3)
        self.semantic_stack.push(tmp)

    def allocate_array(self):
        row = self.symbol_table.table[self.semantic_stack.top()]
        array_begin = self.memory_manager.get_temp(row.pointed_type, count=row.size)
        self.program_block.append(make_command(Commands.ASSIGN,
                                               Unit(addressing_mode='#',
                                                    value=array_begin,
                                                    type=Value_type.POINTER),
                                               Unit(addressing_mode='',
                                                    value=row.address,
                                                    type=Value_type.POINTER),))
        self.semantic_stack.pop()

    def push_array(self):
        arr_indx_adrs = self.memory_manager.get_temp(Value_type.POINTER)
        var_adrs = self.memory_manager.get_temp(Value_type.POINTER)
        arr_index = self.semantic_stack[-1]
        row = self.symbol_table.table[self.semantic_stack[-2]]
        self.program_block.append(make_command(Commands.MULT,
                                               arr_index,
                                               Unit(addressing_mode='#',
                                                    value=row.pointed_type.size,
                                                    type=Value_type.INT),
                                               Unit(addressing_mode='',
                                                    value=arr_indx_adrs,
                                                    type=Value_type.POINTER)))
        self.program_block.append(make_command(Commands.ADD,
                                               Unit(addressing_mode='',
                                                    value=row.address,
                                                    type=row.type),
                                               Unit(addressing_mode='',
                                                    value=arr_indx_adrs,
                                                    type=Value_type.POINTER),
                                               Unit(addressing_mode='',
                                                    value=var_adrs,
                                                    type=Value_type.POINTER)))
        self.semantic_stack.pop(2)
        self.semantic_stack.push(Unit(addressing_mode='@', value=var_adrs, type=row.pointed_type))

    def set_fun_address(self):
        row = self.symbol_table.table[self.semantic_stack[-1]]
        self.semantic_stack.push(len(self.program_block))
        if row.value != "main" :
            self.program_block.append(None)
        row.address = len(self.program_block)

    def jp_fun(self):
        row = self.symbol_table.table[self.semantic_stack[-2]]
        # TODO: why do we need jump anyway?
        self.program_block.append(make_command(Commands.JP,
                                               Unit(addressing_mode='',
                                                    value=row.save_space,
                                                    type=row.type)))
        if row.value != "main":
            self.program_block[self.semantic_stack[-1]] = make_command(Commands.JP,
                                                                       Unit(addressing_mode='#',
                                                                            value=len(self.program_block),
                                                                            type=Value_type.POINTER))
        self.semantic_stack.pop(2)

    def return_void_fun(self):
        row = self.symbol_table.table[self.semantic_stack[-2]]
        self.program_block.append(make_command(Commands.JP,
                Unit(addressing_mode='',
                     value=row.save_space,
                     type=row.type),))

    def return_int_fun(self):
        row = self.symbol_table.table[self.semantic_stack[-3]]
        self.program_block.append(make_command(Commands.ASSIGN,
                                               self.semantic_stack[-1],
                                               Unit(addressing_mode='',
                                                    value=row.return_address,
                                                    type=row.type),))
        self.program_block.append(make_command(Commands.JP,
                                               Unit(addressing_mode='',
                                                    value=row.save_space,
                                                    type=row.type)))
        self.semantic_stack.pop()

    def call_fun(self):
        method_row_index = self.semantic_stack[-1]
        self.semantic_stack.pop()
        row = self.symbol_table.table[method_row_index]
        self.program_block.append(make_command(Commands.ASSIGN,
                                               Unit(addressing_mode='#',
                                                    value=len(self.program_block) + 2,
                                                    type=Value_type.POINTER),
                                               Unit(addressing_mode='',
                                                    value=row.save_space,
                                                    type=Value_type.POINTER)))
        self.program_block.append(make_command(Commands.JP,
                                               Unit(addressing_mode='#',
                                                    value=row.address,
                                                    type=Value_type.POINTER)))
        if row.type != Value_type.VOID:
            tmp_var = self.memory_manager.get_variable(row.type)
            self.program_block.append(make_command(Commands.ASSIGN,
                                                   Unit(addressing_mode='',
                                                        value=row.return_address,
                                                        type=row.type),
                                                   Unit(addressing_mode='#',
                                                        value=tmp_var,
                                                        type=row.type)
                                                   ))
            self.semantic_stack.push(Unit(addressing_mode='', value=tmp_var, type=row.type))
        else:
            self.semantic_stack.push(Unit(addressing_mode='', value=row.return_address, type=row.type))

    def set_arg(self):
        val = self.semantic_stack[-1]
        arg_index = self.semantic_stack[-2] - 1
        method_row_index = self.semantic_stack[-3]
        method_row = self.symbol_table.table[method_row_index]
        arg_name, arg_type, arg_address = method_row.arguments[arg_index]
        self.program_block.append(make_command(Commands.ASSIGN,
                                               val,
                                               Unit(addressing_mode='',
                                                    value=arg_address,
                                                    type=arg_type)))
        self.semantic_stack.pop()

def make_command(command, first=None, second=None, third=None):
    row = "( " + command.value + ", " + str(first.value)
    if second is not None:
        row += ', ' + str(second.value)
    else:
        return row + ', , )'
    if third is not None:
        row += ', ' + str(third.value)
    else:
        return row + ', )'
    return row + " )"