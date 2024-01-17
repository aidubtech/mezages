<h1 align="center">Overview</h1>

Mezages is a `message bag` management package that handles the formatting of operational messages, so that developers can focus on displaying messages to their end users instead of dealing with formatting them first

The following are topics we will discuss under this package
- [Subjects](#subjects)
- [Messages](#messages)
- [Behaviours](#behaviours)

## Subjects

These are entities that will be associated with one or more messages

A subject can be one of the following types, namely (1) Array (2) Record (3) Unknown

A subject may have `children` (a.k.a child subjects or nested subjects) if it is of array or record type

Each message bag in its entirety will refer to some `base subject`

## Messages

These are texts presented in the most user-frendly form to keep users informed about their operations

A collection of one or more messages will be refered to as a `bucket of messages`

Each bucket of messages will always be associated with a subject

## Subject Paths

A subject within a message bag is identified by a `path` which always shows its `lineage`

A base subject will always be identified within its message bag by a special path called the `base path`

A path (*excluding the base path*) is made up of one or more `tokens`, which can be of `index` or `key` type
- A token of index type will match the format `[integer]`
- A token of key type must be string containing only alphabet, integer and underscore characters

## Getting Subject Type

A subject is said to have a parent of `record` type if the last token in its path is of `key` type

A message bag is said to refer to a base subject of type `record` if each child's path starts with a `key` type token

A subject is said to have a parent of `array` type if the last token in its path is of `index` type

A message bag is said to refer to a base subject of type `array` if each child's path starts with an `index` type token

## General Constraints

A message bag must never contain children with paths starting with index and key tokens at the same time

## Supported Behaviours

Initialize a message bag (Mezages) optionally with an initial store

Add one or more messages to a path while keeping the uniqueness of its bucket

Get all formatted messages as a mapping or a flat array

Merge a store into the current Mezages instance optionally on a mount point

Merge an instance of Mezages into the current instance optionally on a mount point
