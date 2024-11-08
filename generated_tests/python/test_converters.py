import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# test_converters.py

import pytest
from src.attr.converters import default_if_none, optional, to_bool
from src.attr._make import NOTHING, Factory

@pytest.mark.parametrize("input_value,expected", [
    (None, None),
    ("42", 42),
    (42, 42),
])
def test_optional_success(input_value, expected):
    """Test the `optional` converter with various inputs."""
    converter = optional(int)
    assert converter(input_value) == expected

def test_optional_fail():
    """Test the `optional` converter fails with invalid input."""
    converter = optional(int)
    with pytest.raises(ValueError):
        converter("not_an_int")

@pytest.mark.parametrize("default,factory,value,expected", [
    (42, None, None, 42),
    (None, lambda: 42, None, 42),
    ('default', None, 'value', 'value'),
])
def test_default_if_none_success(default, factory, value, expected):
    """Test `default_if_none` successfully returns the correct values."""
    converter = default_if_none(default=default, factory=factory)
    assert converter(value) == expected

def test_default_if_none_missing_both():
    """Test `default_if_none` raises TypeError when both default and factory are missing."""
    with pytest.raises(TypeError):
        default_if_none()

def test_default_if_none_both_provided():
    """Test `default_if_none` raises TypeError when both default and factory are provided."""
    with pytest.raises(TypeError):
        default_if_none(default=42, factory=lambda: 42)

def test_default_if_none_factory_takes_self():
    """Test `default_if_none` raises ValueError when factory with `takes_self=True` is provided."""
    with pytest.raises(ValueError):
        default_if_none(factory=Factory(lambda: 42, takes_self=True))

@pytest.mark.parametrize("value,expected", [
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
def test_to_bool_success(value, expected):
    """Test `to_bool` converter successfully converts various truthy and falsy inputs."""
    assert to_bool(value) == expected

@pytest.mark.parametrize("value", [
    "not_a_bool",
    2,
    [],
    {},
])
def test_to_bool_fail(value):
    """Test `to_bool` raises ValueError for unconvertible inputs."""
    with pytest.raises(ValueError):
        to_bool(value)