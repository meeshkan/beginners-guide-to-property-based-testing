import json
from string import printable

import hypothesis.strategies as some
import json5
from hypothesis import example, given, settings

# Construct a generator of arbitrary objects to test serialization on:
some_object = some.recursive(
    some.none() | some.booleans() | some.floats(allow_nan=False) | some.text(printable),
    lambda children: some.lists(children, min_size=1)
    | some.dictionaries(some.text(printable), children, min_size=1),
)


@given(some_object)
# Sets the number of test cases to 500 rather than the default 100:
@settings(max_examples=500)
# Add a hard-coded example to the generated input to prevent future issues.
# Comment out the following line if you want to discover the bug yourself:
@example({"": None})
def test_json5_loads(input_object):
    dumped_json_string = json.dumps(input_object)
    dumped_json5_string = json5.dumps(input_object)

    parsed_object_from_json = json5.loads(dumped_json_string)
    parsed_object_from_json5 = json5.loads(dumped_json5_string)

    assert parsed_object_from_json == input_object
    assert parsed_object_from_json5 == input_object
