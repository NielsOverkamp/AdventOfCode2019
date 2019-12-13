from enum import Enum
from typing import Callable, MutableSequence, MutableMapping, Iterator, Iterable

from itertools import chain, repeat

#
# Example programs
#

quine = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]


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


def tick(prog_mem, regs, inputf, outputf):
    i = regs["pc"]
    rel_base = regs["rel_base"]
    op = prog_mem[i]
    op, imm1, imm2, imm3 = op % 100, op // 100 % 10, op // 1000 % 10, op // 10000 % 10
    if op == 99:
        regs["pc"] = -1
        return

    if op == 1:
        set(prog_mem, i + 3, imm3, rel_base,
            get(prog_mem, i + 1, imm1, rel_base) + get(prog_mem, i + 2, imm2, rel_base))
        i += 4
    elif op == 2:
        set(prog_mem, i + 3, imm3, rel_base,
            get(prog_mem, i + 1, imm1, rel_base) * get(prog_mem, i + 2, imm2, rel_base))
        i += 4
    elif op == 3:
        _input = inputf()
        if _input is not None:
            set(prog_mem, i + 1, imm1, rel_base, _input)
            i += 2
    elif op == 4:
        outputf(get(prog_mem, i + 1, imm1, rel_base))
        i += 2
    elif op == 5:
        if get(prog_mem, i + 1, imm1, rel_base) != 0:
            i = get(prog_mem, i + 2, imm2, rel_base)
        else:
            i += 3
    elif op == 6:
        if get(prog_mem, i + 1, imm1, rel_base) == 0:
            i = get(prog_mem, i + 2, imm2, rel_base)
        else:
            i += 3
    elif op == 7:
        if get(prog_mem, i + 1, imm1, rel_base) < get(prog_mem, i + 2, imm2, rel_base):
            set(prog_mem, i + 3, imm3, rel_base, 1)
        else:
            set(prog_mem, i + 3, imm3, rel_base, 0)
        i += 4
    elif op == 8:
        if get(prog_mem, i + 1, imm1, rel_base) == get(prog_mem, i + 2, imm2, rel_base):
            set(prog_mem, i + 3, imm3, rel_base, 1)
        else:
            set(prog_mem, i + 3, imm3, rel_base, 0)
        i += 4
    elif op == 9:
        rel_base += get(prog_mem, i + 1, imm1, rel_base)
        i += 2
    regs["pc"] = i
    regs["rel_base"] = rel_base


#
# I/O Helpers
#

def std_in(machine_id=None):
    res = None
    while res is None:
        try:
            if machine_id is None:
                res = int(input("IntMachine Input: "))
            else:
                res = int(input("IntMachine {} Input: ".format(machine_id)))
        except ValueError:
            continue
    return res


def std_out(out, machine_id=None):
    if machine_id is None:
        print("IntMachine Output: {}".format(out))
    else:
        print("IntMachine {} Output: {}".format(machine_id, out))


class IterIn:
    iter: Iterator

    def __init__(self, _iter: Iterable):
        self._iter = iter(_iter)

    def __iter__(self):
        return self

    def __next__(self):
        return next(chain(self._iter, repeat(None)))

    def add_to_iter(self, new_iter: Iterable):
        self._iter = chain(self._iter, iter(new_iter))


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

class Status(Enum):
    RUNNING = 0
    WAITING = 1
    TERMINATED = 99


class Machine:
    prog_mem: MutableSequence[int]
    regs: MutableMapping[str, int]
    inputf: Callable[[int], int]
    outputf: Callable[[int, int], None]
    status: Status = Status.RUNNING

    def __init__(self, prog_mem, regs=None, inputf=std_in, outputf=std_out):
        self.prog_mem = prog_mem
        self.regs = regs
        if regs is None:
            self.regs = dict()
        if "pc" not in self.regs:
            self.regs["pc"] = 0
        if "rel_base" not in self.regs:
            self.regs["rel_base"] = 0

        self.inputf = inputf
        self.outputf = outputf

    def get_pc(self):
        return self.regs["pc"]


def run(machine: Machine):
    while machine.get_pc() >= 0:
        tick(machine.prog_mem, machine.regs, machine.inputf, machine.outputf)


def run_concurrent(*machines: Machine):
    machines_enumerated: {[int,(Machine, Status)]} = dict(
        map(lambda item: (item[0], item[1]), enumerate(machines)))
    while len(machines_enumerated) > 0:
        for (i, machine) in list(machines_enumerated.items()):
            if machine.get_pc() >= 0:
                prev_pc = machine.get_pc()
                print("Machine {}".format(i))
                print_state(machine.prog_mem, machine.regs)
                tick(machine.prog_mem, machine.regs, lambda: machine.inputf(i), lambda out: machine.outputf(out, i))
                if prev_pc == machine.get_pc():
                    machine.status = Status.WAITING
                else:
                    machine.status = Status.RUNNING
            else:
                print("Machine {}".format(i))
                print_state(machine.prog_mem, machine.regs)
                machine.status = Status.TERMINATED
                machines_enumerated.pop(i)


if __name__ == "__main__":
    run_concurrent(Machine(quine), Machine(quine))
