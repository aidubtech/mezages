from typing import Any, Optional
from mezages.paths import SUBJECT_PLACEHOLDER


#----------------------------------------
# TYPE ALIASES
#----------------------------------------

Bucket = set[str]

FormattedBucket = list[str]


#----------------------------------------
# EXCEPTION CLASSES
#----------------------------------------

class BucketError(Exception):
    pass


#----------------------------------------
# MODULE FUNCTIONS
#----------------------------------------

def is_bucket(argument: Any) -> bool:
    return type(argument) in (set, list, tuple) and argument and not (
        any(not isinstance(message, str) for message in argument)
    )


def ensure_bucket(argument: Any) -> Bucket:
    if is_bucket(argument): return set(argument)
    raise BucketError('Argument must be a valid bucket')


def format_bucket(bucket: Bucket, subject_substitute: Optional[str]) -> FormattedBucket:
    formatted_bucket: set[str] = set()

    for message in bucket:
        if message.startswith(SUBJECT_PLACEHOLDER):
            message = message.replace(SUBJECT_PLACEHOLDER, subject_substitute or str(), 1).strip()
            # [NOTE] Edge case is when it is undesired for us to uppercase the first character
            if subject_substitute is None: message = f'{message[0].upper()}{message[1:]}'

        formatted_bucket.add(message)

    return list(formatted_bucket)
