import re
from typing import Any, Literal


# ----------------------------------------
# Constants
# ----------------------------------------

TOKEN_REGEX = r'(?:[^\.]+)'

KEY_TOKEN_REGEX = r'(?:\{[a-z0-9_]+\})'
KEY_TOKEN_PATTERN = re.compile(KEY_TOKEN_REGEX)

INDEX_TOKEN_REGEX = r'(?:\[\d+\])'
INDEX_TOKEN_PATTERN = re.compile(INDEX_TOKEN_REGEX)

PATH_PATTERN = re.compile(fr'(?:(?:{TOKEN_REGEX}\.)*{TOKEN_REGEX})')


# ----------------------------------------
# Variables
# ----------------------------------------

root_path = '%root%'


# ----------------------------------------
# Type Aliases
# ----------------------------------------

TokenType = Literal['key'] | Literal['index'] | Literal['unknown']


# ----------------------------------------
# Exception Classes
# ----------------------------------------

class PathError(Exception):
    pass


# ----------------------------------------
# Functions
# ----------------------------------------

def is_valid_path(argument: Any) -> bool:
    return argument == root_path or (
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
