import hypothesis.strategies as some
from hypothesis import given

# Use the @given indicator to guide Hypothesis to what input value we need:
@given(input_list=some.lists(some.integers()))
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