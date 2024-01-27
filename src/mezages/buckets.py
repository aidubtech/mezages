from typing import Any, Optional
from mezages.subjects import subject_placeholder


# ----------------------------------------
# Type Aliases
# ----------------------------------------

Bucket = set[str]

FormattedBucket = list[str]

# ----------------------------------------
# Exception Classes
# ----------------------------------------

class BucketError(Exception):
    pass


# ----------------------------------------
# Functions
# ----------------------------------------

def is_valid_bucket(argument: Any) -> bool:
    return type(argument) in (set, list, tuple) and not any(
        not isinstance(message, str) for message in argument
    )


def ensure_bucket(argument: Any) -> Bucket:
    if is_valid_bucket(argument): return set(argument)
    # Find a way to pretty print the structure this error
    raise BucketError(f'{repr(argument)} is an invalid bucket')


def format_bucket(bucket: Bucket, subject_substitute: Optional[str]) -> FormattedBucket:
    formatted_bucket: set[str] = set()

    for message in bucket:
        if message.startswith(subject_placeholder):
            message = message.replace(subject_placeholder, subject_substitute or str(), 1).strip()
            # [NOTE] Edge case is when it is undesired for us to uppercase the first character
            if subject_substitute is None: message = f'{message[0].upper()}{message[1:]}'

        formatted_bucket.add(message)

    return list(formatted_bucket)
