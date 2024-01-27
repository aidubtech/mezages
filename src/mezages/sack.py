from typing import Any
from mezages.subject import Subject
from mezages.bucket import OutputMessages
from mezages.store import Store, OutputStore


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
