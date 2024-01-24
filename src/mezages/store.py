from typing import cast, Any
from mezages.path import Path
from mezages.bucket import Bucket, OutputMessages


OutputStore = dict[str, OutputMessages]


class StoreError(Exception):
    def __init__(self, message: str, **kwargs: Any):
        super().__init__(message)
        self.data = {**kwargs, message: message}


class Store(dict[Path, Bucket]):
    @classmethod
    def is_valid(cls, argument: Any) -> bool:
        return not cls.validate(argument)

    @classmethod
    def ensure(cls, argument: Any) -> dict[Path, Bucket]:
        if not (failures := cls.validate(argument)):
            return dict(
                (Path(key), Bucket(value))
                for key, value in argument.items()
            )

        message = '\n'.join([
            'Encountered some store issues\n',
            *[f'\t[!] {failure}' for failure in failures],
            '',
        ])

        # Pretty print the argument after message
        raise StoreError(message, failures=failures)

    @classmethod
    def validate(cls, argument: Any) -> set[str]:
        if not isinstance(argument, dict):
            return {'Store must be a dict instance'}

        failures: set[str] = set()

        for path, bucket in cast(Any, argument.items()):
            has_valid_path = Path.is_valid(path)
            has_valid_bucket = Bucket.is_valid(bucket)

            if not has_valid_path and has_valid_bucket:
                failures.add(f'{repr(path)} is an invalid path')
            elif has_valid_path and not has_valid_bucket:
                failures.add(f'{repr(path)} is mapped to an invalid bucket')
            elif not has_valid_path and not has_valid_bucket:
                failures.add(f'{repr(path)} is an invalid path mapped to an invalid bucket')

        return failures

    def __init__(self, initval: Any = dict()) -> None:
        super().__init__(self.ensure(initval))
