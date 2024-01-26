from typing import Any, Optional
from mezages.path import Path
from mezages.subject import Subject
from mezages.store import Store, OutputStore
from mezages.bucket import Bucket, OutputMessages


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

        return output_store

    def union(self, store: dict[str, set[str]], mount_path: Optional[str] = None) -> None:
        # validate arguments
        Store.ensure(store)
        if mount_path is not None:
            Path.ensure(mount_path)

        # if the mount_path exist, arrange the path accordingly
        adjusted_store = {
            Path(f'{mount_path}.{path}') if mount_path else Path(path): Bucket(bucket)
            for path, bucket in store.items()
        }

        for path, bucket in adjusted_store.items():
            if path in self.__store:
                # unify the bucket if path already exist
                self.__store[path].union(bucket)
            else:
                # copy path and bucket into the instance
                self.__store[path] = bucket
