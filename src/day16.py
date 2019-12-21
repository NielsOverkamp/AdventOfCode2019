import math
from itertools import *


def lcm(x, y):
    return x*y // math.gcd(x, y)


data = '59750939545604170490448806904053996019334767199634549908834775721405739596861952646254979483184471162036292390420794027064363954885147560867913605882489622487048479055396272724159301464058399346811328233322326527416513041769256881220146486963575598109803656565965629866620042497176335792972212552985666620566167342140228123108131419565738662203188342087202064894410035696740418174710212851654722274533332525489527010152875822730659946962403568074408253218880547715921491803133272403027533886903982268040703808320401476923037465500423410637688454817997420944672193747192363987753459196311580461975618629750912028908140713295213305315022251918307904937'
# data = '03036732577212944063491565474664'
# data = '80871224585914546619083218645595'
offset = int(data[:7])
# data = "12345678"
# offset = 0

data_len = len(data)
signal = list(map(int, data)) * 10000
# signal = list(map(int, data)) * 4
signal_len = len(signal)

for i in range(100):
    print(i, signal[offset:offset+data_len])
    new_signal = []
    prev_tots = []
    for j in range(signal_len - 1, offset-1, -1):
        block_len = min(lcm(4*(j+1), data_len), signal_len)
        tot = 0
        word_len = (j+1) * 4
        nibble_len = j+1
        for ik, k in enumerate(range(0, block_len, word_len)):
            plus_start = k + nibble_len - 1
            plus_end = k + 2*nibble_len - 1
            minus_start = k+3*nibble_len - 1
            minus_end = k + 4*nibble_len - 1
            if 2*ik < len(prev_tots):
                prev_k = (word_len + 4) * ik
                prev_nibble_len = nibble_len + 1

                prev_plus_start = prev_k + prev_nibble_len - 1
                prev_plus_end = prev_k + 2*prev_nibble_len - 1
                prev_minus_start = prev_k + 3*prev_nibble_len - 1
                prev_minus_end = prev_k + 4*prev_nibble_len - 1

                new_tot = prev_tots[2*ik] \
                          - sum(signal[minus_end:prev_minus_end]) \
                          + sum(signal[minus_start:prev_minus_end])
                prev_tots[2*ik] = new_tot
                tot -= new_tot
                new_tot = prev_tots[2*ik + 1] \
                          - sum(signal[plus_end:prev_plus_end]) \
                          + sum(signal[plus_start:prev_plus_start])
                prev_tots[2*ik + 1] = new_tot
                tot += new_tot
            else:
                new_tot = sum(signal[minus_start:minus_end])
                prev_tots.append(new_tot)
                tot -= new_tot
                new_tot = sum(signal[plus_start:plus_end])
                prev_tots.append(new_tot)
                tot += new_tot
        new_signal.append(abs(tot*(signal_len//block_len)) % 10)
    signal = signal[:offset] + list(reversed(new_signal))

print(signal)
print(''.join(map(str, signal[offset:offset + 8])))
