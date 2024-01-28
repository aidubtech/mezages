from typing import TYPE_CHECKING, Literal, Optional
from mezages.paths import ROOT_PATH, get_token_type, TokenType

if TYPE_CHECKING:
    from mezages.states import State


#----------------------------------------
# TYPE ALIASES
#----------------------------------------

SubjectType = Literal['scion'] | Literal['array'] | Literal['record']

SubjectLineageTypes = tuple[Optional[SubjectType], ...]


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


def get_subject_lineage_types(path: str, state: 'State') -> SubjectLineageTypes:
    subject_lineage_types: list[Optional[SubjectType]] = list()

    prev_path = None

    for token in path.split('.'):
        next_path = f'{prev_path}.{token}' if prev_path else token

        next_path_type: Optional[SubjectType] = None

        if any_child_path := get_subject_first_child_path(next_path, state):
            child_sub_path = any_child_path[len(f'{next_path}.'):]
            sub_path_first_token = child_sub_path.split('.')[0]
            sub_path_first_token_type = get_token_type(sub_path_first_token)

            next_path_type = (
                None if not sub_path_first_token_type
                else TOKEN_SUBJECT_TYPE_MAP.get(sub_path_first_token_type)
            )

        parent_type_is_known = (
            subject_lineage_types and (
                subject_lineage_types[-1] not in (None, 'scion')
            )
        )

        is_scion_type = not next_path_type and parent_type_is_known
        subject_lineage_types.append('scion' if is_scion_type else next_path_type)

        prev_path = next_path

    return tuple(subject_lineage_types)


def get_subject_substitute(path: str, state: 'State') -> Optional[str]:
    if path == ROOT_PATH: return None

    path_type = get_subject_lineage_types(path, state)[-1]
    if not path_type: return None

    # Add better array subject substitute logic here
    # Add better record subject substitute logic here
    return path
