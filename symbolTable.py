class Symbol(object):
    def __init__(self, value):
        self.value = value


class SymbolTable(object):
    def __init__(self):
        self.table = []
        self.stack = [0]
        self.hide_upper_scopes = False

    def find(self, id_value):
        for id in self.table:
            if id.value == id_value:
                return self.table.index(id)

        new_id = Symbol(id_value)
        self.table.append(new_id)
        return self.table.index(new_id)
