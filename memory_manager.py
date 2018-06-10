from constants import Value_type


class MemoryManager(object):
    def __init__(self, start):
        self.pointer = start

    def get_variable(self, type, count=1):
        if type == Value_type.VOID:
            raise Exception("Cannot assign memory to void")
        start = self.pointer
        self.pointer += count * 4
        # todo: array out of bound exception ?!
        return start


# todo: which get_variable? (R or K)