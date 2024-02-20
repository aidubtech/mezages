from re import compile
from typing import Any, Literal, Optional, TypedDict, NotRequired


# -------------------------------------
# TYPE ALIASES
# -------------------------------------

MessageType = Literal['notice'] | Literal['error'] | Literal['warning']


Message = TypedDict(
    'Message',
    {
        'ctx': str,
        'type': MessageType,
        'summary': str,
        'description': Optional[str],
    },
)


StructInputMessage = TypedDict(
    'StructInputMessage',
    {
        'type': NotRequired[Optional[MessageType]],
        'summary': str,
        'description': NotRequired[Optional[str]],
    },
)


InputMessage = str | StructInputMessage

# -------------------------------------
# CONSTANTS
# -------------------------------------

DEFAULT_CONTEXT_PATH = 'global'

DEFAULT_MESSAGE_TYPE: MessageType = 'notice'

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
        return value or DEFAULT_CONTEXT_PATH
    raise ContextError(f'Invalid context path: {repr(value)}')


def build_message(context_path: str, input_message: InputMessage) -> Message:
    if isinstance(input_message, str):
        input_message = {'summary': input_message}

    return Message(
        {
            'ctx': context_path,
            'type': input_message.get('type') or DEFAULT_MESSAGE_TYPE,
            'summary': input_message['summary'],
            'description': input_message.get('description'),
        }
    )
