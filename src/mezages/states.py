from typing import cast, Any
from mezages.paths import is_valid_path
from mezages.buckets import is_valid_bucket, Bucket, FormattedBucket


# ----------------------------------------
# Type Aliases
# ----------------------------------------

State = dict[str, Bucket]

FormattedState = dict[str, FormattedBucket]


# ----------------------------------------
# Exception Classes
# ----------------------------------------

class StateError(Exception):
    def __init__(self, message: str, **kwargs: Any):
        super().__init__(message)
        self.data = {**kwargs, message: message}


# ----------------------------------------
# Functions
# ----------------------------------------

def validate_state(argument: Any) -> set[str]:
    if not isinstance(argument, dict):
        return {'State must be a dict instance'}

    failures: set[str] = set()

    for path, bucket in cast(Any, argument.items()):
        path_is_valid = is_valid_path(path)
        bucket_is_valid = is_valid_bucket(bucket)

        if not path_is_valid and bucket_is_valid:
            failures.add(f'{repr(path)} is an invalid path')
        elif path_is_valid and not bucket_is_valid:
            failures.add(f'{repr(path)} is mapped to an invalid bucket')
        elif not path_is_valid and not bucket_is_valid:
            failures.add(f'{repr(path)} is an invalid path mapped to an invalid bucket')

    return failures


def is_valid_state(argument: Any) -> bool:
    return not validate_state(argument)


def ensure_state(argument: Any) -> State:
    if not (failures := validate_state(argument)):
        return dict((key, set(value)) for key, value in argument.items())

    message = '\n'.join([
        'Encountered some state issues\n',
        *[f'\t[!] {failure}' for failure in failures],
        '',
    ])

    # Pretty print the argument after message
    raise StateError(message, failures=failures)
