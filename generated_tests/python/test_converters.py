import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# test_converters.py
import pytest
from unittest.mock import Mock

from src.attr.converters import default_if_none, optional, to_bool


@pytest.fixture
def mock_factory():
    """Fixture for creating a mock Factory."""
    factory = Mock()
    factory.takes_self = False
    factory.factory = Mock(return_value='mock_factory_result')
    return factory


def test_optional_with_none_returns_none():
    """Test that the optional converter returns None when given None."""
    converter = optional(int)
    assert converter(None) is None


def test_optional_with_valid_value():
    """Test that the optional converter applies the wrapped converter to non-None values."""
    converter = optional(int)
    assert converter("42") == 42


def test_optional_raises_error_with_invalid_value():
    """Test that the optional converter raises an error for invalid values."""
    converter = optional(int)
    with pytest.raises(ValueError):
        converter("not_an_int")


def test_default_if_none_with_none_and_default():
    """Test default_if_none returns the default value if None is passed."""
    converter = default_if_none(default=42)
    assert converter(None) == 42


def test_default_if_none_with_value():
    """Test default_if_none passes through the value if not None."""
    converter = default_if_none(default=42)
    assert converter(24) == 24


def test_default_if_none_with_factory(mock_factory):
    """Test default_if_none uses the factory if None is passed."""
    converter = default_if_none(factory=mock_factory.factory)
    assert converter(None) == 'mock_factory_result'


def test_default_if_none_raises_type_error_without_default_or_factory():
    """Test default_if_none raises TypeError if neither default nor factory is given."""
    with pytest.raises(TypeError):
        default_if_none()


def test_default_if_none_raises_type_error_with_both_default_and_factory():
    """Test default_if_none raises TypeError if both default and factory are given."""
    with pytest.raises(TypeError):
        default_if_none(default=42, factory=lambda: 0)


def test_default_if_none_raises_value_error_with_factory_takes_self():
    """Test default_if_none raises ValueError if the factory has takes_self=True."""
    factory = Mock()
    factory.takes_self = True
    with pytest.raises(ValueError):
        default_if_none(factory=factory)


@pytest.mark.parametrize("input_value,expected", [
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
    (0, False),
])
def test_to_bool_with_valid_values(input_value, expected):
    """Test to_bool correctly converts valid truthy and falsy values."""
    assert to_bool(input_value) == expected


@pytest.mark.parametrize("invalid_value", [
    "not_a_bool",
    [],
    {},
    2,
    -1,
    "trueish",
    "falsy"
])
def test_to_bool_raises_value_error_with_invalid_values(invalid_value):
    """Test to_bool raises ValueError for invalid values."""
    with pytest.raises(ValueError):
        to_bool(invalid_value)