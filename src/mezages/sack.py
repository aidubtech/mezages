from typing import Any, Optional
from mezages.paths import ensure_path
from mezages.subjects import get_subject_substitute
from mezages.states import ensure_state, FormattedState
from mezages.buckets import FormattedBucket, format_bucket


class SackError(Exception):
    pass


class Sack:
    def __init__(self, init_state: Any = dict()) -> None:
        self.__state = ensure_state(init_state)

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

    def union(self, store: Any, mount_path: Optional[str] = None) -> None:
        store = ensure_state(store)
        if mount_path: ensure_path(mount_path)

        if not store: return None

        for path, bucket in store.items():
            new_path = f'{mount_path}.{path}' if mount_path else path

            previous_bucket = self.__state.get(new_path, set())
            self.__state[new_path] = previous_bucket.union(bucket)
