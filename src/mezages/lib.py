from re import compile
from typing import Any, Literal, Optional, TypedDict, NotRequired


# -------------------------------------
# TYPE ALIASES
# -------------------------------------

Kind = Literal['notice'] | Literal['warning'] | Literal['failure']


Message = TypedDict(
    'Message',
    {
        'ctx': str,
        'kind': Kind,
        'summary': str,
        'description': Optional[str],
    },
)


InputMessageStruct = TypedDict(
    'InputMessageStruct',
    {
        'kind': NotRequired[Optional[Kind]],
        'summary': str,
        'description': NotRequired[Optional[str]],
    },
)


InputMessage = str | InputMessageStruct

# -------------------------------------
# CONSTANTS
# -------------------------------------

GLOBAL_CONTEXT_PATH = 'global'

CONTEXT_KEY_REGEX = '(?:(?:[a-z0-9]+_)*[a-z0-9]+)'

CONTEXT_PATH_PATTERN = compile(fr'(?:{CONTEXT_KEY_REGEX}\.)*{CONTEXT_KEY_REGEX}')

# -------------------------------------
# EXCEPTIONS
# -------------------------------------


class ContextError(Exception):
    pass


# -------------------------------------
# FUNCTIONS
# -------------------------------------


def ensure_context_path(value: Any) -> str:
    if value is None or (
        isinstance(value, str) and CONTEXT_PATH_PATTERN.fullmatch(value)
    ):
        return value or GLOBAL_CONTEXT_PATH
    raise ContextError(f'Invalid context path: {repr(value)}')


def build_message(context_path: str, input_message: InputMessage) -> Message:
    if isinstance(input_message, str):
        input_message = {'summary': input_message}

    return Message(
        {
            'ctx': context_path,
            'kind': input_message.get('kind') or 'notice',
            'summary': input_message['summary'],
            'description': input_message.get('description'),
        }
    )
