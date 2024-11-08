import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# test_converters.py

import pytest
from unittest.mock import MagicMock
from src.attr.converters import optional, default_if_none, to_bool, pipe

# Optional Converter Tests

def test_optional_with_none():
    """Test that optional converter returns None for None input."""
    converter = optional(int)
    assert converter(None) is None

def test_optional_with_valid_input():
    """Test that optional converter correctly processes valid input."""
    converter = optional(int)
    assert converter("123") == 123

def test_optional_with_invalid_input():
    """Test that optional converter raises an error for invalid input."""
    converter = optional(int)
    with pytest.raises(ValueError):
        converter("abc")

# Default If None Converter Tests

def test_default_if_none_without_default_or_factory_raises_type_error():
    """Test that default_if_none raises a TypeError if neither default nor factory is provided."""
    with pytest.raises(TypeError):
        default_if_none()

def test_default_if_none_with_both_default_and_factory_raises_type_error():
    """Test that default_if_none raises a TypeError if both default and factory are provided."""
    with pytest.raises(TypeError):
        default_if_none(default=1, factory=lambda: 2)

def test_default_if_none_with_factory_takes_self_raises_value_error():
    """Test that default_if_none raises a ValueError if factory has takes_self=True."""
    factory = Factory(lambda: 2, takes_self=True)
    with pytest.raises(ValueError):
        default_if_none(factory=factory)

def test_default_if_none_with_valid_default():
    """Test that default_if_none correctly uses the default value."""
    converter = default_if_none(default="default")
    assert converter(None) == "default"
    assert converter(1) == 1

def test_default_if_none_with_valid_factory():
    """Test that default_if_none correctly uses a factory."""
    converter = default_if_none(factory=lambda: "factory")
    assert converter(None) == "factory"
    assert converter(1) == 1

# To Bool Converter Tests

@pytest.mark.parametrize("input,expected", [
    ("true", True),
    ("t", True),
    ("yes", True),
    ("y", True),
    ("on", True),
    ("1", True),
    (1, True),
    ("false", False),
    ("f", False),
    ("no", False),
    ("n", False),
    ("off", False),
    ("0", False),
    (0, False),
])
def test_to_bool_valid_cases(input, expected):
    """Test that to_bool converts various inputs correctly."""
    assert to_bool(input) == expected

def test_to_bool_invalid_case():
    """Test that to_bool raises ValueError for invalid inputs."""
    with pytest.raises(ValueError):
        to_bool("invalid")

# Pipe Converter Tests

def test_pipe_with_multiple_converters():
    """Test that pipe applies multiple converters in sequence."""
    converter = pipe(str, int)
    assert converter("123") == 123

def test_pipe_with_failure_in_sequence():
    """Test that pipe raises an error if any converter in the sequence fails."""
    converter = pipe(str, int)  # int("abc") should fail
    with pytest.raises(ValueError):
        converter("abc")