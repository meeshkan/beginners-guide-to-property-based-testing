import hypothesis.strategies as some
import pytest
from hypothesis import given, settings

try:
    import gmpy2
except ModuleNotFoundError:
    pass

# Slower solution that converts the integer to a binary string 
# and then counts the occurences of the string "1" inside:
def count_bits_slow(input_int):
    return bin(input_int).count("1")

@pytest.mark.skip(reason="Avoid forcing to install gmpy2")
@given(some.integers(min_value=0))
# Sets the number of test cases to 500 rather than the default 100:
@settings(max_examples=500)
# Optimized solution using pygmp2 to count set bits in an integer:
def test_gmpy2_popcount(input_int):
    assert count_bits_slow(input_int) == gmpy2.popcount(input_int)
