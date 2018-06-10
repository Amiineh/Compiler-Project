from constants import Value_type , ID_type
from error_handler import  Semantic_error
from Utils import Unit

class SemanticAnalyzer(object):
    def __init__(self, semantic_stack, symbol_table, error_handler, memory_manager):
        self.memory_manager = memory_manager
        self.semantic_stack = semantic_stack
        self.symbol_table = symbol_table
        self.error_handler = error_handler

    def open_scope(self, token):
        self.symbol_table.push_scope()

    def close_scope(self, token):
        self.symbol_table.pop_scope()

    def hide_upper_scopes(self , token):
        self.symbol_table.hide_upper_scopes = True

    def unhide_upper_scopes(self , token):
        self.symbol_table.hide_upper_scopes = False

    def push_stack(self , input):
        self.semantic_stack.push(input)

    def define_var(self , token):
        var = self.symbol_table.table[token]
        if var.type is not None:
            self.error_handler.semantic_error("%s is already defined in this scope." %(var.value), None )
            raise Semantic_error("")
        var.id_type = ID_type.VAR
        if self.semantic_stack.top().upper() is not Value_type.INT:
            self.error_handler.semantic_error("invalid type specifier for %s." %(var.value), None )
            raise Semantic_error("")
        var.type = self.semantic_stack.top().upper()
        self.semantic_stack.pop()
        var.address = self.memory_manager.get_temp(Value_type.INT)

    def check_array_size(self, token):
        if self.semantic_stack.top() <= 0:
            self.error_handler.semantic_error("invalid array size %s (cannot be negative)." % (self.semantic_stack.top()), None)
            raise Semantic_error("")

    def define_array(self, token):
        array_name = self.semantic_stack[-2]
        row = self.symbol_table.table[array_name]
        if row.type is not None:
            self.error_handler.semantic_error("%s is already defined in this scope." %(var.value), None )
            raise Semantic_error("")
        row.id_type = ID_type.VAR
        row.type = Value_type.POINTER
        row.pointed_type = Value_type.INT
        row.address = self.memory_manager.get_variable(row.type)
        row.size = self.semantic_stack.top()
        self.semantic_stack.pop(3)
        self.semantic_stack.push(array_name)

    def check_type(self , token):
        if self.semantic_stack[-1].type.upper() != self.semantic_stack[-2].type.upper():
            self.error_handler.semantic_error("invalid assign type" ,None)
            raise Semantic_error("")

    def push_variable(self , token):
        row = self.symbol_table.table[token]
        if row.type is None:
            self.error_handler.semantic_error("%s is not defined in this scope." % (row.value), None)
            raise Semantic_error("")
        if row.id_type != ID_type.VAR:
            self.error_handler.semantic_error("not a variable", None )
            raise Semantic_error("")
        self.semantic_stack.push(Unit(
            type = row.type,
            value = row.value
        ))

    def check_array_bound(self , token):
        if not (0 <= self.semantic_stack[-1].value < self.symbol_table.table[self.semantic_stack[-2]].size):
            self.error_handler.semantic_error("%s out of bound" %(self.semantic_stack[-1].value), None)
            raise Semantic_error("")

    def operation_type_check(self , token):
        # example a + b
        if self.semantic_stack[-1].type.upper() != self.semantic_stack[-3].type.upper():
            self.error_handler.semantic_error("invalid assign type" ,None)
            raise Semantic_error("")

    def push_immediate(self, token):
        imidiate = Unit(value  =token , addressing_mode="#" , type = Value_type.INT)
        self.semantic_stack.push(imidiate)

    def define_fun(self , token):
        row = self.symbol_table.table[token]
        if row.type is not None:
            self.error_handler.semantic_error("function %s has already been defined" %(str(row.value)), None)
            raise Semantic_error("")
        row.id_type = ID_type.FUN
        row.type = self.semantic_stack[-1]
        self.semantic_stack.pop()
        self.semantic_stack.push(token)
        row.arguments = []
        if row.type != Value_type.VOID:
            row.return_address = self.memory_manager.get_variable(row.type)
        else:
            row.return_address = None
        row.save_space = self.memory_manager.get_variable(Value_type.POINTER)

    def set_fun_arg(self, token):
        method_row = self.symbol_table.table[self.semantic_stack[-1]]
        row = self.symbol_table.table[token]
        method_row.arguments.append((row.value, row.type, row.address))

    def check_void_fun_return(self, token):
        row_index = self.semantic_stack[-2]
        row = self.symbol_table.table[row_index]
        if row.type != Value_type.VOID:
            self.error_handler.semantic_error("Unexpected return value", None)
            raise Semantic_error("")

    def check_int_fun_return(self, token):
        row_index = self.semantic_stack[-3]
        row = self.symbol_table.table[row_index]
        if row.type == Value_type.VOID:
            self.error_handler.semantic_error("Unexpected return value" , None)
            raise Semantic_error("")
        elif row.type != self.semantic_stack[-1].type:
            self.error_handler.semantic_error("Expected %s, got %s" %(row.type , self.semantic_stack[-1].type), None)
            raise Semantic_error("")

    def check_is_fun(self , token):
        fun = self.symbol_table.table[token]
        if fun.id_type != ID_type.FUN:
            self.error_handler.semantic_error("%s is not a function" %(str(fun.value)), None)
            raise Semantic_error("")

    def check_arg_count(self, token):
        method_row = self.symbol_table.table[self.semantic_stack[-2]]
        if self.semantic_stack[-1] != len(method_row.arguments):
            self.error_handler.semantic_error("too few arguman for function" , None)
            raise Semantic_error("")
        self.semantic_stack.pop(1)

    def push_arg_len(self, token):
        self.semantic_stack.push(0)

    def check_exist_arg(self, token):
        method_row = self.symbol_table.table[self.semantic_stack[-3]]
        arg_index = self.semantic_stack[-2]
        if arg_index >= len(method_row.arguments):
            self.error_handler.semantic_error("too many arguments for function", None)
            raise Semantic_error("")
        argument_name, argument_type, argument_address = method_row.arguments[arg_index]
        if self.semantic_stack[-1].type != argument_type:
            self.error_handler.semantic_error("Expected %s for %s but got %s" %(argument_type , argument_name , argument_address), None)
            raise Semantic_error("")
        self.semantic_stack[-2] += 1



