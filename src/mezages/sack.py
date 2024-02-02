from copy import deepcopy
from typing import Any, Optional
from mezages.paths import ensure_path, ROOT_PATH
from mezages.subjects import get_subject_substitute
from mezages.buckets import FormattedBucket, format_bucket
from mezages.states import State, ensure_state, FormattedState


class SackError(Exception):
    pass


class Sack:
    def __init__(self, init_state: Any = dict()) -> None:
        self.__state = ensure_state(init_state)

    @property
    def state(self) -> State:
        return deepcopy(self.__state)

    @property
    def all(self) -> FormattedBucket:
        return list(message for bucket in self.map.values() for message in bucket)

    @property
    def map(self) -> FormattedState:
        formatted_state: FormattedState = dict()

        for path, bucket in self.__state.items():
            subject_substitute = get_subject_substitute(path, self.__state)
            formatted_state[str(path)] = format_bucket(bucket, subject_substitute)

        return formatted_state

    def merge(self, state: State, mount_path: Optional[str] = None) -> None:
        state = ensure_state(state)
        if mount_path: ensure_path(mount_path)

        for path, bucket in state.items():
            new_path = path

            if mount_path:
                if path == ROOT_PATH:
                    new_path = mount_path
                else:
                    new_path = f'{mount_path}.{path}'

            previous_bucket = self.__state.get(new_path, set())
            self.__state[new_path] = previous_bucket.union(bucket)

    def mount(self, path: str) -> None:

        ensure_path(path)

        new_state = {}

        for old_path, bucket in self.__state.items():
            new_path = old_path

            if new_path == ROOT_PATH:
                new_path = path
            else:
                new_path = f'{path}.{old_path}'

            new_state[new_path] = bucket

        self.__state = new_state
