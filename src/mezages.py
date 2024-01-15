import re
from typing import cast, Any, TypedDict, Optional


base_path = 'base'
entity_placeholder = '{entity}'

MezagesStore = dict[str, list[str]]
MezagesInputStore = dict[str, (set[str] | list[str] | tuple[str])]
MezagesPathConfig = TypedDict('MezagesPathConfig', { 'substitute': Optional[str] })

class MezagesError(Exception):
    pass


class Mezages:
    KEY_REGEX = r'(?:(?:\d+)|(?:[a-z](?:(?:[a-z0-9]*_)*[a-z0-9]+)*))'
    PATH_REGEX = fr'(?:(?:{KEY_REGEX}\.)*{KEY_REGEX})'

    def __init__(self, store: Any = dict()) -> None:
        self.__store = self.__ensure_store(store)

    def flat(self, only: list[str] = list(), omit: list[str] = list()) -> list[str]:
        '''
        Produce a flattened array of resolved messages from all or selected paths
        '''
        return [message for bucket in self.slice(only=only, omit=omit).values() for message in bucket]

    def slice(self, only: list[str] = list(), omit: list[str] = list(), resolve: bool = True) -> MezagesStore:
        '''
        Produce a mapping of path to resolved or unresolved messages from all or selected paths
        '''
        result: MezagesStore = dict()

        for path, bucket in self.__store.items():
            if (not only or path in only) and (not omit or path not in omit):
                result[path] = self.__resolve_messages(path, bucket) if resolve else list(bucket)

        return result

    def __is_path(self, key: Any) -> bool:
        return isinstance(key, str) and bool(re.fullmatch(self.PATH_REGEX, key))

    def __resolve_messages(self, path: str, messages: list[str]) -> list[str]:
        path_config: MezagesPathConfig = {'substitute': None}
        config_substitute = path_config.get('substitute', None)

        entity_substitute = (
            (str() if path == base_path else path)
            if config_substitute is None else config_substitute
        )

        resolved_messages: list[str] = list()

        for message in messages:
            if message.startswith(entity_placeholder):
                message = message.replace(entity_placeholder, entity_substitute, 1).strip()
                # An edge case is when the user does not want us to touch the message
                if entity_substitute == str(): message = f'{message[0].upper()}{message[1:]}'

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
                type(bucket) in (set, list, tuple) and bucket and not
                any(not isinstance(message, str) for message in bucket)
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
