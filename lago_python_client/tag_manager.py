import sys

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class TagManager:
    """Tag manager used in `Client` class to group operations by tags."""

    def __init__(self, base_url: str, api_key: str, operations: Mapping[str, Callable[..., Callable]]) -> None:
        self.base_url: str = base_url
        self.api_key: str = api_key

        for operation_name, Operation in operations.items():
            setattr(self, operation_name, Operation(base_url=base_url, api_key=api_key))
