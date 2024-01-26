from typing import Any, Optional
from mezages.subject import subject_placeholder


Messages = set[str]

OutputMessages = list[str]


class BucketError(Exception):
    pass


class Bucket(Messages):
    @classmethod
    def is_valid(cls, argument: Any) -> bool:
        return type(argument) in (set, list, tuple) and not any(
            not isinstance(message, str) for message in argument
        )

    @classmethod
    def ensure(cls, argument: Any) -> Messages:
        if cls.is_valid(argument): return set(argument)
        # Find a way to pretty print the structure in error
        raise BucketError(f'{repr(argument)} is an invalid bucket')

    def __init__(self, initval: Any = set()):
        super().__init__(self.ensure(initval))

    def format(self, subject_substitute: Optional[str]) -> OutputMessages:
        formatted_messages: Messages = set()

        for message in self:
            if message.startswith(subject_placeholder):
                message = message.replace(subject_placeholder, subject_substitute or str(), 1).strip()
                # [NOTE] Edge case is when it is undesired for us to uppercase the first character
                if subject_substitute is None: message = f'{message[0].upper()}{message[1:]}'

            formatted_messages.add(message)

        return list(formatted_messages)
