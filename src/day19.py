from collections import deque

from itertools import product, chain, tee

from IntMachine import Machine, run
from print_2d import String2DBuilder

_prog = [109, 424, 203, 1, 21102, 11, 1, 0, 1106, 0, 282, 21101, 0, 18, 0, 1106, 0, 259, 1201, 1, 0, 221, 203, 1, 21102,
         1, 31, 0, 1106, 0, 282, 21101, 0, 38, 0, 1106, 0, 259, 20102, 1, 23, 2, 21202, 1, 1, 3, 21101, 1, 0, 1, 21101,
         0, 57, 0, 1105, 1, 303, 2101, 0, 1, 222, 20101, 0, 221, 3, 21001, 221, 0, 2, 21102, 1, 259, 1, 21101, 0, 80, 0,
         1105, 1, 225, 21101, 185, 0, 2, 21102, 91, 1, 0, 1106, 0, 303, 1202, 1, 1, 223, 21001, 222, 0, 4, 21102, 259,
         1, 3, 21101, 225, 0, 2, 21102, 1, 225, 1, 21101, 0, 118, 0, 1106, 0, 225, 20102, 1, 222, 3, 21102, 1, 131, 2,
         21101, 133, 0, 0, 1106, 0, 303, 21202, 1, -1, 1, 22001, 223, 1, 1, 21101, 148, 0, 0, 1105, 1, 259, 2101, 0, 1,
         223, 21002, 221, 1, 4, 21002, 222, 1, 3, 21101, 0, 16, 2, 1001, 132, -2, 224, 1002, 224, 2, 224, 1001, 224, 3,
         224, 1002, 132, -1, 132, 1, 224, 132, 224, 21001, 224, 1, 1, 21101, 0, 195, 0, 106, 0, 109, 20207, 1, 223, 2,
         20101, 0, 23, 1, 21102, 1, -1, 3, 21101, 0, 214, 0, 1105, 1, 303, 22101, 1, 1, 1, 204, 1, 99, 0, 0, 0, 0, 109,
         5, 1201, -4, 0, 249, 22101, 0, -3, 1, 22101, 0, -2, 2, 21201, -1, 0, 3, 21101, 0, 250, 0, 1106, 0, 225, 21201,
         1, 0, -4, 109, -5, 2106, 0, 0, 109, 3, 22107, 0, -2, -1, 21202, -1, 2, -1, 21201, -1, -1, -1, 22202, -1, -2,
         -2, 109, -3, 2106, 0, 0, 109, 3, 21207, -2, 0, -1, 1206, -1, 294, 104, 0, 99, 22102, 1, -2, -2, 109, -3, 2105,
         1, 0, 109, 5, 22207, -3, -4, -1, 1206, -1, 346, 22201, -4, -3, -4, 21202, -3, -1, -1, 22201, -4, -1, 2, 21202,
         2, -1, -1, 22201, -4, -1, 1, 21201, -2, 0, 3, 21101, 343, 0, 0, 1106, 0, 303, 1105, 1, 415, 22207, -2, -3, -1,
         1206, -1, 387, 22201, -3, -2, -3, 21202, -2, -1, -1, 22201, -3, -1, 3, 21202, 3, -1, -1, 22201, -3, -1, 2,
         22101, 0, -4, 1, 21102, 384, 1, 0, 1106, 0, 303, 1105, 1, 415, 21202, -4, -1, -4, 22201, -4, -3, -4, 22202, -3,
         -2, -2, 22202, -2, -4, -4, 22202, -3, -2, -3, 21202, -4, -1, -2, 22201, -3, -2, 1, 21201, 1, 0, -4, 109, -5,
         2106, 0, 0]


def scan(start_x, end_x, start_y, end_y):
    coord_iter, _coord_iter = tee(product(range(start_x, end_x), range(start_y,end_y)))
    inputf = chain.from_iterable(_coord_iter).__next__

    map_map = String2DBuilder()
    count = 0

    def outputf(val):
        nonlocal count
        if val == 1:
            count += 1
            map_map[next(coord_iter)] = '#'
        else:
            next(coord_iter)

    while True:
        try:
            machine = Machine(_prog[:], inputf=inputf, outputf=outputf)
            run(machine)
        except StopIteration:
            break
    map_map.print()
    print(count)


if __name__ == "__main__":

    # print('\n'.join(map(lambda x: '{}\t{}'.format(*x), map_map.keys())))
    # scan(0,50,0,50)

    s = 100
    educated_guess = (1700, 2025)

    # s = 10
    # educated_guess = (171, 204)

    scan(educated_guess[0], educated_guess[0]+s, educated_guess[1], educated_guess[1]+s)

    guess_buffer = deque((educated_guess[0], educated_guess[1] + s - 1, educated_guess[0] + s - 1, educated_guess[1]))
    current_guess = educated_guess
    l_in = False
    r_in = False
    is_l = True
    found_lower = False
    final_guess = None


    def inputf():
        global l_in, r_in, is_l, current_guess, found_lower, final_guess
        while True:
            if not found_lower:
                if l_in:
                    current_guess = current_guess[0] - 1, current_guess[1]
                    guess_buffer.clear()
                    is_l = True
                    print()
                elif r_in:
                    current_guess = (current_guess[0], current_guess[1] - 1)
                    assert len(guess_buffer) == 0
                    print()
                elif len(guess_buffer) <= 0:
                    print()
                    print("Guess {} is lower bound".format(current_guess))
                    found_lower = True

            if found_lower:
                if not l_in:
                    current_guess = current_guess[0] + 1, current_guess[1]
                    guess_buffer.clear()
                    is_l = True
                    print()
                elif not r_in:
                    current_guess = current_guess[0], current_guess[1] + 1
                    assert len(guess_buffer) == 0
                    print()
                elif len(guess_buffer) <= 0:
                    print()
                    print("Found {}".format(current_guess))
                    final_guess = current_guess[0], current_guess[1]

            if len(guess_buffer) <= 0:
                print("Trying guess {}".format(current_guess))
                l_in = found_lower
                r_in = found_lower
                new_guess_x, new_guess_y = current_guess
                guess_buffer.extend((new_guess_x, new_guess_y + s - 1, new_guess_x + s - 1, new_guess_y))

            print(guess_buffer[0], end='\t')
            yield guess_buffer.popleft()


    def outputf(val):
        global is_l
        if is_l:
            global l_in
            l_in = val == 1
            is_l = False
        else:
            global r_in
            r_in = val == 1
            is_l = True


    while final_guess is None:
        machine = Machine(_prog[:], inputf=inputf().__next__, outputf=outputf)
        run(machine)
    print()
    print(final_guess)
    scan(final_guess[0], final_guess[0]+s, final_guess[1], final_guess[1] + s)
    scan(final_guess[0] - 1, final_guess[0] + s -1, final_guess[1] - 1, final_guess[1] + s - 1)
