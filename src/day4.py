_data = (278384, 824795)
# _data=(334445, 999999)


def options(number_bounds, depth, prev_digit=None, has_double=False, is_double_streak=False):
    if depth < 0:
        return ['']

    lower, upper = number_bounds[0] // 10 ** depth, number_bounds[1] // 10 ** depth
    lower1 = 0
    if depth == 0 and not has_double:
        if not is_double_streak and (lower < prev_digit <= upper):
            print('-'*5+str(prev_digit))
            return [str(prev_digit)]
        else:
            return []
    elif depth == 0 and is_double_streak:
        lower1 += prev_digit + 1


    if prev_digit is not None:
        lower1 = max(lower, prev_digit, lower1)
    else:
        lower1 = lower

    r = []
    # print("depth", depth)
    # print("range", lower1, upper)
    for d in range(lower1, upper + 1):
        print('-'*(5-depth) +str(d))
        if d == lower:
            new_lower_bound = number_bounds[0] - lower * 10 ** depth
            new_upper_bound = 10 ** depth - 1
        elif d == upper:
            new_lower_bound = 0
            new_upper_bound = number_bounds[1] - upper * 10 ** depth
        else:
            new_lower_bound = 0
            new_upper_bound = 10 ** depth - 1
        new_bounds = (new_lower_bound, new_upper_bound)
        new_is_double_streak = (not has_double or is_double_streak) and d == prev_digit
        new_has_double = not (new_is_double_streak and is_double_streak) and (has_double or d == prev_digit)
        r.extend(map(lambda x: str(d) + x, options(new_bounds, depth - 1, d, new_has_double, new_is_double_streak)))
    return r


_r = options(_data, 5)
print(_r)
print(len(_r))
