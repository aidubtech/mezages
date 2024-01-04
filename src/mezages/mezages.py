MezagesStore = dict[str, set[str]]


class MezagesError(Exception):
    pass


class Mezages:
    def __init__(self, store: MezagesStore = dict()) -> None:
        self.__store = self.__ensure_store(store)

    @property
    def store(self) -> MezagesStore:
        return dict(self.__store)

    def __ensure_store(self, store: MezagesStore) -> MezagesStore:
        # Raise the MezagesError exception on failed validations
        # Ensure that each key conform to the expected string format
        # Ensure that each value is a set of strings representing message texts
        return store
