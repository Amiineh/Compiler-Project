
class Stack(list):
    def push(self, *args, **kwargs):
        x = self.append(*args, **kwargs)
        return x

    def pop(self, count=1, *args, **kwargs):
        for _ in range(count):
            super(Stack, self).pop(*args, **kwargs)

    def top(self):
        return self[len(self) - 1]