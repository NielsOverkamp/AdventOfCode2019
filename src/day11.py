# _data = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
# _data = [1,1,1,4,99,5,6,0,99]
from collections import defaultdict

from itertools import chain, repeat, cycle, islice

_data = [3, 8, 1005, 8, 358, 1106, 0, 11, 0, 0, 0, 104, 1, 104, 0, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 1008,
         8, 1, 10, 4, 10, 101, 0, 8, 29, 1, 1104, 7, 10, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108, 0, 8, 10, 4,
         10, 1002, 8, 1, 54, 1, 103, 17, 10, 1, 7, 3, 10, 2, 8, 9, 10, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10,
         1008, 8, 1, 10, 4, 10, 102, 1, 8, 89, 1, 1009, 16, 10, 1006, 0, 86, 1006, 0, 89, 1006, 0, 35, 3, 8, 102, -1, 8,
         10, 101, 1, 10, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 102, 1, 8, 124, 1, 105, 8, 10, 1, 2, 0, 10, 1, 1106, 5, 10,
         3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 1001, 8, 0, 158, 1, 102, 2, 10, 1, 109,
         17, 10, 1, 109, 6, 10, 1, 1003, 1, 10, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10, 108, 1, 8, 10, 4, 10,
         1001, 8, 0, 195, 1006, 0, 49, 1, 101, 5, 10, 1006, 0, 5, 1, 108, 6, 10, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10,
         4, 10, 1008, 8, 0, 10, 4, 10, 102, 1, 8, 232, 2, 1102, 9, 10, 1, 1108, 9, 10, 3, 8, 1002, 8, -1, 10, 101, 1,
         10, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 1002, 8, 1, 262, 1006, 0, 47, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4,
         10, 108, 0, 8, 10, 4, 10, 101, 0, 8, 286, 1006, 0, 79, 2, 1003, 2, 10, 2, 107, 0, 10, 1006, 0, 89, 3, 8, 1002,
         8, -1, 10, 101, 1, 10, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 101, 0, 8, 323, 1006, 0, 51, 2, 5, 1, 10, 1, 6, 15,
         10, 2, 1102, 3, 10, 101, 1, 9, 9, 1007, 9, 905, 10, 1005, 10, 15, 99, 109, 680, 104, 0, 104, 1, 21101,
         838211572492, 0, 1, 21101, 0, 375, 0, 1106, 0, 479, 21102, 1, 48063328668, 1, 21102, 386, 1, 0, 1106, 0, 479,
         3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104,
         0, 3, 10, 104, 0, 104, 1, 21102, 1, 21679533248, 1, 21101, 0, 433, 0, 1105, 1, 479, 21102, 235190455527, 1, 1,
         21102, 444, 1, 0, 1106, 0, 479, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 0, 21101, 0, 837901247244, 1, 21102,
         1, 467, 0, 1106, 0, 479, 21101, 0, 709488169828, 1, 21102, 1, 478, 0, 1105, 1, 479, 99, 109, 2, 22102, 1, -1,
         1, 21102, 1, 40, 2, 21101, 0, 510, 3, 21102, 1, 500, 0, 1105, 1, 543, 109, -2, 2106, 0, 0, 0, 1, 0, 0, 1, 109,
         2, 3, 10, 204, -1, 1001, 505, 506, 521, 4, 0, 1001, 505, 1, 505, 108, 4, 505, 10, 1006, 10, 537, 1102, 1, 0,
         505, 109, -2, 2106, 0, 0, 0, 109, 4, 2101, 0, -1, 542, 1207, -3, 0, 10, 1006, 10, 560, 21101, 0, 0, -3, 21201,
         -3, 0, 1, 21202, -2, 1, 2, 21102, 1, 1, 3, 21102, 1, 579, 0, 1105, 1, 584, 109, -4, 2106, 0, 0, 109, 5, 1207,
         -3, 1, 10, 1006, 10, 607, 2207, -4, -2, 10, 1006, 10, 607, 21202, -4, 1, -4, 1106, 0, 675, 21202, -4, 1, 1,
         21201, -3, -1, 2, 21202, -2, 2, 3, 21101, 0, 626, 0, 1106, 0, 584, 22101, 0, 1, -4, 21102, 1, 1, -1, 2207, -4,
         -2, 10, 1006, 10, 645, 21102, 1, 0, -1, 22202, -2, -1, -2, 2107, 0, -3, 10, 1006, 10, 667, 22101, 0, -1, 1,
         21102, 1, 667, 0, 105, 1, 542, 21202, -2, -1, -2, 22201, -4, -2, -4, 109, -5, 2105, 1, 0]


#
# Machine Logic
#

def dynamic_allocate(data: [int], length):
    data.extend([0] * (length - (len(data) - 1)))


def get(data, i, imm, rel_base):
    dynamic_allocate(data, i)
    if imm == 1:
        return data[i]
    elif imm == 0:
        dynamic_allocate(data, data[i])
        return data[data[i]]
    elif imm == 2:
        dynamic_allocate(data, rel_base + data[i])
        return data[rel_base + data[i]]
    else:
        raise Exception("Get mode {} not available".format(imm))


def set(data, i, imm, rel_base, v):
    dynamic_allocate(data, i)
    if imm == 0:
        dynamic_allocate(data, data[i])
        data[data[i]] = v
    elif imm == 2:
        dynamic_allocate(data, rel_base + data[i])
        data[rel_base + data[i]] = v
    else:
        raise Exception("Set mode {} not available".format(imm))


def tick(data, regs, inputf, outputf):
    i = regs["pc"]
    rel_base = regs["rel_base"]
    op = data[i]
    op, imm1, imm2, imm3 = op % 100, op // 100 % 10, op // 1000 % 10, op // 10000 % 10
    if op == 99:
        regs["pc"] = -1
        return

    if op == 1:
        set(data, i + 3, imm3, rel_base, get(data, i + 1, imm1, rel_base) + get(data, i + 2, imm2, rel_base))
        i += 4
    elif op == 2:
        set(data, i + 3, imm3, rel_base, get(data, i + 1, imm1, rel_base) * get(data, i + 2, imm2, rel_base))
        i += 4
    elif op == 3:
        _input = inputf()
        if _input is not None:
            set(data, i + 1, imm1, rel_base, _input)
            i += 2
    elif op == 4:
        outputf(get(data, i + 1, imm1, rel_base))
        i += 2
    elif op == 5:
        if get(data, i + 1, imm1, rel_base) != 0:
            i = get(data, i + 2, imm2, rel_base)
        else:
            i += 3
    elif op == 6:
        if get(data, i + 1, imm1, rel_base) == 0:
            i = get(data, i + 2, imm2, rel_base)
        else:
            i += 3
    elif op == 7:
        if get(data, i + 1, imm1, rel_base) < get(data, i + 2, imm2, rel_base):
            set(data, i + 3, imm3, rel_base, 1)
        else:
            set(data, i + 3, imm3, rel_base, 0)
        i += 4
    elif op == 8:
        if get(data, i + 1, imm1, rel_base) == get(data, i + 2, imm2, rel_base):
            set(data, i + 3, imm3, rel_base, 1)
        else:
            set(data, i + 3, imm3, rel_base, 0)
        i += 4
    elif op == 9:
        rel_base += get(data, i + 1, imm1, rel_base)
        i += 2
    regs["pc"] = i
    regs["rel_base"] = rel_base


#
# I/O Helpers
#

def std_in():
    res = None
    while res is None:
        try:
            res = int(input("IntMachine Input: "))
        except ValueError:
            continue
    return res


def std_out(out):
    print("IntMachine Output: {}".format(out))


class IterIn:
    def __init__(self, _iter):
        self._iter = _iter

    def __iter__(self):
        return self

    def __next__(self):
        return next(chain(self._iter, repeat(None)))

    def add_to_iter(self, new_iter):
        self._iter = chain(self._iter, new_iter)


#
# PRINTING
#

def dig_str(n, d):
    if n >= 0:
        if n >= 10 ** d:
            return str((n // 10 ** d) % 10)
        else:
            return " "
    else:
        if 10 ** d > -n >= 10 ** (d - 1):
            return "-"
        elif -n >= 10 ** d:
            return str((-n // 10 ** d) % 10)
        else:
            return " "


def print_state(data: [int], regs: {str: int}):
    header = "po123"
    for d in reversed(range(0, 5)):
        print(header[d] + " " + " ".join(map(lambda n: dig_str(n, d), data)))
    print(" " * (2 * regs["pc"] + 2) + "^")
    print("{{\n{}}}".format("".join(list(map(lambda item: "\t{}: {},\n".format(*item), regs.items())))))


#
# Main controller
#

def run(data, regs=None, inputf=std_in, outputf=std_out):
    if regs is None:
        regs = dict()
    if "pc" not in regs:
        regs["pc"] = 0
    if "rel_base" not in regs:
        regs["rel_base"] = 0
    while regs["pc"] >= 0:
        # print_state(data, regs)
        tick(data, regs, inputf, outputf)
    print_state(data, regs)


if __name__ == '__main__':
    dir_iter = cycle([(0, 1), (1, 0), (0, -1), (-1, 0)])
    colors = defaultdict(lambda: 0)
    pos = (0, 0)
    colors[pos] = 1
    direc: (int, int) = next(dir_iter)
    i = 0


    def set_color_or_dir(out):
        global pos, direc, colors, dir_iter, i
        if i == 0:
            i = 1
            colors[pos] = out
        else:
            i = 0
            if out == 0:
                direc = next(islice(dir_iter, 2, 3))
            else:
                direc = next(dir_iter)
            pos = pos[0] + direc[0], pos[1] + direc[1]


    run(_data, inputf=lambda: colors[pos], outputf=set_color_or_dir)
    xs = list(map(lambda x: x[0], colors.keys()))
    min_x, max_x = min(xs), max(xs)
    ys = list(map(lambda x: x[1], colors.keys()))
    min_y, max_y = min(ys), max(ys)

    print(len(colors))
    s = ""
    for y in range(max_y, min_y -1, -1):
        for x in range(min_x, max_x + 1):
            s += " " if colors[x,y] == 0 else "#"
        s += "\n"
    print(s)
