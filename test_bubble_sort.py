import hypothesis.strategies as some
from hypothesis import given


def bubble_sort(nums):
    result = nums.copy()
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(result) - 1):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
    return result


def test_bubble_sort_example():
    # Test using two manually worked out examples:
    assert [1, 2, 3, 4, 5] == bubble_sort([5, 3, 1, 4, 2])
    assert [1, 1, 3, 3, 5] == bubble_sort([1, 3, 1, 3, 5])


# Guide the framework in what input we need:
@given(input_list=some.lists(some.integers()))
def test_bubble_sort_properties(input_list):
    input_list_copy = input_list.copy()
    sorted_list = bubble_sort(input_list)

    # Regardless of input, sorting should never change the original list:
    assert input_list_copy == input_list

    # Regardless of input, sorting should never change the size:
    assert len(sorted_list) == len(input_list)

    # Regardless of input, sorting should never change the set of distinct elements:
    assert set(sorted_list) == set(input_list)

    # Regardless of input, each element in the sorted list should be lower or equal to the value that comes after it:
    for i in range(len(sorted_list) - 1):
        assert sorted_list[i] <= sorted_list[i + 1]
