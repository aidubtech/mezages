import re
from typing import cast, Any


base_path = '{base}'
subject_placeholder = '{subject}'

MezagesStore = dict[str, Any]
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
    
    # .....merge method begins......
    
    def merge(self, other: 'Mezages', mount_path: str | None) -> None:
        # Validate arguments
        if not isinstance(other, Mezages):
            raise MezagesError('other must be an instance of Mezages')
        if mount_path is not None and not self.__is_path(mount_path):
            raise MezagesError('Mount path must be None or a valid path string')

        # function to merge buckets
        def merge_buckets(existing_bucket: set[str], new_bucket: list[str]) -> set[str]:
            return existing_bucket.union(set(new_bucket))

        # function to merge paths
        def merge_paths(existing_path: str, new_path: str, mount_point: str | None = None) -> str:
            if mount_point is not None:
                return f'{mount_point}.{new_path}'
            return existing_path

        # Merge paths and buckets
        for other_path, other_bucket in other.map.items():
            merged_path = merge_paths(self.__get_subject_substitute(other_path), other_path, mount_path)
            if merged_path in self.__store:
                # Path exists, merge buckets
                self.__store[merged_path] = merge_buckets(self.__store[merged_path], other_bucket)
            else:
                # Path doesn't exist, create new entry
                self.__store[merged_path] = other_bucket

    # .....merge method ends......

