import re
import copy
from typing import cast, Any


MezagesStore = dict[str, set[str]]

MezagesInputStore = dict[str, (set[str] | list[str] | tuple[str])]


class MezagesError(Exception):
    pass


class Mezages:
    KEY_REGEX = r'(?:(?:\d+)|(?:[a-z][a-z0-9_]+[a-z0-9]))'
    PATH_PATTERN = re.compile(fr'(?:(?:{KEY_REGEX}\.)*{KEY_REGEX})')

    def __init__(self, store: Any = dict()) -> None:
        self.__store = self.__ensure_store(store)

    @property
    def store(self) -> MezagesStore:
        return copy.deepcopy(self.__store)

    def export(self, only: list[str] = list(), omit: list[str] = list()) -> MezagesStore:
        return dict(item for item in self.__store.items() if (
            (not only or item[0] in only) and (not omit or item[0] not in omit)
        ))

    def __is_key(self, key: Any) -> bool:
        return isinstance(key, str) and bool(self.PATH_PATTERN.match(key))

    def __ensure_store(self, store: Any) -> MezagesStore:
        if not isinstance(store, dict):
            raise MezagesError('Store must be a valid mapping of paths to messages')

        failures: set[str] = set()
        new_store: MezagesStore = dict()

        for path, bucket in cast(dict[Any, Any], store).items():
            has_valid_path = self.__is_key(path)

            has_valid_bucket = (
                type(bucket) in (set, list, tuple) and bucket
                and not any(not isinstance(message, str) for message in bucket)
            )

            if has_valid_path and has_valid_bucket:
                new_store[path] = set(bucket)
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
