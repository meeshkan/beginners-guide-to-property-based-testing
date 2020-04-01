import base32_crockford
import hypothesis.strategies as some
from hypothesis import given


# This decoding scheme only works for non-negative integers
# `min_value=0` restricts Hypothesis to only generate integers with a minimum value of zero
@given(some.integers(min_value=0))
def test_base32_crockford(input_int):
    assert base32_crockford.decode(base32_crockford.encode(input_int)) == input_int
