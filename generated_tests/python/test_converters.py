import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# File: tests/test_converters.py
import pytest
from unittest.mock import MagicMock

from src.attr.converters import default_if_none, optional, to_bool


@pytest.fixture
def setup_factory_mock():
    factory_mock = MagicMock()
    factory_mock.factory = MagicMock(return_value='factory_result')
    factory_mock.takes_self = False
    yield factory_mock


class TestOptional:
    def test_optional_success(self):
        assert optional(int)(None) is None, "Should return None for None input"
        assert optional(int)('123') == 123, "Should convert string to int"

    def test_optional_raises_error(self):
        with pytest.raises(ValueError):
            optional(int)('abc'), "Should raise ValueError for invalid int conversion"


class TestDefaultIfNone:
    def test_default_if_none_with_default(self):
        converter = default_if_none(default=42)
        assert converter(None) == 42, "Should return default value when None is passed"

    def test_default_if_none_with_factory(self, setup_factory_mock):
        factory_mock = setup_factory_mock
        converter = default_if_none(factory=factory_mock.factory)
        assert converter(None) == 'factory_result', "Should return factory result when None is passed"

    def test_default_if_none_with_value(self):
        converter = default_if_none(default=42)
        assert converter(24) == 24, "Should return passed value when it's not None"

    def test_default_if_none_raises_type_error(self):
        with pytest.raises(TypeError):
            default_if_none(), "Should raise TypeError when neither default nor factory are provided"

    def test_default_if_none_raises_type_error_both_provided(self):
        with pytest.raises(TypeError):
            default_if_none(default=42, factory=lambda: 0), "Should raise TypeError when both default and factory are provided"

    def test_default_if_none_raises_value_error_takes_self(self, setup_factory_mock):
        factory_mock = setup_factory_mock
        factory_mock.takes_self = True
        with pytest.raises(ValueError):
            default_if_none(default=Factory(factory_mock)), "Should raise ValueError when factory with takes_self=True is provided"


class TestToBool:
    @pytest.mark.parametrize("value, expected", [
        ('true', True), ('t', True), ('yes', True), ('y', True), ('on', True), ('1', True), (1, True),
        ('false', False), ('f', False), ('no', False), ('n', False), ('off', False), ('0', False), (0, False),
    ])
    def test_to_bool_success(self, value, expected):
        assert to_bool(value) == expected, f"Should convert {value!r} to {expected}"

    @pytest.mark.parametrize("value", ['not_a_bool', 2, -1, None, [], {}])
    def test_to_bool_failure(self, value):
        with pytest.raises(ValueError):
            to_bool(value), f"Should raise ValueError for {value!r}"

    # Edge case: Unhashable types (e.g., lists) that cannot be directly converted or looked up
    def test_to_bool_unhashable_type(self):
        with pytest.raises(ValueError):
            to_bool([]), "Should raise ValueError for unhashable types like lists"