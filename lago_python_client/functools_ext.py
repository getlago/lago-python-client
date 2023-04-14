import sys
from typing import Any, TypeVar
import warnings
try:
    from functools import cached_property
except ImportError:
    cached_property = property  # type: ignore
try:
    from typing import ParamSpec
except ImportError:  # Python 3.7, Python 3.8, Python 3.9
    from typing_extensions import ParamSpec
if sys.version_info >= (3, 9):
    from collections.abc import Callable

T = TypeVar("T")
P = ParamSpec("P")


class Proxy(object):
    def __init__(self, _obj: object) -> None:
        object.__setattr__(self, "_obj", _obj)

    def __getattr__(self, name) -> Any:
        if name == "_obj":
            return object.__getattribute__(self, name)
        return getattr(object.__getattribute__(self, "_obj"), name)

    def __setattr__(self, name, value) -> None:
        setattr(self._obj, name, value)

    def __call__(self) -> Any:
        warnings.warn(
            ''.join((
                'We are going to deprecate callable properties (`client.<your_tag_name>()`) in future. ',
                'Please, remove braces. ',
                'Use `client.<your_tag_name>.<your_operation_name>(...)` instead of `client.<your_tag_name>().<your_operation_name>(...)`',
            )),
            PendingDeprecationWarning,
        )
        return self._obj

    def __repr__(self) -> str:
        return repr(self._obj)

    def __str__(self) -> str:
        return str(self._obj)

    def __format__(self, format_spec: str) -> str:
        return format(self._obj, format_spec)

    def __hash__(self) -> int:
        return hash(self._obj)


if sys.version_info >= (3, 9):
    def callable_cached_property(func: Callable[P, T]) -> cached_property[T]:
        return cached_property(lambda s: Proxy(func(s)))  # type: ignore
else:
    def callable_cached_property(func):
        return cached_property(lambda s: Proxy(func(s)))
