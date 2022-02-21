from typing import Any, Generic, Iterator, Tuple, TypeVar

from ..exceptions import FailedResponse


__all__ = ['BaseAPIModel']


T = TypeVar('T')


class BaseAPIModel(Generic[T]):
    def __new__(cls, *args, **payload):
        instance = super().__new__(cls)

        if payload.get('error', None):
            """Sometimes the server will send an error field when there is no cached response"""
            raise FailedResponse(payload['error'])
            
        return instance

    def __init__(self, iterable: Tuple[T]) -> None:
        self._iterable = iterable

    def __getitem__(self, index: int) -> T:
        return self._iterable.__getitem__(index)

    def __iter__(self) -> Iterator[T]:
        return self._iterable.__iter__()

    def __next__(self) -> T:
        return next(self._iterable)

    def __len__(self) -> int:
        return self._iterable.__len__()

    def __str__(self) -> str:
        return self._iterable.__str__()

    def __repr__(self) -> str:
        return self._iterable.__str__()
