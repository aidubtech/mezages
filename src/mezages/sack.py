from copy import deepcopy
from itertools import chain
from typing import Optional, Sequence

from mezages.lib import (
    Message,
    InputMessage,
    build_message,
    ensure_context_path,
    GLOBAL_CONTEXT_PATH,
)


SackStore = dict[str, dict[str, list[Message]]]


class Sack:
    def __init__(self) -> None:
        self.__store: SackStore = dict()

    @property
    def store(self) -> SackStore:
        return deepcopy(self.__store)

    @property
    def flat(self) -> list[Message]:
        return list(
            chain.from_iterable(
                [
                    bucket
                    for context_store in self.store.values()
                    for bucket in context_store.values()
                ]
            )
        )

    def mount(self, mount_context_path: str) -> None:
        mount_context_path = ensure_context_path(mount_context_path)

        if mount_context_path == GLOBAL_CONTEXT_PATH:
            return None

        new_store: SackStore = dict()

        for context_path, context_store in self.__store.items():
            new_context_path = (
                mount_context_path
                if context_path == GLOBAL_CONTEXT_PATH
                else f'{mount_context_path}.{context_path}'
            )

            # [NOTE] Set messages context by reference
            for message in chain(*context_store.values()):
                message.update(ctx=new_context_path)

            new_store[new_context_path] = context_store

        self.__store = new_store

    def add_messages(
        self,
        input_messages: Sequence[InputMessage],
        context_path: Optional[str] = None,
    ) -> None:
        context_path = ensure_context_path(context_path)

        for input_message in input_messages:
            message = build_message(context_path, input_message)

            self.__store.setdefault(context_path, dict())
            self.__store[context_path].setdefault(message['kind'], list())
            self.__store[context_path][message['kind']].append(message)

    def merge(self, other: 'Sack', mount_context_path: Optional[str] = None) -> None:

        mount_context_path = ensure_context_path(mount_context_path)

        for context_path, context_store in other.store.items():
            merged_context_path = (
                f'{mount_context_path}.{context_path}'
                if context_path
                else mount_context_path
            )

            self.__store.setdefault(merged_context_path, dict())

            for kind, messages in context_store.items():
                self.__store[merged_context_path].setdefault(kind, list())
                self.__store[merged_context_path][kind].extend(messages)
