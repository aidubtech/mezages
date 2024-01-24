from mezages.path import Path
from mezages.token import Token
from typing import Literal, TYPE_CHECKING


if TYPE_CHECKING:
    # To prevent circular imports
    from mezages.store import Store


subject_placeholder = '{subject}'


SubjectType = Literal['any'] | Literal['unknown'] | Literal['array'] | Literal['record']

SubjectTypePair = tuple[SubjectType, SubjectType]


class Subject:
    @classmethod
    def get_type(cls, path: Path, store: 'Store') -> SubjectType:
        first_child_path = None

        try:
            first_child_path = next(
                store_path for store_path in store.keys() if (
                    not store_path.is_root
                    and (path.is_root or store_path.startswith(f'{path}.'))
                )
            )
        except StopIteration: pass

        if not first_child_path: return 'unknown'

        sub_path = first_child_path[len(f'{path}.'):]
        sub_first_token_type = Token.get_type(sub_path.split('.')[0])

        if sub_first_token_type == 'key': return 'record'
        if sub_first_token_type == 'index': return 'array'
        return 'unknown'

    @classmethod
    def get_type_pair(cls, path: Path, store: 'Store') -> SubjectTypePair:
        parent_path = '.'.join(path.split('.')[:-1])  # Empty string if not path parent
        parent_type = cls.get_type(Path(parent_path), store) if parent_path else 'unknown'

        self_type = cls.get_type(path, store)
        is_any_type = self_type == 'unknown' and parent_type != 'unknown'

        return ('any' if is_any_type else self_type, parent_type)

    @classmethod
    def get_substitute(cls, path: Path, store: 'Store') -> (str | None):
        if path.is_root: return None

        self_type = cls.get_type_pair(path, store)[0]
        if self_type == 'unknown': return None

        # Add better array subject substitute logic here
        # Add better record subject substitute logic here
        return path
