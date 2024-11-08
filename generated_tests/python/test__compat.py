import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
import threading
import platform
import sys
from unittest.mock import patch

from src.attr._compat import _AnnotationExtractor, get_generic_base, PYPY, PY_3_9_PLUS, _get_annotations, repr_context


@pytest.mark.parametrize("callable,expected", [
    (lambda x: x, int),
    ((lambda x, y: x + y), int),
    (lambda: None, None)
])
def test_AnnotationExtractor_get_first_param_type_success_cases(callable, expected):
    """
    Test _AnnotationExtractor.get_first_param_type with different callables
    """
    ae = _AnnotationExtractor(callable)
    assert ae.get_first_param_type() is expected


@pytest.mark.parametrize("callable", [
    42,
    "not a callable"
])
def test_AnnotationExtractor_get_first_param_type_failure_cases(callable):
    """
    Test _AnnotationExtractor.get_first_param_type with non-callable inputs
    """
    ae = _AnnotationExtractor(callable)
    assert ae.get_first_param_type() is None


def test_AnnotationExtractor_get_return_type():
    """
    Test _AnnotationExtractor.get_return_type with a simple function
    """
    def func() -> int:
        return 42

    ae = _AnnotationExtractor(func)
    assert ae.get_return_type() is int


def test_repr_context_thread_locality():
    """
    Test if repr_context is thread-local by modifying it in a new thread
    """
    def modify_repr_context():
        repr_context.marker = True

    t = threading.Thread(target=modify_repr_context)
    t.start()
    t.join()

    assert not hasattr(repr_context, "marker")


@pytest.mark.parametrize("version_info,expected", [
    ((3, 9), PY_3_9_PLUS),
    ((3, 10), PY_3_10_PLUS),
    ((3, 11), PY_3_11_PLUS),
    ((3, 12), PY_3_12_PLUS),
    ((3, 13), PY_3_13_PLUS),
    ((3, 14), PY_3_14_PLUS)
])
def test_python_version_flags(version_info, expected):
    """
    Test Python version flags for correctness
    """
    assert (sys.version_info[:2] >= version_info) is expected


@pytest.mark.parametrize("implementation,expected", [
    ("CPython", False),
    ("PyPy", True)
])
def test_PYPY_flag(implementation, expected):
    """
    Test the PYPY flag value based on different Python implementations
    """
    with patch("platform.python_implementation", return_value=implementation):
        assert (platform.python_implementation() == "PyPy") is expected


@pytest.mark.parametrize("cls,expected", [
    (dict, None),  # Not a generic class
    (list, None),  # Not a generic class
])
def test_get_generic_base_non_generic(cls, expected):
    """
    Test get_generic_base with non-generic classes
    """
    assert get_generic_base(cls) is expected


class TestGetAnnotations:
    """
    Tests for _get_annotations function
    """

    def test_get_annotations_existing(self):
        """
        Test _get_annotations with a class that has annotations
        """
        class AnnotatedClass:
            __annotations__ = {'name': str, 'value': int}

        annotations = _get_annotations(AnnotatedClass)
        assert annotations == {'name': str, 'value': int}

    def test_get_annotations_missing(self):
        """
        Test _get_annotations with a class that lacks annotations
        """
        class UnannotatedClass:
            pass

        annotations = _get_annotations(UnannotatedClass)
        assert annotations == {}