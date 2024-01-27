from typing import TYPE_CHECKING, Literal, Optional
from mezages.paths import ROOT_PATH, get_token_type

if TYPE_CHECKING:
    from mezages.states import State


#----------------------------------------
# TYPE ALIASES
#----------------------------------------

SubjectType = Literal['any'] | Literal['unknown'] | Literal['array'] | Literal['record']

SubjectTypePair = tuple[SubjectType, SubjectType]


#----------------------------------------
# CONSTANTS
#----------------------------------------

SUBJECT_PLACEHOLDER = '{subject}'


#----------------------------------------
# REUSABLE PROCEDURES
#----------------------------------------

def get_subject_type(path: str, state: 'State') -> SubjectType:
    child_path = None

    try:
        child_path = next(
            state_path for state_path in state.keys() if (
                state_path != ROOT_PATH and (
                    path == ROOT_PATH or state_path.startswith(f'{path}.')
                )
            )
        )
    except StopIteration: pass

    if not child_path: return 'unknown'

    sub_child_path = child_path[len(f'{path}.'):]
    sub_first_token = sub_child_path.split('.')[0]
    sub_first_token_type = get_token_type(sub_first_token)

    if sub_first_token_type == 'key': return 'record'
    if sub_first_token_type == 'index': return 'array'
    return 'unknown'


def get_subject_type_pair(path: str, state: 'State') -> SubjectTypePair:
    parent_path = '.'.join(path.split('.')[:-1])

    # Set to unknown when there is not parent
    parent_type = (
        get_subject_type(parent_path, state)
        if parent_path else 'unknown'
    )

    self_type = get_subject_type(path, state)
    is_any_type = self_type == 'unknown' and parent_type != 'unknown'

    return ('any' if is_any_type else self_type, parent_type)


def get_subject_substitute(path: str, state: 'State') -> Optional[str]:
    if path == ROOT_PATH: return None

    self_type = get_subject_type_pair(path, state)[0]
    if self_type == 'unknown': return None

    # Add better array subject substitute logic here
    # Add better record subject substitute logic here
    return path
