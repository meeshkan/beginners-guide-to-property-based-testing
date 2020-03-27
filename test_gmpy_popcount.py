import hypothesis.strategies as some
import pytest
from hypothesis import given

try:
    import gmpy2
except ModuleNotFoundError:
    pass


def count_bits_slow(input_int):
    return bin(input_int).count("1")


@pytest.mark.skip(reason="Avoid forcing to install gmpy2")
@given(some.integers(min_value=0))
def test_gmpy2_popcount(input_int):
    assert count_bits_slow(input_int) == gmpy2.popcount(input_int)
