import hypothesis.strategies as some
from hypothesis import given, settings


# Function that organizes list items in ascending order:
def sort_this_list(list):
    sorted_list = sorted(list)
    return sorted_list


# Example-based test that uses two manually determined cases:
def test_sort_this_list_example():
    assert sort_this_list([5, 3, 1, 4, 2]) == [1, 2, 3, 4, 5]  # True
    assert sort_this_list(["a", "d", "c", "e", "b"]) == [
        "a",
        "b",
        "c",
        "d",
        "e",
    ]  # True


# Property-based test that automatically generates up to 10,000 cases:

# Use the @given decorator to guide Hypothesis to the input value needed:
@given(input_list=some.lists(some.integers()))
# Use the @settings object to set the number of cases to run:
@settings(max_examples=10000)
def test_sort_this_list_properties(input_list):
    sorted_list = sorted(input_list)

    # Regardless of input, sorting should never change the size:
    assert len(sorted_list) == len(input_list)

    # Regardless of input, sorting should never change the set of distinct elements:
    assert set(sorted_list) == set(input_list)

    # Regardless of input, each element in the sorted list should be
    # lower or equal to the value that comes after it:
    for i in range(len(sorted_list) - 1):
        assert sorted_list[i] <= sorted_list[i + 1]
