from constants import Value_type


class MemoryManager(object):
    def __init__(self, start):
        self.pointer = start
        self.type_dict = dict()

    def get_temp(self, type):
        ret = self.pointer
        self.type_dict[ret] = type
        if (type == Value_type.VOID):
            raise Exception("Cannot assign memory to void.")
        self.pointer += 4
        return ret

