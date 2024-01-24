from re import compile
from typing import Any
from mezages.token import Token


root_path = '%root%'


class PathError(Exception):
    pass


class Path(str):
    PATH_PATTERN = compile(fr'(?:(?:{Token.TOKEN_REGEX}\.)*{Token.TOKEN_REGEX})')

    @classmethod
    def is_valid(cls, argument: Any) -> bool:
        return argument == root_path or (
            isinstance(argument, str) and bool(
                cls.PATH_PATTERN.fullmatch(argument)
            )
        )

    @classmethod
    def ensure(cls, argument: Any) -> str:
        if cls.is_valid(argument): return str(argument)
        raise PathError(f'{repr(argument)} is an invalid path')

    def __new__(cls, initval: Any):
        return super().__new__(cls, cls.ensure(initval))

    @property
    def is_root(self):
        return self == root_path
