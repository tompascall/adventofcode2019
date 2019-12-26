def solo_pair_at_start(digits, position, length):
    return (
        (position == 0) and
        digits[position] == digits[position + 1] and
        (digits[position + 1] != digits[position + 2]))

def solo_pair_at_end(digits, position, length):
    return (
        (position + 1 == length - 1) and
        digits[position] == digits[position + 1] and
        (digits[position - 1] != digits[position]))

def solo_pair_in_middle(digits, position, length):
    return (
        digits[position] == digits[position + 1] and
        (position > 0) and
        (position + 1 < length - 1) and
        (digits[position - 1] != digits[position]) and
        (digits[position + 1] != digits[position + 2]))

def has_solo_pair(digits):
    adjacent = False
    length = len(digits)
    for position in range(length - 1):
        if (
            solo_pair_at_start(digits, position, length) or
            solo_pair_at_end(digits, position, length) or
            solo_pair_in_middle(digits, position, length)
        ):
            adjacent = True
            break
    return adjacent

def is_increasing(digits):
    increasing = True
    for position in range(len(digits) - 1):
        if digits[position] > digits[position + 1]:
            increasing = False
            break
    return increasing

def count_candidate(start, end):
    counter = 0
    for num in range(start, end + 1):
        strnum = str(num)
        if has_solo_pair(strnum) & is_increasing(strnum):
            counter = counter + 1
    return counter

if __name__ == '__main__':
    print(count_candidate(307237, 769058))