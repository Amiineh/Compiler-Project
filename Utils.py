
class Stack(list):
    def push(self, *args, **kwargs):
        x = self.append(*args, **kwargs)
        return x

    def pop(self, count=1, *args, **kwargs):
        for _ in range(count):
            super(Stack, self).pop(*args, **kwargs)

    def top(self, count = 1):
        return self[len(self) - count]


class Unit(object):

    def __init__(self, value=None, type=None , memory_address = None):
        self.value = value
        self.type = type
        self.address = memory_address
