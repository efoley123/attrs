import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from unittest.mock import Mock
from src.attr.converters import optional, default_if_none, to_bool  # Adjust this import as needed



# Tests for `optional`
def test_optional_with_none():
    """Test that `optional` converter returns None when given None."""
    converter = Mock(return_value="mocked_value")
    opt_converter = optional(converter)
    assert opt_converter(None) is None

def test_optional_with_value():
    """Test that `optional` converter uses the provided converter for non-None values."""
    converter = Mock(return_value="mocked_value")
    opt_converter = optional(converter)
    assert opt_converter("some_value") == "mocked_value"
    converter.assert_called_once_with("some_value")

def test_optional_raises_if_converter_fails():
    """Test that `optional` propagates errors if the converter raises an exception."""
    converter = Mock(side_effect=ValueError("Conversion error"))
    opt_converter = optional(converter)
    with pytest.raises(ValueError, match="Conversion error"):
        opt_converter("invalid_value")


# Tests for `default_if_none`
def test_default_if_none_with_default():
    """Test that `default_if_none` returns the default value when None is passed."""
    converter = default_if_none(default="default_value")
    assert converter(None) == "default_value"

def test_default_if_none_with_value():
    """Test that `default_if_none` returns the original value if it's not None."""
    converter = default_if_none(default="default_value")
    assert converter("some_value") == "some_value"

def test_default_if_none_with_factory():
    """Test that `default_if_none` uses a factory when None is passed."""
    factory = Mock(return_value="factory_result")
    converter = default_if_none(factory=factory)
    assert converter(None) == "factory_result"
    factory.assert_called_once()

def test_default_if_none_raises_type_error_if_both_default_and_factory():
    """Test that `default_if_none` raises a TypeError if both default and factory are provided."""
    with pytest.raises(TypeError, match="Must pass either `default` or `factory` but not both"):
        default_if_none(default="default_value", factory=lambda: "factory_value")

def test_default_if_none_raises_type_error_if_neither_default_nor_factory():
    """Test that `default_if_none` raises a TypeError if neither default nor factory are provided."""
    with pytest.raises(TypeError, match="Must pass either `default` or `factory`."):
        default_if_none()

def test_default_if_none_raises_value_error_with_takes_self():
    """Test that `default_if_none` raises a ValueError if the factory has `takes_self=True`."""
    factory = Mock()
    factory.takes_self = True
    with pytest.raises(ValueError, match="`takes_self` is not supported by default_if_none"):
        default_if_none(factory=factory)

def test_default_if_none_with_callable_default():
    """Test that `default_if_none` handles callable defaults."""
    default_value = Mock(return_value="callable_default")
    converter = default_if_none(default=default_value)
    assert converter(None) == "callable_default"
    default_value.assert_called_once()

def test_default_if_none_with_callable_factory():
    """Test that `default_if_none` handles callable factories that accept arguments."""
    factory = lambda: "callable_factory_result"
    converter = default_if_none(factory=factory)
    assert converter(None) == "callable_factory_result"


# Tests for `to_bool`
@pytest.mark.parametrize("value, expected", [
    (True, True),
    ("true", True),
    ("t", True),
    ("yes", True),
    ("y", True),
    ("on", True),
    ("1", True),
    (1, True),
    (False, False),
    ("false", False),
    ("f", False),
    ("no", False),
    ("n", False),
    ("off", False),
    ("0", False),
    (0, False)
])
def test_to_bool(value, expected):
    """Test that `to_bool` correctly converts truthy and falsy values."""
    assert to_bool(value) == expected

def test_to_bool_invalid_value():
    """Test that `to_bool` raises ValueError for invalid input values."""
    with pytest.raises(ValueError, match="Cannot convert value to bool"):
        to_bool("not_a_boolean")

def test_to_bool_handles_uppercase_values():
    """Test that `to_bool` correctly handles uppercase input values."""
    assert to_bool("TRUE") is True
    assert to_bool("FALSE") is False

def test_to_bool_handles_whitespace():
    """Test that `to_bool` trims whitespace before converting."""
    assert to_bool(" true ") is True
    assert to_bool(" false ") is False

def test_to_bool_with_non_string_iterable():
    """Test that `to_bool` raises ValueError for non-string iterable inputs."""
    with pytest.raises(ValueError, match="Cannot convert value to bool"):
        to_bool([])

def test_to_bool_with_unhashable_input():
    """Test that `to_bool` raises ValueError for unhashable inputs."""
    with pytest.raises(ValueError, match="Cannot convert value to bool"):
        to_bool({})
