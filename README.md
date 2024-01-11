<h1 align="center">Mezages</h1>
<p align="center">A package for the management of operational messages</p>


```bash

$ flake8

```

```bash

$ pyright

```

``` bash

$ pipenv install --editable .

```

```bash

$ pytest --no-header

```

```python

# Terminologies
# ---------------------------
# Mezages
# Mezages Store
# Mezages Instance

# Features
# ---------------------------
# Update export method to handle placeholder replacements in messages
# Add method to return all messages as a flattened set
# Add method to merge two mezages optionally on a mount path
# Add method to unite a mezages and a store optionally on a mount path
# Add method to insert one or more messages for a path
# Add support to map path to placeholder configuration (custom values | keys and paths manipulations)

# Keeping this here for now, might be removed later
PLACEHOLDERS = ('key', 'path', 'base-key', 'base-path')

```