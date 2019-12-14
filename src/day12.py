from itertools import combinations
from time import time

if __name__ == "__main__":
    io = ([3, 3, 0], [0, 0, 0])
    europe = ([4, -16, 2], [0, 0, 0])
    ganymede = ([-10, -6, 5], [0, 0, 0])
    callisto = ([-3, 0, -13], [0, 0, 0])
    # io = ([-1, 0, 2], [0, 0, 0])
    # europe = ([2, -10, -7], [0, 0, 0])
    # ganymede = ([4, -8, 8], [0, 0, 0])
    # callisto = ([3, 5, -1], [0, 0, 0])
    # io = ([-8,-10,0],[0,0,0])
    # europe = ([5,5,10],[0,0,0])
    # ganymede = ([2,-7,3],[0,0,0])
    # callisto = ([9,-8,-3],[0,0,0])

    moons = (io, europe, ganymede, callisto)
    visited = set()
    visited_x = dict()
    visited_y = dict()
    visited_z = dict()
    found_x = False
    found_y = False
    found_z = False
    t0 = time()
    i = 0
    while i > -1:
        key = (moons[0][0][0], moons[0][0][1], moons[0][0][2],
               moons[0][1][0], moons[0][1][1], moons[0][1][2],
               moons[1][0][0], moons[1][0][1], moons[1][0][2],
               moons[1][1][0], moons[1][1][1], moons[1][1][2],
               moons[2][0][0], moons[2][0][1], moons[2][0][2],
               moons[2][1][0], moons[2][1][1], moons[2][1][2],
               moons[3][0][0], moons[3][0][1], moons[3][0][2],
               moons[3][1][0], moons[3][1][1], moons[3][1][2])
        if key in visited:
            break
        visited.add(key)

        x_key = (moons[0][0][0],
                 moons[0][1][0],
                 moons[1][0][0],
                 moons[1][1][0],
                 moons[2][0][0],
                 moons[2][1][0],
                 moons[3][0][0],
                 moons[3][1][0])

        y_key = (moons[0][0][1],
                 moons[0][1][1],
                 moons[1][0][1],
                 moons[1][1][1],
                 moons[2][0][1],
                 moons[2][1][1],
                 moons[3][0][1],
                 moons[3][1][1])

        z_key = (moons[0][0][2],
                 moons[0][1][2],
                 moons[1][0][2],
                 moons[1][1][2],
                 moons[2][0][2],
                 moons[2][1][2],
                 moons[3][0][2],
                 moons[3][1][2])

        if not found_x and x_key in visited_x:
            print("x {}-{}".format(i, visited_x[x_key]))
            if visited_x[x_key] > 0:
                found_x = True
        visited_x[x_key] = i

        if not found_y and y_key in visited_y:
            print("y {}-{}".format(i, visited_y[y_key]))
            if visited_y[y_key] > 0:
                found_y = True
        visited_y[y_key] = i

        if not found_z and z_key in visited_z:
            print("z {}-{}".format(i, visited_z[z_key]))
            if visited_z[z_key] > 0:
                found_z = True
        visited_z[z_key] = i

        if found_x and found_y and found_z:
            break

        # print(i)
        # for moon in moons: print(moon)
        for (p1, v1), (p2, v2) in combinations(moons, 2):
            v1[0] += (1 if p1[0] < p2[0] else (-1 if p1[0] > p2[0] else 0))
            v1[1] += (1 if p1[1] < p2[1] else (-1 if p1[1] > p2[1] else 0))
            v1[2] += (1 if p1[2] < p2[2] else (-1 if p1[2] > p2[2] else 0))
            v2[0] += (1 if p2[0] < p1[0] else (-1 if p2[0] > p1[0] else 0))
            v2[1] += (1 if p2[1] < p1[1] else (-1 if p2[1] > p1[1] else 0))
            v2[2] += (1 if p2[2] < p1[2] else (-1 if p2[2] > p1[2] else 0))
        for (p, v) in moons:
            p[0] += v[0]
            p[1] += v[1]
            p[2] += v[2]
        i += 1
    print(i)
    for moon in moons:
        print(moon)
    print("Energy: {}".format(sum(map(lambda moon: sum(map(abs, moon[0])) * sum(map(abs, moon[1])), moons))))
    print(time() - t0)
