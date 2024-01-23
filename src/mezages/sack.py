from typing import cast, Any
from mezages.path import Path
from mezages.bucket import Bucket


subject_placeholder = '{subject}'

SackStore = dict[Path, Bucket]
SackOutputStore = dict[str, list[str]]
SackInputStore = dict[str, (set[str] | list[str] | tuple[str, ...])]


class SackError(Exception):
    def __init__(self, message: str, **kwargs: Any):
        super().__init__(message)
        self.data = {**kwargs, message: message}


class Sack:
    def __init__(self, store: Any = dict()) -> None:
        self.__store = self.__ensure_store(store)

    @property
    def store(self) -> SackStore:
        return self.__store

    @property
    def all(self) -> list[str]:
        return list(message for messages in self.map.values() for message in messages)

    @property
    def map(self) -> SackOutputStore:
        return dict((path.value, list(bucket.format_messages(path))) for path, bucket in self.__store.items())

    def __ensure_store(self, store: Any) -> SackStore:
        if not isinstance(store, dict):
            raise SackError('Store must be a dictionary object')

        failures: set[str] = set()
        new_store: SackStore = dict()

        for path, bucket in cast(dict[Any, Any], store).items():
            has_valid_path = Path.valid(path)
            has_valid_bucket = type(bucket) in (set, list, tuple) and bucket

            has_valid_messages = has_valid_bucket and not any(
                not isinstance(message, str) for message in bucket
            )

            if has_valid_path and has_valid_messages:
                # Cast values into the required data types
                new_store[Path(path)] = Bucket(bucket)
                continue

            # Build well formatted failure messages
            if not has_valid_path and has_valid_messages:
                failures.add(f'{repr(path)} is not a valid path')
            elif has_valid_path and not has_valid_bucket:
                failures.add(f'{repr(path)} is not mapped to a valid bucket')
            elif has_valid_path and not has_valid_messages:
                failures.add(f'{repr(path)} has one or more invalid messages in its bucket')
            elif not has_valid_path and not has_valid_bucket:
                failures.add(f'{repr(path)} is not a valid path, and is not mapped to a valid bucket')
            elif not has_valid_path and not has_valid_messages:
                failures.add(f'{repr(path)} is not a valid path, and has one or more invalid messages in its bucket')

        if failures:
            message = '\n'.join([
                'Encountered some store issues\n',
                *[f'\t[!] {failure}' for failure in failures],
                '',
            ])
            raise SackError(message, failures=failures)

        return new_store
