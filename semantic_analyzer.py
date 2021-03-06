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
        self.semantic_stack.push(input[1])

    def define_var(self , token):
        var = self.symbol_table.table[int(token[1])]
        if var.type is not None:
            self.error_handler.semantic_error("%s is already defined in this scope" %(var.value), None )
            raise Semantic_error("")
        var.id_type = ID_type.VAR
        tmp_type = self.semantic_stack.top()
        if tmp_type != 'int':
            self.error_handler.semantic_error("invalid type specifier for %s" %(var.value), None )
            raise Semantic_error("")
        var.type = Value_type.INT
        self.semantic_stack.pop()
        self.semantic_stack.push(token[1])
        var.address = self.memory_manager.get_temp(Value_type.INT)

    def check_array_size(self, token):
        if self.semantic_stack.top() <= 0:
            self.error_handler.semantic_error("invalid array size %s (cannot be negative)" % (self.semantic_stack.top()), None)
            raise Semantic_error("")

    def define_array(self, token):
        array_name = self.semantic_stack[-2]
        row = self.symbol_table.table[array_name]
        if row.type is not None:
            self.error_handler.semantic_error("%s is already defined in this scope" %(row.value), None )
            raise Semantic_error("")
        row.id_type = ID_type.VAR
        row.type = Value_type.POINTER
        row.pointed_type = Value_type.INT
        row.address = self.memory_manager.get_temp(row.type)
        row.size = self.semantic_stack.top()
        self.semantic_stack.pop(3)
        self.semantic_stack.push(array_name)

    def check_type(self , token):
        if str(self.semantic_stack[-1].type).upper() != str(self.semantic_stack[-2].type).upper():
            self.error_handler.semantic_error("invalid assign type" ,None)
            raise Semantic_error("")

    def push_variable(self , token):
        row = self.symbol_table.table[int(token[1])]
        if row.type is None:
            self.error_handler.semantic_error("%s is not defined in this scope" % (row.value), None)
            raise Semantic_error("")
        if row.id_type != ID_type.VAR:
            self.error_handler.semantic_error("not a variable", None )
            raise Semantic_error("")
        self.semantic_stack.push(Unit(
            addressing_mode='',
            type = row.type,
            value = token[1]
        ))

    def check_array_bound(self , token):
        if not (0 <= self.semantic_stack[-1].value < self.symbol_table.table[self.semantic_stack[-2]].size):
            self.error_handler.semantic_error("%s out of bound" %(self.semantic_stack[-1].value), None)
            raise Semantic_error("")

    def operation_type_check(self , token):
        # example a + b
        if str(self.semantic_stack[-1].type).upper() != str(self.semantic_stack[-3].type).upper():
            self.error_handler.semantic_error("invalid assign type" ,None)
            raise Semantic_error("")

    def push_immediate(self, token):
        imidiate = Unit(value  =token[1] , addressing_mode="#" , type = Value_type.INT)
        self.semantic_stack.push(imidiate)

    def define_fun(self , token):
        row = self.symbol_table.table[int(token[1])]
        if row.type is not None:
            self.error_handler.semantic_error("function %s has already been defined" %(str(row.value)), None)
            raise Semantic_error("")
        row.id_type = ID_type.FUN
        row.type = str(self.semantic_stack[-1]).upper()
        self.semantic_stack.pop()
        self.semantic_stack.push(token[1])
        if row.arguments is None:
            row.arguments = []
        if str(row.type).upper() != 'VOID':
            row.return_address = self.memory_manager.get_temp(row.type)
        else:
            row.return_address = None
        row.save_space = self.memory_manager.get_temp(Value_type.POINTER)

    def set_fun_arg(self, token):
        method_row = self.symbol_table.table[self.semantic_stack[-1]]
        row = self.symbol_table.table[token[1]]
        if method_row.arguments is None:
            method_row.arguments = []
        method_row.arguments.append((row.value, row.type, row.address))

    def check_void_fun_return(self, token):
        row_index = self.semantic_stack[-2]
        row = self.symbol_table.table[row_index]
        if str(row.type).upper() != 'VOID':
            self.error_handler.semantic_error("Unexpected return value", None)
            raise Semantic_error("")

    def check_int_fun_return(self, token):
        row_index = self.semantic_stack[-2]
        row = self.symbol_table.table[row_index]
        if str(row.type).upper() == 'VOID':
            self.error_handler.semantic_error("Expected return value" , None)
            raise Semantic_error("")
        elif row.type != self.semantic_stack[-1].type:
            self.error_handler.semantic_error("Expected %s, got %s" %(row.type , self.semantic_stack[-1].type), None)
            raise Semantic_error("")

    def check_is_fun(self , token):
        fun = self.symbol_table.table[int(token[1])]
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
        method_row = self.symbol_table.table[self.semantic_stack[-2]]
        arg_index = self.semantic_stack[-2]
        if arg_index >= len(method_row.arguments):
            self.error_handler.semantic_error("too many arguments for function", None)
            raise Semantic_error("")
        argument_name, argument_type, argument_address = method_row.arguments[arg_index]
        if self.semantic_stack[-1].type != argument_type:
            self.error_handler.semantic_error("Expected %s for %s but got %s" %(argument_type , argument_name , argument_address), None)
            raise Semantic_error("")
        self.semantic_stack[-2] += 1

    def check_main(self, last_token):
        main_row_index = self.symbol_table.find("main")
        main_row = self.symbol_table.table[main_row_index]
        if main_row.id_type != ID_type.FUN:
            self.error_handler.semantic_error(
                "no main function found" , None)
            raise Semantic_error("")
        elif len(main_row.arguments) != 0:
            self.error_handler.semantic_error(
                "Unexpected argument for main" , None)
            raise Semantic_error("")
        elif main_row.type != 'VOID':
            self.error_handler.semantic_error(
                "invalid type specified for main" , None)
            raise Semantic_error("")

    def check_int_argument(self , token):
        if self.semantic_stack[-1].type != Value_type.INT:
            self.error_handler.semantic_error(
                "Expected int as argument of output function in c_minuus", None)
