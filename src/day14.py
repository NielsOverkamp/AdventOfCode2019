import re
from collections import Counter

import math

_data = '''1 RNQHX, 1 LFKRJ, 1 JNGM => 8 DSRGV
2 HCQGN, 1 XLNC, 4 WRPWG => 7 ZGVZL
172 ORE => 5 WRPWG
7 MXMQ, 1 SLTF => 3 JTBLB
1 DSRGV => 4 SLZF
2 HDVD, 32 LFKRJ => 4 FCZQD
9 LNRS, 18 WKMWF => 8 RNQRM
12 MWSGQ => 9 DCKC
6 SLTF, 5 XLNC => 1 KFBX
4 QNRZ, 1 QHLF, 15 FWSK => 9 SFJC
9 KFBX, 15 RPKGX, 2 QNRZ => 6 LFKRJ
8 SFJC, 6 ZQGL, 4 PFCGF => 3 THPCT
2 RNQHX, 4 PFCGF, 1 ZQGL => 6 LNRS
195 ORE => 4 PTHDF
3 FJKSL => 7 FWSK
12 KBJW, 9 MWSGQ => 9 WKMWF
3 XLNC => 5 RPKGX
188 ORE => 7 FJKSL
6 ZNPNM, 3 KHXPM, 3 TJXB => 2 HSDS
1 DGKW, 17 XLNC => 1 PFCGF
2 VRPJZ, 3 DSRGV => 5 MWSGQ
12 BJBQP, 5 XLNC => 4 HCQGN
1 GFCGF => 3 HDVD
18 TJXB, 2 THPCT, 1 WPGQN => 4 KHXPM
1 ZGVZL => 1 JNGM
3 ZGVZL => 8 KBJW
12 GFCGF => 8 BJBQP
7 MXMQ, 18 WRPWG => 9 XLNC
13 ZGVZL, 1 QNRZ => 6 RNQHX
5 HRBG, 16 QNRZ => 9 WPGQN
5 SFJC, 1 PFCGF, 1 KHXPM => 5 FXDMQ
1 KBJW, 5 BNFV, 16 XLNC, 1 JNGM, 1 PFCGF, 1 ZNPNM, 4 FXDMQ => 5 VBWCM
5 ZGVZL, 5 LFKRJ => 9 QHLF
14 JTBLB => 5 VRPJZ
4 FWSK => 9 RXHC
2 HRBG, 3 FCZQD => 8 DRLBG
9 KLXC, 23 VBWCM, 44 VPTBL, 5 JRKB, 41 PFCGF, 4 WBCRL, 20 QNRZ, 28 SLZF => 1 FUEL
1 DRLBG => 5 VPTBL
13 LNRS => 7 ZNPNM
3 WPGQN => 9 TJXB
5 GFCGF, 3 HCQGN => 5 ZQGL
1 KHXPM, 4 LMCSR, 1 QHLF, 4 WKMWF, 1 DGKW, 3 KBRM, 2 RNQRM => 4 KLXC
171 ORE => 8 ZJGSJ
3 ZJGSJ => 3 MXMQ
124 ORE => 5 SLTF
22 KHXPM, 10 FXDMQ => 6 KBRM
2 FCZQD => 8 LMCSR
7 DCKC, 8 HSDS, 7 PFCGF, 16 ZNPNM, 3 RNQRM, 3 WKMWF, 2 WBCRL, 14 RXHC => 7 JRKB
7 DCKC, 2 MWSGQ => 3 BNFV
2 ZQGL => 9 DGKW
22 WRPWG => 6 HRBG
22 KBJW, 1 KFBX, 1 THPCT => 6 WBCRL
4 WRPWG, 1 RXHC, 21 FWSK => 8 QNRZ
1 PTHDF => 8 GFCGF'''

# _data = '''10 ORE => 10 A
# 1 ORE => 1 B
# 7 A, 1 B => 1 C
# 7 A, 1 C => 1 D
# 7 A, 1 D => 1 E
# 7 A, 1 E => 1 FUEL'''
#
# _data = '''171 ORE => 8 CNZTR
# 7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
# 114 ORE => 4 BHXH
# 14 VRPVC => 6 BMBT
# 6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
# 6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
# 15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
# 13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
# 5 BMBT => 4 WPTQ
# 189 ORE => 9 KTJDG
# 1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
# 12 VRPVC, 27 CNZTR => 2 XDBXC
# 15 KTJDG, 12 BHXH => 5 XCVML
# 3 BHXH, 2 VRPVC => 7 MZWV
# 121 ORE => 7 VRPVC
# 7 XCVML => 6 RJRHP
# 5 BHXH, 4 VRPVC => 5 LTCX'''

ReagentStr = (int, str)
Reagent = (int, 'Resource')
ReactionStr = ([ReagentStr], ReagentStr)
Reaction = ([Reagent], Reagent)


def parse(s: str) -> [ReactionStr]:
    r = re.compile(r'((?:\s*\d+\s+\w+\s*,?)+)=>\s*(\d+)\s+(\w+)\s*', flags=re.MULTILINE)
    reagents_r = re.compile(r'(\d+)\s+(\w+)')
    reactions = []
    for match in r.finditer(s):
        reagents = []
        for reagent_match in reagents_r.finditer(match.group(1)):
            reagent = int(reagent_match.group(1)), reagent_match.group(2)
            reagents.append(reagent)
        result = int(match.group(2)), match.group(3)
        reactions.append((reagents, result))
    return reactions


class Resource:
    name: str
    made_from: ([Reagent], int)
    makes: [Reaction]
    ore_path: [str]

    def __init__(self, name):
        self.name = name
        self.made_from = None
        self.makes = []

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)

    def make(self, resources: Counter, ore_used=0, amount=1):
        # print("Making {} of {}".format(amount, self.name))
        if self.name == 'ORE':
            resources['ORE'] += amount
            # print("Made {} of {}".format(amount, self.name))
            return ore_used + amount
        reagents, res_i = self.made_from
        times = math.ceil(amount / res_i)
        for r_i, reagent in reagents:
            r_amount = times*r_i - resources[reagent.name]
            if r_amount > 0:
                ore_used = reagent.make(resources, ore_used, r_amount)
            resources[reagent.name] -= times*r_i
        resources[self.name] += times*res_i
        # print("Made {} of {}".format(times*res_i, self.name))
        return ore_used


def run():
    _reactions = parse(_data)
    resources: {str: Resource} = dict()
    for (reagents, (res_i, result_str)) in _reactions:
        if result_str not in resources:
            resources[result_str] = Resource(result_str)
        result = resources[result_str]
        makes = []
        made_from = []
        for (r_i, reagent_str) in reagents:
            if reagent_str not in resources:
                resources[reagent_str] = Resource(reagent_str)
            reagent = resources[reagent_str]

            made_from.append((r_i, reagent))
            makes.append((r_i, reagent))
            reagent.makes.append((makes, (res_i, result)))
        result.made_from = (made_from, res_i)

    fuel = resources['FUEL']
    ore_limit = 10**12 #trillion
    ore_used = 0
    extra_resources = Counter()
    amount = ore_limit // 469536
    while True:
        new_extra_resources = Counter(extra_resources)
        print("Trying to make {} of fuel".format(amount))
        new_ore_used = fuel.make(new_extra_resources, amount=amount)
        print("Made {} of fuel total, {} of ore left".format(new_extra_resources['FUEL'], ore_limit - ore_used - new_ore_used))
        if new_ore_used < ore_limit - ore_used:
            print(">Affirmative")
            ore_used += new_ore_used
            extra_resources = new_extra_resources
        elif amount > 1:
            print(">Too much, halving amount")
            amount //= 2
        else:
            print(">Too much, found optimum")
            break

    return extra_resources['FUEL']


if __name__ == '__main__':
    print(run())
