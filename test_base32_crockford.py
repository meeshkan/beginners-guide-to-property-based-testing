import base32_crockford
import hypothesis.strategies as some
from hypothesis import given


@given(some.integers(min_value=0))
def test_base32_crockford(input_int):
    assert base32_crockford.decode(base32_crockford.encode(input_int)) == input_int
