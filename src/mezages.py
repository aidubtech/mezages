import re
from typing import cast, Any


base_path = '{base}'
subject_placeholder = '{subject}'

MezagesStore = dict[str, set[str]]
MezagesOutputStore = dict[str, list[str]]
MezagesInputStore = dict[str, (set[str] | list[str] | tuple[str, ...])]


class MezagesError(Exception):
    pass


class Mezages:
    KEY_REGEX = '[a-z0-9_]+'
    INDEX_REGEX = r'(?:\[\d+\])'
    TOKEN_REGEX = f'(?:{INDEX_REGEX}|{KEY_REGEX})'
    PATH_REGEX = fr'(?:(?:{TOKEN_REGEX}\.)*{TOKEN_REGEX})'

    def __init__(self, store: Any = dict()) -> None:
        self.__store = self.__ensure_store(store)

    @property
    def all(self) -> list[str]:
        return [message for bucket in self.map.values() for message in bucket]

    @property
    def map(self) -> MezagesOutputStore:
        return {path: list(self.__format_messages(path, bucket)) for path, bucket in self.__store.items()}

    def __is_path(self, path: Any) -> bool:
        return path == base_path or (isinstance(path, str) and bool(re.fullmatch(self.PATH_REGEX, path)))

    def __get_subject_substitute(self, path: str) -> str:
        return path  # Add other subject substitute logic here

    def __format_messages(self, path: str, messages: set[str]) -> set[str]:
        formatted_messages: set[str] = set()

        subject_substitute = (
            str() if path == base_path
            else self.__get_subject_substitute(path)
        )

        for message in messages:
            if message.startswith(subject_placeholder):
                message = message.replace(subject_placeholder, subject_substitute, 1).strip()
                # [NOTE] An edge case is if developers do not want us to touch the message
                if subject_substitute == str(): message = f'{message[0].upper()}{message[1:]}'

            formatted_messages.add(message)

        return formatted_messages

    def __ensure_store(self, store: Any) -> MezagesStore:
        if not isinstance(store, dict):
            raise MezagesError('Store must be a mapping of path to a bucket of messages')

        failures: set[str] = set()
        new_store: MezagesStore = dict()

        for path, bucket in cast(dict[Any, Any], store).items():
            has_valid_path = self.__is_path(path)
            has_valid_bucket = type(bucket) in (set, list, tuple)

            has_valid_messages = has_valid_bucket and not any(
                not isinstance(message, str) for message in bucket
            )

            if has_valid_path and has_valid_messages:
                new_store[path] = set(bucket)
                continue

            if not has_valid_path and has_valid_messages:
                failures.add(f'{repr(path)} is not a valid path')
            elif has_valid_path and not has_valid_bucket:
                failures.add(f'{repr(path)} is not mapped to a valid bucket of messages')
            elif has_valid_path and not has_valid_messages:
                failures.add(f'{repr(path)} has one or more invalid messages in its bucket')
            elif not has_valid_path and not has_valid_bucket:
                failures.add(f'{repr(path)} is not a valid path, and is not mapped to a valid bucket of messages')
            elif not has_valid_path and not has_valid_messages:
                failures.add(f'{repr(path)} is not a valid path, and has one or more invalid messages in its bucket')

        if not failures: return new_store

        raise MezagesError('\n'.join([
            'Encountered some store issues\n', *[f'\t[!] {failure}' for failure in failures], '',
        ]))

    def union(self, store: MezagesInputStore, mount_path: str | None = None) -> None:
        # validate arguments
        self.__ensure_store(store)
        self.__is_path(mount_path)

        # if the mount_path exist, arrange the path accordingly
        adjusted_store = {f"{mount_path}.{path}" if mount_path else path: sack for path, sack in store.items()}

        # iterate through the adjusted store, and unify with the existing paths instance
        for path, sack in adjusted_store.items():
            if path in self.__store:
                # unify the sack if path already exist
                self.__store[path] = self.__store[path].union(sack)
            else:
                # copy path and sack into the instance
                self.__store[path] = set(sack)
