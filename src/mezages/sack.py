from typing import Self
from copy import deepcopy

from mezages.lib import (
    Message,
    SackStore,
    build_message,
    PartialMessage,
    ensure_context_id,
    DEFAULT_CONTEXT_ID,
)


class Sack:
    def __init__(self) -> None:
        self.__store: SackStore = dict()

    @property
    def flat(self) -> list[Message]:
        return [
            message
            for types_dict in self.store.values()
            for bucket in types_dict.values()
            for message in bucket
        ]

    @property
    def store(self) -> SackStore:
        return deepcopy(self.__store)

    def mount(self, mount_context_id: str) -> None:
        mount_context_id = ensure_context_id(mount_context_id)

        if mount_context_id == DEFAULT_CONTEXT_ID:
            return None

        new_store: SackStore = dict()

        for context_id, types_dict in self.__store.items():
            new_context_id = (
                mount_context_id
                if context_id == DEFAULT_CONTEXT_ID
                else f'{mount_context_id}.{context_id}'
            )
            new_store[new_context_id] = {
                message_type: [{**message, 'ctx': new_context_id} for message in bucket]
                for message_type, bucket in types_dict.items()
            }

        self.__store = new_store

    def merge(self, other: Self, mount_context_id: str = DEFAULT_CONTEXT_ID) -> None:
        pass

    def add(self, partial_message: PartialMessage, context_id: str = DEFAULT_CONTEXT_ID) -> None:
        return self.add_many(partial_messages=[partial_message], context_id=context_id)

    def add_many(
        self, partial_messages: list[PartialMessage], context_id: str = DEFAULT_CONTEXT_ID
    ) -> None:
        context_id = ensure_context_id(context_id)

        for partial_message in partial_messages:
            message = build_message(context_id, partial_message)

            self.__store.setdefault(context_id, dict())
            self.__store[context_id].setdefault(message['type'], list())
            self.__store[context_id][message['type']].append(message)
