import json

import hypothesis.strategies as some
from hypothesis import example, given

# Regardless of input, `json.loads()` never throws any exceptions other than `json.JSONDecodeError`
@given(some.text())
@example("[")
def test_json_loads(input_string):
    try:
        json.loads(input_string)
    except json.JSONDecodeError:
        return
