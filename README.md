<h1 align="center">Mezages</h1>
<p align="center">A package for the management of operational messages</p>

## Terminologies

- Mezages
- Mezages Store
- Mezages Instance
- Entity, Key, Path & Bucket

## Entities

An entity is that which has one or more messages associated with it
An entity could be anything, such as a `datum`, `process`, `operations` etc
An entity is identified by a `key` but fully by a `path` which shows its `lineage`

An entity can be said to be `basic`, `array-like` or `record-like` based on how the path is constructed
**Note that** this have nothing to do with the array and record data types in programming languages

If an entity is contained within another entity (parent), then the following applies
- If the entity's path ends with an integer key, then the parent must be an `array-like` entity
- Otherwise, the parent must be a `record-like` entity

We should be able bind each path to a configuration object, which should not apply down the lineage

#### Messages

These are strings that are associtated with entities or sub-entities
A messages can be said to be `partial` or `complete`
Messages are partial if they start with the entity placeholder. Otherwise, they are complete
Buckets of messages can contain both partial and complete messages at the same time

We will have a base path to hold messages for an entity to separate them from those of sub-entities
- The base path will be named `base` for now, but can be changed at anytime in the library
- In order to not break user codes, we will assign the base path to the global variable `base_path`

#### Entity Placeholder Replacements

Replacement of the entity placeholder will happen if and only if a message is seen to be partial

An entity placeholder is replaced by default with the entity's path unless customized via paths configurations

However, if the entity's path is the base path, then we do the following
- Remove the entity placeholder from the message
- Trim whatever string is left
- Capitalize the first character only if reasonable

#### Library Entity Placeholder Replacements

The following must only happen through paths configurations

If an entity's parent is `array-like`, then do the following
- If entity's path is a key, then replace the placeholder with the text `Item at index < idx >`
- Otherwise, replace the placeholder with the text `Item at index < idx > in < parent-path >`

If an entity's parent is `record-like`, then do the following ( *Logic is coming soon* )

## Quick Commands

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
