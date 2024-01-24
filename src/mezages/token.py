from re import compile
from typing import Literal


TokenType = Literal['key'] | Literal['index'] | Literal['unknown']


class Token:
    TOKEN_REGEX = r'(?:[^\.]+)'
    TOKEN_PATTERN = compile(TOKEN_REGEX)

    KEY_TOKEN_REGEX = r'(?:\{[a-z0-9_]+\})'
    KEY_TOKEN_PATTERN = compile(KEY_TOKEN_REGEX)

    INDEX_TOKEN_REGEX = r'(?:\[\d+\])'
    INDEX_TOKEN_PATTERN = compile(INDEX_TOKEN_REGEX)

    @classmethod
    def get_type(cls, token: str) -> TokenType:
        if bool(cls.KEY_TOKEN_PATTERN.fullmatch(token)): return 'key'
        if bool(cls.INDEX_TOKEN_PATTERN.fullmatch(token)): return 'index'
        return 'unknown'
