# --- Initialization

# Should we initialize with a state?

# --- Features

# Ability to modifiers placeholders
# Split words only if snake case
# Uppercase the first character

# Map keys to placeholders backed by defaults from key

# Resolve and export messages in store filterable by keys

# Add one or more messages for a key
# Validate only new keys
# How to ignore unintended placeholders?

# Merge a mezage into another mezage at the root or mounted on a key
# Move placeholder mappings into the desitination and put mount point into consideration

# --- Notes

# placeholder format: {name:modifier:modifier:...}


class MezagesError(Exception):
    pass


class Mezages:
    def __init__(self) -> None:
        self.__store: dict[str, set[str]] = dict()

    def export(self, *keys: str) -> dict[str, set[str]]:
        return dict()

    def union(self, source: 'Mezages', mount: str | None = None) -> None:
        pass

    def merge(self, source: dict[str, set[str]], mount: str | None = None) -> None:
        pass
