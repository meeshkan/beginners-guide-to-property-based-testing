# Function that organizes list items in ascending order:
def sort_this_list(list):
    sorted_list = sorted(list)
    return sorted_list

# Test for our function that uses two manually determined examples:
def test_sort_this_list():
    assert sort_this_list([5, 3, 1, 4, 2]) == [1, 2, 3, 4, 5] # True
    assert sort_this_list(['a', 'd', 'c', 'e', 'b']) == ['a', 'b', 'c', 'd', 'e'] # True