import re
from enum import Enum
from typing import Union, Tuple, Iterable, Reversible

# ((a * 52) - 6699) * 13 - 1684) * 106

_data = '''deal with increment 52
cut -6699
deal with increment 33
cut -1684
deal with increment 43
cut 106
deal into new stack
deal with increment 64
cut 8580
deal with increment 72
cut -1582
deal with increment 28
cut -2695
deal with increment 32
cut -563
deal with increment 38
deal into new stack
deal with increment 69
deal into new stack
cut 9695
deal with increment 24
cut -2734
deal into new stack
cut 7754
deal with increment 67
deal into new stack
cut -9526
deal with increment 27
cut 7997
deal with increment 64
deal into new stack
deal with increment 28
deal into new stack
cut 4724
deal with increment 49
cut -7086
deal with increment 38
cut 9989
deal with increment 66
cut 1686
deal with increment 68
deal into new stack
deal with increment 36
cut 4781
deal into new stack
cut -999
deal with increment 69
cut -1613
deal with increment 44
cut -8147
deal with increment 46
cut 8971
deal with increment 67
cut -4022
deal with increment 10
deal into new stack
deal with increment 36
cut -6282
deal with increment 68
cut 7512
deal with increment 61
deal into new stack
cut 572
deal with increment 34
cut 4657
deal with increment 7
cut -1947
deal with increment 30
cut 1251
deal with increment 15
cut 5738
deal with increment 6
cut -8928
deal into new stack
deal with increment 49
cut -6696
deal with increment 52
cut 9897
deal with increment 16
cut 5911
deal with increment 29
cut 201
deal with increment 20
cut 3702
deal into new stack
deal with increment 29
deal into new stack
cut 6079
deal with increment 71
deal into new stack
cut -7073
deal with increment 49
cut -6207
deal into new stack
deal with increment 73
cut 1913
deal with increment 24
cut -6212
deal into new stack
cut 319'''
deck_l = 10007
deck2_l = 119315717514047
times = 101741582076661

# _data = '''deal with increment 7
# deal into new stack
# deal into new stack'''
#
# _data = '''deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1'''
#
# _data = '''cut 6
# deal with increment 7
# deal into new stack '''
# deck_l = 10

REVERSE_REG = re.compile(r'deal into new stack')
DEAL_INCREMENT_REG = re.compile(r'deal with increment (-?\d+)')
CUT_REG = re.compile(r'cut (-?[\d]+)')


class Operation(Enum):
    REVERSE = 0
    DEAL_INCREMENT = 1
    CUT = 2


Trick = Union[Tuple[Operation], Tuple[Operation, int]]


def parse(s: str) -> Iterable[Trick]:
    s = s.splitlines()
    for line in s:
        if REVERSE_REG.match(line):
            yield Operation.REVERSE,
        else:
            match = DEAL_INCREMENT_REG.match(line)
            if match is not None:
                yield Operation.DEAL_INCREMENT, int(match.group(1))
            else:
                match = CUT_REG.match(line)
                if match is not None:
                    yield Operation.CUT, int(match.group(1))
                else:
                    raise Exception("Unknown command {}".format(line))


def do_trick(index: int, trick: Trick, l: int):
    if trick[0] == Operation.REVERSE:
        return (index * -1 - 1) % l
    elif trick[0] == Operation.DEAL_INCREMENT:
        return (index * trick[1]) % l
    elif trick[0] == Operation.CUT:
        return (index - trick[1]) % l
    else:
        raise Exception("Unknown trick {}".format(trick))


def compress_tricks(tricks: Reversible[Trick], l: int, reverse: bool = False) -> Tuple[int, int]:
    mul = 1
    add = 0
    if reverse:
        tricks = reversed(tricks)
    for trick in tricks:
        if trick[0] == Operation.REVERSE:
            mul *= -1
            add *= -1
            add -= 1
            mul %= l
            add %= l
        elif trick[0] == Operation.DEAL_INCREMENT:
            if reverse:
                a = pow(trick[1], deck2_l - 2, deck2_l)
                mul *= a
                add *= a
            else:
                mul *= trick[1]
                add *= trick[1]
            mul %= l
            add %= l
        elif trick[0] == Operation.CUT:
            if reverse:
                add += trick[1]
            else:
                add -= trick[1]
            add %= l
    return mul, add



if __name__ == '__main__':
    _tricks = list(parse(_data))

    _index = 2019

    # _index = 2
    # deck_l = 20011
    # times = 5

    # for _ in range(times):
    for _trick in _tricks:
        _index = do_trick(_index, _trick, deck_l)
    print(_index)

    print("HA! Childsplay!")

    _start_index = 2020

    # deck2_l = deck_l
    # _start_index = _index
    # times = 1

    _inv_mul, _inv_add = compress_tricks(_tricks, deck2_l, reverse=True)
    part_res = _start_index
    _mul_adds = [(_inv_mul, _inv_add)]
    _times = times
    print(times, _mul_adds)
    while times > 0:
        _mul, _add = _mul_adds[-1]
        if times & 1 == 1:
            part_res *= _mul
            part_res += _add
            part_res %= deck2_l
        _mul, _add = (_mul ** 2) % deck2_l, (_mul * _add + _add) % deck2_l
        _mul_adds.append((_mul, _add))
        times >>= 1
        print(times, _mul_adds, part_res)

    print(part_res)
