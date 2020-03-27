import json
from string import printable

import hypothesis.strategies as some
import json5
from hypothesis import example, given, settings

some_object = some.recursive(
    some.none() | some.booleans() | some.floats(allow_nan=False) | some.text(printable),
    lambda children: some.lists(children, min_size=1)
    | some.dictionaries(some.text(printable), children, min_size=1),
)


@given(some_object)
@settings(max_examples=500)
@example({"": "hi"})
def test_json5_loads(input_object):
    dumped_json_string = json.dumps(input_object)
    dumped_json5_string = json5.dumps(input_object)

    parsed_object_from_json = json5.loads(dumped_json_string)
    parsed_object_from_json5 = json5.loads(dumped_json5_string)

    assert parsed_object_from_json == input_object
    assert parsed_object_from_json5 == input_object
