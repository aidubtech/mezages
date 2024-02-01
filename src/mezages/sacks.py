from typing import cast, Any, Optional
from mezages.buckets import Bucket, FormattedBucket, is_bucket, format_bucket
from mezages.paths import ROOT_PATH, is_path, ensure_path, get_subject_substitute


#----------------------------------------
# TYPE ALIASES
#----------------------------------------

SackState = dict[str, Bucket]

FormattedSackState = dict[str, FormattedBucket]


#----------------------------------------
# EXCEPTION CLASSES
#----------------------------------------

class SackError(Exception):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message)
        self.data = {**kwargs, message: message}


#----------------------------------------
# MODULE FUNCTIONS
#----------------------------------------

def validate_sack_state(argument: Any) -> set[str]:
    if not isinstance(argument, dict):
        return {'Argument must be a dict instance'}

    failures: set[str] = set()

    for path, bucket in cast(Any, argument.items()):
        is_valid_path = is_path(path)
        is_valid_bucket = is_bucket(bucket)

        if not is_valid_path and is_valid_bucket:
            failures.add(f'{repr(path)} is an invalid path')
        elif is_valid_path and not is_valid_bucket:
            failures.add(f'{repr(path)} is mapped to an invalid bucket')
        elif not is_valid_path and not is_valid_bucket:
            failures.add(f'{repr(path)} is an invalid path mapped to an invalid bucket')

    return failures


def ensure_sack_state(argument: Any) -> SackState:
    if not (failures := validate_sack_state(argument)):
        return {key: set(value) for key, value in argument.items()}

    message = '\n'.join([
        'Encountered some sack state errors\n',
        *[f'\t[!] {failure}' for failure in failures],
        '',
    ])

    raise SackError(message, failures=failures)


#----------------------------------------
# SACK CLASS DEFINITION
#----------------------------------------

class Sack:
    def __init__(self, init_state: Any = dict()) -> None:
        self.__state = ensure_sack_state(init_state)

    @property
    def all(self) -> FormattedBucket:
        return [message for bucket in self.map.values() for message in bucket]

    @property
    def map(self) -> FormattedSackState:
        formatted_state: FormattedSackState = dict()

        for path, bucket in self.__state.items():
            subject_substitute = get_subject_substitute(path, self.__state)
            formatted_state[str(path)] = format_bucket(bucket, subject_substitute)

        return formatted_state

    def merge(self, other: 'Sack', mount_path: Optional[str] = None) -> None:
        if not isinstance(other, Sack):
            raise SackError('Other must be a sack instance')

        if mount_path is not None: ensure_path(mount_path)

        for path, bucket in getattr(other, '_Sack__state').items():
            new_path = path if not mount_path else (
                mount_path if path == ROOT_PATH else f'{mount_path}.{path}'
            )

            self.__state[new_path] = self.__state.get(new_path, set()).union(bucket)
