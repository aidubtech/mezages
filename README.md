<h1 align="center">Mezages</h1>
<p align="center">A package for the management of operational messages</p>

### Quick Start

```bash

$ flake8 src tests

```

```bash

$ pyright src tests

```

``` bash

# This only needs to be executed once
$ pipenv install --editable .

```

```bash

# Ensure to install package before running tests
$ pytest --no-header src tests

```

### Entities

An entity is that which has one or more messages associated with it
An entity represent anything, such as a `datum`, `process`, `operation` etc
An entity is identified by a `key` but fully by a `path` which shows its `lineage`

An entity can be said to be `basic`, `array-like` or `record-like` based on how its path is constructed
**Note that** this have nothing to do with the array and record data types in different programming languages

If an entity's path ends with an `integer` key, then its parent must be an `array-like` entity

### Messages

A message is a string associtated with an entity, which can be `partial` or `complete`
The array of messages associated with an entity is called a `bucket` of messages
Entities can be associated with both `partial` and `complete` messages at the same time
Messages are said to be `partial` if they start with the entity placeholder => `{entity}`

We will have a base path to hold messages for the base entity itself
- The base path will be named `base` for now, but can be changed at anytime in the library
- In order to not break user codes, we will assign the base path to the global variable `base_path`

### Entity Placeholder Replacement

Replacement of an entity placeholder will happen if it containing message is partial
We will try as much as possible to replace entity placeholders with texts that make messages more user friendly
In cases where we are unable to compose good texts for entity placeholder replacements, we default to the entities paths

> Replacement Scenario #1

If an entity's parent is an `array-like` entity, then do the following
- If entity's path is a key, replace the entity placeholder with the text `Item at index { idx }`
- Otherwise, replace the entity placeholder with the text `Item at index { idx } in { parent-path }`

> Replacement Scenario #2

If an entity's parent is a `record-like` entity, then do the following
- If entity's path is a key, replace the entity placeholder with `{ phrasified-key }`
- Otherwise, replace the entity placeholder with the text `{ phrasified-key } in { parent-path }`

### Library Features

- Create a new instance of Mezages optionally with a store
- Add one or more messages for each path within an instance of Mezages
- Get all messages resolved as a map or a flat array
- Merge an instance of Mezages into the current instance
- Unite a store with the current Mezages instance

### Notes, Caveats & Questions

- The goal is to handle formatting of messages for users, so they don't do it themselves
- The only thing that make sense for users to configure if considered is the entity substitutes
- We should never have support for functionalities whose purpose is simply to aid once in a while debugging
- Getting the store unresolved is not useful to users, since they should not be resolving messages on their end
