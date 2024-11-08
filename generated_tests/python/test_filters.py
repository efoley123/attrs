import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from unittest.mock import MagicMock
from src.attr.filters import include, exclude, _split_what
from src.attr._make import Attribute

class TestSplitWhat:
    """
    Tests for the _split_what function.
    """

    def test_empty_input(self):
        """
        Test with empty input.
        """
        assert _split_what([]) == (frozenset(), frozenset(), frozenset())

    def test_splits_correctly(self):
        """
        Test that input is split correctly into classes, strings, and Attributes.
        """
        class DummyClass:
            pass

        attr1 = Attribute(name='attr1')
        result = _split_what([DummyClass, 'attr_name', attr1])
        assert result == (frozenset([DummyClass]), frozenset(['attr_name']), frozenset([attr1]))

    def test_unsupported_types(self):
        """
        Test with unsupported types.
        """
        with pytest.raises(TypeError):
            _split_what([123])


class TestInclude:
    """
    Tests for the include filter factory.
    """

    def setup_method(self):
        self.attr = MagicMock(spec=Attribute)
        self.attr.name = 'test_attr'

    def test_include_specific_class(self):
        """
        Test including a specific class only.
        """
        filter_ = include(int)
        assert filter_(self.attr, 123) is True
        assert filter_(self.attr, 'string') is False

    def test_include_specific_attribute(self):
        """
        Test including a specific attribute by name.
        """
        filter_ = include('test_attr')
        assert filter_(self.attr, 123) is True
        self.attr.name = 'other_attr'
        assert filter_(self.attr, 123) is False

    def test_include_attribute_object(self):
        """
        Test including a specific attribute object.
        """
        included_attr = Attribute(name='included')
        filter_ = include(included_attr)
        assert filter_(included_attr, 123) is True
        self.attr.name = 'other_attr'
        assert filter_(self.attr, 123) is False


class TestExclude:
    """
    Tests for the exclude filter factory.
    """

    def setup_method(self):
        self.attr = MagicMock(spec=Attribute)
        self.attr.name = 'test_attr'

    def test_exclude_specific_class(self):
        """
        Test excluding a specific class only.
        """
        filter_ = exclude(int)
        assert filter_(self.attr, 123) is False
        assert filter_(self.attr, 'string') is True

    def test_exclude_specific_attribute(self):
        """
        Test excluding a specific attribute by name.
        """
        filter_ = exclude('test_attr')
        assert filter_(self.attr, 123) is False
        self.attr.name = 'other_attr'
        assert filter_(self.attr, 123) is True

    def test_exclude_attribute_object(self):
        """
        Test excluding a specific attribute object.
        """
        excluded_attr = Attribute(name='excluded')
        filter_ = exclude(excluded_attr)
        assert filter_(excluded_attr, 123) is False
        self.attr.name = 'other_attr'
        assert filter_(self.attr, 123) is True

```
This suite of tests covers normal, edge, and error cases for the functionality in `src/attr/filters.py`, employing mocking for the `Attribute` class to avoid dependencies on the actual implementation. It ensures high code coverage and tests both success and failure scenarios as requested.