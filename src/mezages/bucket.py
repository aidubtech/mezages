from typing import cast, Any
from mezages.path import Path


subject_placeholder = '{subject}'


class BucketError(Exception):
    pass


class Bucket:
    @classmethod
    def valid(cls, bucket: Any) -> bool:
        return type(bucket) in (set, list, tuple) and not any(
            not isinstance(message, str) for message in cast(set[str], bucket)
        )

    def __init__(self, value: Any = set()):
        self.__value = self.__ensure_bucket(value)

    @property
    def value(self) -> set[str]:
        return self.__value

    @property
    def has_partial_messages(self) -> bool:
        return any(message.startswith(subject_placeholder) for message in self.__value)

    def format_messages(self, path: Path = Path()) -> set[str]:
        formatted_messages: set[str] = set()

        for message in self.__value:
            if message.startswith(subject_placeholder):
                message = message.replace(subject_placeholder, path.substitute, 1).strip()
                # Uppercase the first character if the subject was an empty string
                # [NOTE] An edge case is if caller do not want us to touch the message
                if path.substitute == str(): message = f'{message[0].upper()}{message[1:]}'

            formatted_messages.add(message)

        return formatted_messages

    def __ensure_bucket(self, value: Any) -> set[str]:
        if self.__class__.valid(value): return set(value)
        raise BucketError(f'{repr(value)} is an invalid bucket')
