from itertools import tee


class String2DBuilder(dict):
    def build(self) -> str:
        keys0, keys1, keys2, keys3 = tee(self.keys(), 4)
        min_x, max_x = min(keys0, key=lambda x: x[0])[0], max(keys1, key=lambda x: x[0])[0]
        min_y, max_y = min(keys2, key=lambda x: x[1])[1], max(keys3, key=lambda x: x[1])[1]
        s = ""
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                s += self[(x, y)]
            s += '\n'
        return s
