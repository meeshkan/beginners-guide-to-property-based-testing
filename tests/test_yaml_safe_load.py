import hypothesis.strategies as some
import yaml
from hypothesis import given


@given(some.text())
def test_yaml_safe_load(input_string):
    try:
        yaml.safe_load(input_string)
    except yaml.YAMLError:
        # except yaml.reader.ReaderError:
        pass


def test_yaml_safe_load_single_apostrophe():
    try:
        yaml.safe_load("'")
        assert False
    except yaml.scanner.ScannerError:
        pass


def test_yaml_safe_load_not_zero():
    try:
        yaml.safe_load("!0")
        assert False
    except yaml.constructor.ConstructorError:
        pass
