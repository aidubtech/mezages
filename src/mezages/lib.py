from re import compile
from typing import Any, Literal, Optional, TypedDict, NotRequired


# ----------------------------------------
# TYPE ALIASES
# ----------------------------------------

MessageType = Literal['notice'] | Literal['warning'] | Literal['failure']

Message = TypedDict(
    'Message',
    {
        'ctx': str,
        'type': MessageType,
        'summary': str,
        'description': Optional[str],
    },
)

PartialMessageDict = TypedDict(
    'PartialMessageDict',
    {
        'type': NotRequired[Optional[MessageType]],
        'summary': str,
        'description': NotRequired[Optional[str]],
    },
)

PartialMessage = str | PartialMessageDict

SackStore = dict[str, dict[MessageType, list[Message]]]

# ----------------------------------------
# CONSTANTS
# ----------------------------------------

DEFAULT_CONTEXT_ID: str = 'global'

DEFAULT_MESSAGE_TYPE: MessageType = 'notice'

CONTEXT_ID_PATTERN = compile(r'(?:(?:[a-z0-9_])+)')

# ----------------------------------------
# EXCEPTIONS
# ----------------------------------------


class ContextError(Exception):
    pass


# ----------------------------------------
# FUNCTIONS
# ----------------------------------------


def is_context_id(argument: Any) -> bool:
    return bool(CONTEXT_ID_PATTERN.fullmatch(str(argument)))


def ensure_context_id(argument: Any) -> str:
    if is_context_id(argument):
        return str(argument)

    failure = 'Context id provided is invalid'
    raise ContextError(f'{failure}: {repr(argument)}')


def build_message(context_id: str, partial_message: PartialMessage) -> Message:
    if isinstance(partial_message, str):
        partial_message = {'summary': partial_message}

    return Message(
        {
            'ctx': context_id,
            'type': partial_message.get('type') or DEFAULT_MESSAGE_TYPE,
            'summary': partial_message['summary'],
            'description': partial_message.get('description'),
        }
    )
