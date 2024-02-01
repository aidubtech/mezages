from re import compile
from collections.abc import Generator
from typing import TYPE_CHECKING, Any, Literal, Optional

if TYPE_CHECKING:
    from mezages.sacks import SackState


#----------------------------------------
# TYPE ALIASES
#----------------------------------------

TokenType = Literal['key'] | Literal['index']

SubjectType = Literal['array'] | Literal['record']


#----------------------------------------
# CONSTANTS
#----------------------------------------

ROOT_PATH = '%root%'
SUBJECT_PLACEHOLDER = '{subject}'

KEY_TOKEN_REGEX = r'(?:\{[a-z0-9_]+\})'
KEY_TOKEN_PATTERN = compile(KEY_TOKEN_REGEX)

INDEX_TOKEN_REGEX = r'(?:\[\d+\])'
INDEX_TOKEN_PATTERN = compile(INDEX_TOKEN_REGEX)

KNOWN_TOKEN_REGEX = f'(?:{KEY_TOKEN_REGEX}|{INDEX_TOKEN_REGEX})'
UNKNOWN_TOKEN_REGEX = '(?:[a-z0-9_]+)'

TOKEN_REGEX = f'(?:{KNOWN_TOKEN_REGEX}|{UNKNOWN_TOKEN_REGEX})'
PATH_PATTERN = compile(fr'(?:(?:{TOKEN_REGEX}\.)*{TOKEN_REGEX})')

INVALID_TOKEN_ORDER_REGEX = fr'(?:{KNOWN_TOKEN_REGEX}\.{UNKNOWN_TOKEN_REGEX})'
INVALID_TOKEN_ORDER_PATTERN = compile(INVALID_TOKEN_ORDER_REGEX)

TOKEN_SUBJECT_TYPE_MAP: dict[TokenType, SubjectType] = {'key': 'record', 'index': 'array'}


#----------------------------------------
# EXCEPTION CLASSES
#----------------------------------------

class PathError(Exception):
    pass


#----------------------------------------
# MODULE FUNCTIONS
#----------------------------------------

def is_path(argument: Any) -> bool:
    return argument == ROOT_PATH or (
        isinstance(argument, str)
        and bool(PATH_PATTERN.fullmatch(argument))
        and not bool(INVALID_TOKEN_ORDER_PATTERN.search(argument))
    )


def ensure_path(argument: Any) -> str:
    if is_path(argument): return str(argument)
    raise PathError(f'{repr(argument)} is an invalid path')


def get_token_type(token: str) -> Optional[TokenType]:
    if bool(KEY_TOKEN_PATTERN.fullmatch(token)): return 'key'
    if bool(INDEX_TOKEN_PATTERN.fullmatch(token)): return 'index'


def gen_path_children(path: str, sack_state: 'SackState') -> Generator[str, None, None]:
    for state_path in sack_state.keys():
        if state_path != ROOT_PATH and (path == ROOT_PATH or state_path.startswith(f'{path}.')):
            yield state_path


def get_path_first_child(path: str, sack_state: 'SackState') -> Optional[str]:
    try: return next(gen_path_children(path, sack_state))
    except StopIteration: return None


def get_subject_type(
    path: str, sack_state: 'SackState', child_path: Optional[str] = None
) -> Optional[SubjectType]:
    is_valid_child_path = path != child_path and child_path in sack_state
    child_path = child_path if is_valid_child_path else get_path_first_child(path, sack_state)

    if not child_path: return None

    child_sub_path = child_path[len(f'{path}.'):]
    sub_path_first_token = child_sub_path.split('.')[0]
    sub_path_first_token_type = get_token_type(sub_path_first_token)

    if not sub_path_first_token_type: return None
    return TOKEN_SUBJECT_TYPE_MAP[sub_path_first_token_type]


def get_subject_parent_type(path: str, sack_state: 'SackState') -> Optional[SubjectType]:
    parent_path = '.'.join(path.split('.')[:-1])
    if not parent_path: return None
    return get_subject_type(parent_path, sack_state, path)


def get_subject_substitute(path: str, sack_state: 'SackState') -> Optional[str]:
    if path == ROOT_PATH: return None

    subject_type = get_subject_type(path, sack_state)
    subject_parent_type = get_subject_parent_type(path, sack_state)

    if not subject_type and not subject_parent_type:
        return None

    if subject_parent_type == 'record':
        tokens = path.split('.')
        parent_path = '.'.join(tokens[:-1])
        prop = tokens[-1].strip('{}')

        return f'{prop} in {parent_path}' if parent_path else prop

    return path
