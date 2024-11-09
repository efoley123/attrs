import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from unittest.mock import Mock, patch
from src.attr.converters import default_if_none, optional, to_bool

# The setup and teardown mechanisms are not explicitly needed for these tests 
# as pytest handles most of the isolation between tests. However, if external 
# resources or states were to be modified, fixtures with setup and teardown 
# could be used.

@pytest.mark.parametrize("input_val,expected", [
    (None, None),
    ("test", "test"),
    (123, 123),
    (True, True)
])
def test_optional_normal_cases(input_val, expected):
    """
    Test normal behavior of optional converter.
    """
    converter = optional(lambda x: x)  # Identity converter
    assert converter(input_val) == expected


def test_optional_type_annotation_inference():
    """
    Test if the optional converter correctly infers type annotations.
    """
    def converter(val: int) -> str:
        return str(val)
    
    wrapped_converter = optional(converter)
    assert wrapped_converter.__annotations__['val'] == typing.Optional[int]
    assert wrapped_converter.__annotations__['return'] == typing.Optional[str]


def test_optional_propagates_conversion_error():
    """
    Test if the optional converter propagates the underlying conversion error.
    """
    def failing_converter(val):
        raise ValueError("Conversion failed")

    converter = optional(failing_converter)
    with pytest.raises(ValueError, match="Conversion failed"):
        converter("any_value")


@pytest.mark.parametrize("default,factory,value,expected", [
    ("default", None, None, "default"),
    (None, lambda: "factory", None, "factory"),
    (42, None, 24, 24),
    (None, lambda: 42, 24, 24)
])
def test_default_if_none_normal_cases(default, factory, value, expected):
    """
    Test normal behavior of default_if_none converter.
    """
    converter = default_if_none(default=default, factory=factory)
    assert converter(value) == expected


def test_default_if_none_raises_type_error_on_missing_both():
    """
    Test if TypeError is raised when both default and factory are missing.
    """
    with pytest.raises(TypeError, match="Must pass either `default` or `factory`."):
        default_if_none()


def test_default_if_none_raises_type_error_on_both_provided():
    """
    Test if TypeError is raised when both default and factory are provided.
    """
    with pytest.raises(TypeError, match="but not both."):
        default_if_none(default=True, factory=lambda: False)


def test_default_if_none_raises_value_error_on_factory_with_takes_self():
    """
    Test if ValueError is raised when factory with `takes_self=True` is provided.
    """
    with pytest.raises(ValueError, match="`takes_self` is not supported by default_if_none."):
        default_if_none(factory=Factory(Mock, takes_self=True))


@pytest.mark.parametrize("input_val,expected", [
    ("true", True),
    ("t", True),
    ("yes", True),
    ("on", True),
    ("1", True),
    (1, True),
    ("false", False),
    ("f", False),
    ("no", False),
    ("off", False),
    ("0", False),
    (0, False)
])
def test_to_bool_normal_cases(input_val, expected):
    """
    Test normal cases for to_bool converter.
    """
    assert to_bool(input_val) == expected


@pytest.mark.parametrize("input_val", [
    "invalid",
    [],
    {},
    2,
    -1,
    "True"  # Case sensitivity check
])
def test_to_bool_error_cases(input_val):
    """
    Test error cases for to_bool converter.
    """
    with pytest.raises(ValueError, match="Cannot convert value to bool"):
        to_bool(input_val)