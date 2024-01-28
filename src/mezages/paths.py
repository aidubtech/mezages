from re import compile
from typing import Any, Literal, Optional


#----------------------------------------
# TYPE ALIASES
#----------------------------------------

TokenType = Literal['key'] | Literal['index']


#----------------------------------------
# CONSTANTS
#----------------------------------------

ROOT_PATH = '%root%'

KEY_TOKEN_REGEX = r'(?:\{[a-z0-9_]+\})'
KEY_TOKEN_PATTERN = compile(KEY_TOKEN_REGEX)

INDEX_TOKEN_REGEX = r'(?:\[\d+\])'
INDEX_TOKEN_PATTERN = compile(INDEX_TOKEN_REGEX)

UNKNOWN_TOKEN_REGEX = '(?:[a-z0-9_]+)'

TOKEN_REGEX = f'(?:{KEY_TOKEN_REGEX}|{INDEX_TOKEN_REGEX}|{UNKNOWN_TOKEN_REGEX})'

PATH_PATTERN = compile(fr'(?:(?:{TOKEN_REGEX}\.)*{TOKEN_REGEX})')


#----------------------------------------
# ERROR CLASSES
#----------------------------------------

class PathError(Exception):
    pass


#----------------------------------------
# REUSABLE PROCEDURES
#----------------------------------------

def is_valid_path(argument: Any) -> bool:
    return argument == ROOT_PATH or (
        isinstance(argument, str) and bool(
            PATH_PATTERN.fullmatch(argument)
        )
    )


def ensure_path(argument: Any) -> str:
    if is_valid_path(argument): return argument
    raise PathError(f'{repr(argument)} is an invalid path')


def get_token_type(token: str) -> Optional[TokenType]:
    if bool(KEY_TOKEN_PATTERN.fullmatch(token)): return 'key'
    if bool(INDEX_TOKEN_PATTERN.fullmatch(token)): return 'index'
