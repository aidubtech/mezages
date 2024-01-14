import re
import copy
from typing import cast, Any


base_path = 'base'

entity_placeholder = '{entity}'


MezagesStore = dict[str, list[str]]

MezagesInputStore = dict[str, (set[str] | list[str] | tuple[str])]


class MezagesError(Exception):
    pass


class Mezages:
    KEY_REGEX = r'(?:(?:\d+)|(?:[a-z](?:(?:[a-z0-9]*_)*[a-z0-9]+)*))'
    PATH_REGEX = fr'(?:(?:{KEY_REGEX}\.)*{KEY_REGEX})'

    def __init__(self, store: Any = dict()) -> None:
        self.__store = self.__ensure_store(store)

    @property
    def store(self) -> MezagesStore:
        return copy.deepcopy(self.__store)

    def export(self, only: list[str] = list(), omit: list[str] = list()) -> MezagesStore:
        result: MezagesStore = dict()

        for path, bucket in self.__store.items():
            if (not only or path in only) and (not omit or path not in omit):
                result[path] = self.__resolve_messages(path, bucket)

        return result

    def __is_path(self, key: Any) -> bool:
        return isinstance(key, str) and bool(re.fullmatch(self.PATH_REGEX, key))

    def __get_entity_placeholder_value(self, path: str) -> str:
        # Use value from configuration before defaulting to the path string
        return ('' if path == base_path else path).strip()

    def __resolve_messages(self, path: str, messages: list[str]) -> list[str]:
        entity_placeholder_value = self.__get_entity_placeholder_value(path)

        resolved_messages: list[str] = list()

        for message in messages:
            if message.startswith(entity_placeholder):
                # How do we handle capitalizing the first letter and handle edge cases too?
                # We can set placeholder value for a path to an empty string to behave like base
                message = message.replace(entity_placeholder, entity_placeholder_value, 1).strip()
            resolved_messages.append(message)

        return resolved_messages

    def __ensure_store(self, store: Any) -> MezagesStore:
        if not isinstance(store, dict):
            raise MezagesError('Store must be a mapping of path to messages')

        failures: set[str] = set()
        new_store: MezagesStore = dict()

        for path, bucket in cast(dict[Any, Any], store).items():
            has_valid_path = self.__is_path(path)

            has_valid_bucket = (
                type(bucket) in (set, list, tuple) and bucket
                and not any(not isinstance(message, str) for message in bucket)
            )

            if has_valid_path and has_valid_bucket:
                new_store[path] = list(set(bucket))
                continue

            if not has_valid_path and has_valid_bucket:
                failures.add(f'{repr(path)} is an invalid path string')
            elif has_valid_path and not has_valid_bucket:
                failures.add(f'Path {repr(path)} has an invalid bucket of messages')
            elif not has_valid_path and not has_valid_bucket:
                failures.add(f'{repr(path)} is an invalid path with an invalid bucket of messages')                

        if not failures: return new_store

        raise MezagesError(
            '\n'.join([
                'Encountered some store validation failures\n',
                *[f'\t[!] {failure}' for failure in failures],
                '',
            ])
        )
