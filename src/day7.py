import math

_data = [
    3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0
]

_data = [3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 38, 47, 72, 97, 122, 203, 284, 365, 446, 99999, 3, 9, 1001, 9, 3, 9,
         1002, 9, 5, 9, 1001, 9, 4, 9, 4, 9, 99, 3, 9, 102, 3, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 2, 9, 102, 5, 9, 9, 101,
         3, 9, 9, 1002, 9, 5, 9, 101, 4, 9, 9, 4, 9, 99, 3, 9, 101, 5, 9, 9, 1002, 9, 3, 9, 101, 2, 9, 9, 102, 3, 9, 9,
         1001, 9, 2, 9, 4, 9, 99, 3, 9, 101, 3, 9, 9, 102, 2, 9, 9, 1001, 9, 4, 9, 1002, 9, 2, 9, 101, 2, 9, 9, 4, 9,
         99, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9,
         3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9,
         101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 99, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9,
         101, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002,
         9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 1001, 9,
         2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9,
         4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9,
         3, 9, 102, 2, 9, 9, 4, 9, 99, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3,
         9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9,
         1001, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 99, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9,
         101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101,
         1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9,
         2, 9, 4, 9, 99]

# _data = [
#     3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
#     27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5
# ]


def get(data, i, imm):
    if imm == 1:
        return data[i]
    else:
        return data[data[i]]


def tick(data, i, input_buf, output_buf):
    op = data[i]
    op, imm1, imm2, imm3 = op % 100, op // 100 % 10, op // 1000 % 10, op // 10000 % 10
    if op == 99:
        return -1

    if op == 1:
        data[data[i + 3]] = get(data, i + 1, imm1) + get(data, i + 2, imm2)
        i += 4
    elif op == 2:
        data[data[i + 3]] = get(data, i + 1, imm1) * get(data, i + 2, imm2)
        i += 4
    elif op == 3:
        data[data[i + 1]] = input_buf.pop(0)
        i += 2
    elif op == 4:
        output_buf.append(get(data, i + 1, imm1))
        i += 2
    elif op == 5:
        if get(data, i + 1, imm1) != 0:
            i = get(data, i + 2, imm2)
        else:
            i += 3
    elif op == 6:
        if get(data, i + 1, imm1) == 0:
            i = get(data, i + 2, imm2)
        else:
            i += 3
    elif op == 7:
        if get(data, i + 1, imm1) < get(data, i + 2, imm2):
            data[data[i + 3]] = 1
        else:
            data[data[i + 3]] = 0
        i += 4
    elif op == 8:
        if get(data, i + 1, imm1) == get(data, i + 2, imm2):
            data[data[i + 3]] = 1
        else:
            data[data[i + 3]] = 0
        i += 4

    return i


def run(data, input_buf=None, pc=0):
    if input_buf is None:
        input_buf = []
    output = []
    while pc >= 0:
        pc = tick(data, pc, input_buf, output)
    return output


def run_cond_gen(data):
    pc = 0
    data = data[:]

    def _run_while_input(_input):
        nonlocal pc
        output = []
        while len(_input) > 0 and pc >= 0:
            pc = tick(data, pc, _input, output)
        return output

    def _run_till_output(_input):
        nonlocal pc
        output = []
        while len(output) == 0 and pc >= 0:
            pc = tick(data, pc, _input, output)
        return output

    return _run_while_input, _run_till_output


def gen_seqs(allowed: [[int]]):
    if len(allowed) == 0:
        return [[]]
    _seqs = []
    for v in allowed:
        copy = allowed[:]
        copy.remove(v)
        _seqs.extend(list(map(lambda x: x + [v], gen_seqs(copy))))
    return _seqs


seqs = gen_seqs(list(range(5, 10)))
assert len(seqs) == 120

max_out = -math.inf
for seq in seqs:
    _amps = [(run_cond_gen(_data), seqn) for seqn in seq]
    amps = []
    for ((amp_while, amp_till), seqn) in _amps:
        amp_while([seqn])
        amps.append(amp_till)

    last_final_output = None
    current_amp = 0
    out = [0]
    while len(out) > 0:
        if current_amp == 0:
            last_final_output = out[0]
            print(last_final_output)
        out = amps[current_amp](out)
        current_amp += 1
        current_amp %= 5

    print(last_final_output)
    max_out = max(max_out, last_final_output)
print(max_out)

# for noun in range(100):
#     for verb in range(100):
#         data = _data[:]
#         data[1] = noun
#         data[2] = verb
#         run(data)
#         if data[0] == 19690720:
#             print(100 * noun + verb)
