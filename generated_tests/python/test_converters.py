import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# File: test_converters.py
import pytest
from unittest.mock import Mock
from src.attr.converters import default_if_none, optional, to_bool


# Tests for optional
@pytest.mark.parametrize("input,output", [
    (None, None),
    (1, 1),
    ('string', 'string')
])
def test_optional_normal_cases(input, output):
    """Test optional with normal cases."""
    converter_mock = Mock(return_value=output)
    converter = optional(converter_mock)
    assert converter(input) == output
    if input is not None:
        converter_mock.assert_called_once_with(input)


def test_optional_propagates_conversion_error():
    """Test optional propagates the underlying conversion error."""
    def failing_converter(value):
        raise ValueError("Conversion failed")

    converter = optional(failing_converter)
    with pytest.raises(ValueError, match="Conversion failed"):
        converter("test")


# Tests for default_if_none
def test_default_if_none_with_default():
    """Test default_if_none replaces None with the default value."""
    converter = default_if_none(default=42)
    assert converter(None) == 42
    assert converter(24) == 24


def test_default_if_none_with_factory():
    """Test default_if_none replaces None with the factory output."""
    factory_mock = Mock(return_value=42)
    converter = default_if_none(factory=factory_mock)
    assert converter(None) == 42
    factory_mock.assert_called_once()


def test_default_if_none_raises_type_error_on_missing_both_default_and_factory():
    """Test default_if_none raises TypeError if neither default nor factory are provided."""
    with pytest.raises(TypeError):
        default_if_none()


def test_default_if_none_raises_type_error_on_both_default_and_factory():
    """Test default_if_none raises TypeError if both default and factory are provided."""
    with pytest.raises(TypeError):
        default_if_none(default=42, factory=lambda: 42)


def test_default_if_none_raises_value_error_on_factory_takes_self():
    """Test default_if_none raises ValueError if factory has takes_self=True."""
    with pytest.raises(ValueError):
        default_if_none(factory=Factory(Mock, takes_self=True))


# Tests for to_bool
@pytest.mark.parametrize("input", [
    "true", "t", "yes", "y", "on", "1", 1, True
])
def test_to_bool_truthy_values(input):
    """Test to_bool correctly converts truthy values to True."""
    assert to_bool(input) is True


@pytest.mark.parametrize("input", [
    "false", "f", "no", "n", "off", "0", 0, False
])
def test_to_bool_falsy_values(input):
    """Test to_bool correctly converts falsy values to False."""
    assert to_bool(input) is False


@pytest.mark.parametrize("input", [
    "not_a_bool", 2, -1, [], {}
])
def test_to_bool_raises_value_error_on_invalid_input(input):
    """Test to_bool raises ValueError on invalid input."""
    with pytest.raises(ValueError):
        to_bool(input)


def test_to_bool_unhashable_type():
    """Test to_bool handles unhashable types by raising ValueError."""
    with pytest.raises(ValueError, match="Cannot convert value to bool"):
        to_bool([])
```
This test suite covers normal, edge, and error cases for the converters in `src/attr/converters.py`, mocking external dependencies where necessary, and adhering to pytest best practices for clear, descriptive test names and docstrings.