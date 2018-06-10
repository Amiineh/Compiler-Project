from Utils import Stack

class Symbol_table_row(object):
    def __init__(self, value):
        self.value = value
        self.type = None
        self.address = None
        self.id_type = None
        self.pointed_type = None
        self.arguments = None
        self.return_address = None
        self.save_space = None

class Symbol_table(object):
    def __init__(self):
        self.table = []
        self.scope_stack = Stack()
        self.scope_stack.push(0)
        self.hide_upper_scopes = False

    def find(self, id_value):
        if not self.hide_upper_scopes:
            for item in reversed(self.table):
                if item.value == id_value:
                    return self.table.index(item)
        else:
            for item in self.table[self.scope_stack.top()]:
                if item.value == id_value:
                    return self.table.index(item)
        new_id = Symbol_table_row(id_value)
        self.table.append(new_id)
        return self.table.index(new_id)

    def push_scope(self):
        self.scope_stack.push(len(self.table))

    def pop_scope(self):
        while len(self.table) > self.scope_stack.top():
            self.table.pop()
        self.scope_stack.pop()
