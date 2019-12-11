import math

_data = '''.#..#
.....
#####
....#
...##'''

_data = '''......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####'''

_data = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''

_data = '''#..#.#.###.#...##.##....
.#.#####.#.#.##.....##.#
##..#.###..###..#####..#
####.#.#..#....#..##.##.
.#######.#####...#.###..
.##...#.#.###..###.#.#.#
.######.....#.###..#....
.##..##.#..#####...###.#
#######.#..#####..#.#.#.
.###.###...##.##....##.#
##.###.##.#.#..####.....
#.#..##..#..#.#..#####.#
#####.##.#.#.#.#.#.#..##
#...##.##.###.##.#.###..
####.##.#.#.####.#####.#
.#..##...##..##..#.#.##.
###...####.###.#.###.#.#
..####.#####..#####.#.##
..###..###..#..##...#.#.
##.####...##....####.##.
####..#..##.#.#....#..#.
.#..........#..#.#.####.
###..###.###.#.#.#....##
########.#######.#.##.##'''

# _data = '''.#....#####...#..
# ##...##.#####..##
# ##...#...#.#####.
# ..#.....X...###..
# ..#.#.....#....##'''

_data = _data.split("\n")

meteors = []

for (y, line) in enumerate(_data):
    for (x, v) in enumerate(line):
        if v == '#':
            meteors.append((x, y))


def make_lines(meteor, meteors):
    x, y = meteor
    lines = list()
    for other_meteor in meteors:
        ox, oy = other_meteor
        lines.append(math.atan2((y - oy), (ox - x)))
    return lines


def visible_astroids(meteors):
    liness = dict()
    for meteor in meteors:
        lines = make_lines(meteor, meteors)
        liness[meteor] = len(set(lines)) - 1

    return liness


visibility = visible_astroids(meteors)
maxm, maxn = None, -math.inf
for (meteor, n) in visibility.items():
    if n > maxn:
        maxm, maxn = meteor, n


print(maxm, maxn)
print("Deploying...")
print("Enabling Giant Vaporizing Laser")

lines = list(zip(meteors, make_lines(maxm, meteors)))
lines = list(map(lambda tup: (tup[0],
                              -(tup[1] - (math.tau / 4)) % math.tau,
                              (abs(tup[0][0] - maxm[0]) + abs(tup[0][1] - maxm[1]))),
                 lines))
lines.sort(key=lambda x: (x[1], x[2]), reverse=False)

prev_meteor = None
prev_angle = None
i = 0
while i < 200:
    (meteor, angle, distance) = lines.pop(0)
    if angle == prev_angle and meteor != prev_meteor:
        lines.append((meteor, angle, distance))
    else:
        i += 1
        prev_angle = angle
        print("OBLITERATED ASTEROID #{} {} at angle {} and distance {}".format(i, meteor, angle, distance))
    prev_meteor = meteor



