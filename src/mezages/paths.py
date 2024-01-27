import re
from typing import Any, Literal


#----------------------------------------
# TYPE ALIASES
#----------------------------------------

TokenType = Literal['key'] | Literal['index'] | Literal['unknown']


#----------------------------------------
# CONSTANTS
#----------------------------------------

ROOT_PATH = '%root%'

TOKEN_REGEX = r'(?:[^\.]+)'

KEY_TOKEN_REGEX = r'(?:\{[a-z0-9_]+\})'
KEY_TOKEN_PATTERN = re.compile(KEY_TOKEN_REGEX)

INDEX_TOKEN_REGEX = r'(?:\[\d+\])'
INDEX_TOKEN_PATTERN = re.compile(INDEX_TOKEN_REGEX)

PATH_PATTERN = re.compile(fr'(?:(?:{TOKEN_REGEX}\.)*{TOKEN_REGEX})')


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


def get_token_type(token: str) -> TokenType:
    if bool(KEY_TOKEN_PATTERN.fullmatch(token)): return 'key'
    if bool(INDEX_TOKEN_PATTERN.fullmatch(token)): return 'index'
    return 'unknown'
