from typing import Any
from mezages.subject import Subject
from mezages.bucket import Bucket, OutputMessages
from mezages.store import Store, OutputStore
from mezages.path import Path


class SackError(Exception):
    pass


class Sack:
    def __init__(self, init_store: Any = dict()) -> None:
        self.__store = Store(init_store)

    @property
    def all(self) -> OutputMessages:
        return list(message for messages in self.map.values() for message in messages)

    @property
    def map(self) -> OutputStore:
        output_store: OutputStore = dict()

        for path, bucket in self.__store.items():
            subject_substitute = Subject.get_substitute(path, self.__store)
            output_store[path] = bucket.format(subject_substitute)

        return output_store
    
    def merge(self, other: 'Sack', mount_path: str | None) -> None:
        if not isinstance(other, Sack):
            raise ValueError("Argument 'other' must be an instance of Sack.")
        
        if mount_path is not None and not Path.is_valid(mount_path):
            raise ValueError("Argument 'mount_path' must be None or a valid path string.")

        for other_path, other_bucket in other.__store.items():
            merged_path = Path(mount_path + '.' + other_path) if mount_path else Path(other_path)

            if merged_path in self.__store:
                self.__store[merged_path] = Bucket(self.__store[merged_path].union(other_bucket))
            else:
                self.__store[merged_path] = other_bucket
