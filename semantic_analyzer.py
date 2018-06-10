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

    def check_assign_type(self , token):
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
            memory_address = row.address,
            value = row.value
        ))






