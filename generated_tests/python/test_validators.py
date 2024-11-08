import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.attr.validators import (
    set_disabled,
    get_disabled,
    instance_of,
    matches_re,
    optional,
    in_,
    is_callable,
    deep_iterable,
    deep_mapping,
    lt,
    le,
    ge,
    gt,
    max_len,
    min_len,
    disabled,
)
from src.attr.exceptions import NotCallableError
from re import compile, fullmatch, search, match
from collections.abc import Iterable, Mapping

# Mock external dependencies if any


class TestValidators:
    def test_set_disabled_enables_validators(self):
        set_disabled(False)
        assert not get_disabled()

    def test_set_disabled_disables_validators(self):
        set_disabled(True)
        assert get_disabled()

    def test_instance_of_with_correct_type(self):
        validator = instance_of(int)
        validator(None, None, 5)  # Should not raise

    def test_instance_of_with_incorrect_type(self):
        validator = instance_of(int)
        with pytest.raises(TypeError):
            validator(None, None, "string")

    def test_matches_re_with_fullmatch(self):
        validator = matches_re(r"\d+", func=fullmatch)
        validator(None, None, "12345")  # Should not raise
    
    def test_matches_re_with_search(self):
        validator = matches_re(r"\d+", func=search)
        validator(None, None, "abc12345xyz")  # Should not raise

    def test_matches_re_with_match(self):
        validator = matches_re(r"\d+", func=match)
        validator(None, None, "12345xyz")  # Should not raise

    def test_matches_re_failure(self):
        validator = matches_re(r"\d+", func=fullmatch)
        with pytest.raises(ValueError):
            validator(None, None, "abc")

    def test_optional_with_none(self):
        validator = optional(instance_of(int))
        validator(None, None, None)  # Should not raise

    def test_optional_with_valid_value(self):
        validator = optional(instance_of(int))
        validator(None, None, 5)  # Should not raise

    def test_in_with_valid_option(self):
        validator = in_([1, 2, 3])
        validator(None, None, 2)  # Should not raise

    def test_in_with_invalid_option(self):
        validator = in_([1, 2, 3])
        with pytest.raises(ValueError):
            validator(None, None, 4)

    def test_is_callable_with_callable(self):
        validator = is_callable()
        validator(None, None, lambda x: x)  # Should not raise

    def test_is_callable_with_non_callable(self):
        validator = is_callable()
        with pytest.raises(NotCallableError):
            validator(None, None, "not callable")

    def test_deep_iterable_with_valid_data(self):
        validator = deep_iterable(instance_of(int), instance_of(list))
        validator(None, None, [1, 2, 3])  # Should not raise

    def test_deep_mapping_with_valid_data(self):
        validator = deep_mapping(instance_of(str), instance_of(int))
        validator(None, None, {"a": 1, "b": 2})  # Should not raise

    def test_lt_validator(self):
        validator = lt(10)
        validator(None, None, 5)  # Should not raise

    def test_lt_validator_failure(self):
        validator = lt(10)
        with pytest.raises(ValueError):
            validator(None, None, 10)

    def test_le_validator(self):
        validator = le(10)
        validator(None, None, 10)  # Should not raise

    def test_ge_validator(self):
        validator = ge(10)
        validator(None, None, 10)  # Should not raise

    def test_gt_validator(self):
        validator = gt(10)
        validator(None, None, 11)  # Should not raise

    def test_max_len_validator(self):
        validator = max_len(5)
        validator(None, None, "12345")  # Should not raise

    def test_max_len_validator_failure(self):
        validator = max_len(5)
        with pytest.raises(ValueError):
            validator(None, None, "123456")

    def test_min_len_validator(self):
        validator = min_len(5)
        validator(None, None, "12345")  # Should not raise

    def test_min_len_validator_failure(self):
        validator = min_len(5)
        with pytest.raises(ValueError):
            validator(None, None, "1234")

    def test_disabled_context_manager(self):
        with disabled():
            assert get_disabled()
        assert not get_disabled()