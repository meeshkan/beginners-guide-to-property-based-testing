from hypothesis import given, event
import hypothesis.strategies as some


def encode(input_string):
    if not input_string:
        return []
    count = 1
    prev = ""
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (prev, count)
                lst.append(entry)
            count = 1
            prev = character
        else:
            count += 1
    entry = (character, count)
    lst.append(entry)
    return lst


def decode(lst):
    q = ""
    for character, count in lst:
        q += character * count
    return q


@given(some.text())
def test_decode_inverts_encode(s):
    assert decode(encode(s)) == s


@given(some.integers(), some.integers())
def test_ints_are_commutative(x, y):
    assert x + y == y + x


@given(x=some.integers(), y=some.integers())
def test_ints_cancel(x, y):
    assert (x + y) - y == x


@given(some.lists(some.integers()))
def test_reversing_twice_gives_same_list(xs):
    # This will generate lists of arbitrary length (usually between 0 and
    # 100 elements) whose elements are integers.
    ys = list(xs)
    ys.reverse()
    ys.reverse()
    assert xs == ys


@given(some.tuples(some.booleans(), some.text()))
def test_look_tuples_work_too(t):
    # A tuple is generated as the one you provided, with the corresponding
    # types in those positions.
    assert len(t) == 2
    assert isinstance(t[0], bool)
    assert isinstance(t[1], str)


def my_sort(l):
    return sorted(l)


# Example-based test


def test_mysort():
    l = [5, 3, 2, 1, 6]
    l_sorted = my_sort(l)
    assert l_sorted == [1, 2, 3, 5, 6]


@given(l=some.lists(some.integers()))
def test_my_sort(l):
    l_sorted = my_sort(l)
    assert len(l_sorted) == len(l)
    assert set(l_sorted) == set(l)

    def length_to_range(n):
        base = 5
        div = n // base
        return div * base, (div + 1) * base

    length_range = length_to_range(len(l))
    event("input list length in range {}-{}".format(*length_range))
    for i in range(len(l) - 1):
        assert l_sorted[i] <= l_sorted[i + 1]
