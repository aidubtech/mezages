import re
from typing import Any


root_path = '%root%'


class PathError(Exception):
    pass


class Path:
    KEY_TOKEN_REGEX = r'(?:\{[a-z0-9_]+\})'
    INDEX_TOKEN_REGEX = r'(?:\[\d+\])'
    UNKNOWN_TOKEN_REGEX = '(?:[a-z0-9_]+)'
    TOKEN_REGEX = f'(?:{KEY_TOKEN_REGEX}|{INDEX_TOKEN_REGEX}|{UNKNOWN_TOKEN_REGEX})'
    PATH_PATTERN = re.compile(fr'(?:(?:{TOKEN_REGEX}\.)*{TOKEN_REGEX})')

    @classmethod
    def valid(cls, value: Any) -> bool:
        return value == root_path or (
            isinstance(value, str) and bool(cls.PATH_PATTERN.fullmatch(value))
        )

    def __init__(self, value: str = root_path) -> None:
        self.__value = self.__ensure_path(value)

    @property
    def value(self) -> str:
        return self.__value

    @property
    def is_root(self) -> bool:
        if not hasattr(self, '_Path__is_root'):
            result = self.__value == root_path
            setattr(self, '_Path__is_root', result)

        return getattr(self, '_Path__is_root')

    @property
    def substitute(self) -> str:
        if not hasattr(self, '_Path__is_root'):
            # Add substitute logic here correctly set result
            result = str() if self.is_root else self.value
            setattr(self, '_Path__is_root', result)

        return getattr(self, '_Path__is_root')

    def __ensure_path(self, value: Any) -> str:
        if self.__class__.valid(value): return str(value)
        raise PathError(f'{repr(value)} is not a valid path')
