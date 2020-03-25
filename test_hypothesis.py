import hypothesis.strategies as some
from hypothesis import event, given


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


def concatenate(a, b):
    return a + " " + b


@given(some.tuples(some.text(), some.text()))
def test_concatenate(input_strings):
    result = concatenate(input_strings[0], input_strings[1])
    assert result.startswith(input_strings[0] + ' ')
    assert result.endswith(' ' + input_strings[1])


def test_mysort():
    list_unsorted = [5, 3, 2, 1, 6]
    list_sorted = my_sort(list_unsorted)
    assert list_sorted == [1, 2, 3, 5, 6]


@given(input_list=some.lists(some.integers()))
def test_my_sort(input_list):
    l_sorted = my_sort(input_list)
    assert len(l_sorted) == len(input_list)
    assert set(l_sorted) == set(input_list)

    def length_to_range(n):
        base = 5
        div = n // base
        return div * base, (div + 1) * base

    length_range = length_to_range(len(input_list))
    event("input list length in range {}-{}".format(*length_range))
    for i in range(len(input_list) - 1):
        assert l_sorted[i] <= l_sorted[i + 1]
