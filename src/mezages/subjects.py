from typing import TYPE_CHECKING, Literal, Optional
from mezages.paths import get_token_type, ROOT_PATH, TokenType

if TYPE_CHECKING:
    from mezages.states import State


#----------------------------------------
# TYPE ALIASES
#----------------------------------------

SubjectType = Literal['array'] | Literal['record']


#----------------------------------------
# CONSTANTS
#----------------------------------------

SUBJECT_PLACEHOLDER = '{subject}'

TOKEN_SUBJECT_TYPE_MAP: dict[TokenType, SubjectType] = {'key': 'record', 'index': 'array'}


#----------------------------------------
# REUSABLE PROCEDURES
#----------------------------------------

def get_subject_first_child_path(path: str, state: 'State') -> Optional[str]:
    try:
        return next(
            state_path for state_path in state.keys() if (
                state_path != ROOT_PATH and (
                    path == ROOT_PATH or state_path.startswith(f'{path}.')
                )
            )
        )
    except StopIteration: return None


def get_subject_type(path: str, state: 'State', child_path: Optional[str] = None):
    child_path_valid = child_path is not None and child_path != path and child_path in state
    child_path = child_path if child_path_valid else get_subject_first_child_path(path, state)

    if not child_path: return None

    child_sub_path = child_path[len(f'{path}.'):]
    sub_path_first_token = child_sub_path.split('.')[0]
    sub_path_first_token_type = get_token_type(sub_path_first_token)

    if not sub_path_first_token_type: return None
    return TOKEN_SUBJECT_TYPE_MAP[sub_path_first_token_type]


def get_subject_parent_type(path: str, state: 'State'):
    parent_path = '.'.join(path.split('.')[:-1])
    if not parent_path: return None
    return get_subject_type(parent_path, state, path)


def get_subject_substitute(path: str, state: 'State') -> Optional[str]:
    if path == ROOT_PATH: return None

    subject_type = get_subject_type(path, state)
    subject_parent_type = get_subject_parent_type(path, state)

    if not subject_type and not subject_parent_type:
        return None
    # Add better array subject substitute logic here
    if subject_type == 'array':
        parent_path = '.'.join(path.split('.')[:-1])
        if parent_path:
            if parent_path in state:
                index = int(path.split('.')[-1].split('[')[-1].rstrip(']'))
                if 0 <= index < len(state[parent_path]):
                    return f"Item at index {index} in {parent_path}"
                else:
                    return f"Item at index {index}"
    
    # Add better record subject substitute logic here
    return path


