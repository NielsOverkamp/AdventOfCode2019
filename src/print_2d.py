from itertools import tee


class String2DBuilder(dict):
    last_y = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self) -> str:
        keys0, keys1, keys2, keys3 = tee(self.keys(), 4)
        min_x, max_x = min(keys0, key=lambda x: x[0])[0], max(keys1, key=lambda x: x[0])[0]
        min_y, max_y = min(keys2, key=lambda x: x[1])[1], max(keys3, key=lambda x: x[1])[1]
        s = ""
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) in self:
                    s += str(self[(x, y)])
                else:
                    s += ' '
            s += '\n'
        return s

    def print(self):
        print(self.build())
        return

