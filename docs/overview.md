<h1 align="center">Overview</h1>

Mezages is a package that is responsible for the collation, organization and formatting of user facing messages

The following are topics we will discuss under this package
- [Sacks](#sacks)
- [Subjects](#subjects)
- [Messages](#messages)
- [Public Interface](#behaviours)

## Sacks

We want to reserve the name `mezages` for the package when having conversations, but we do have a `Mezages` class which is the core of the package and we don't want to call instances of this class `mezages` too. So we decided to refer to any instance of the `Mezages` class as a `sack` of organized messages

Now, we define a `sack` as an instance of the Mezages class that internally manages a `store` of messages. This internal store is a mapping of `path` and `bucket` pairs, where each path is a string that must match a strict pattern, and each bucket is a non-empty set of messages

Each path within a sack will always refer to a datum which can be of any data type, except for a special path called the `base path` which will hold messages that may or may not relate to a datum

Kindly note and get familiarized with the terms used in the above definitions: `Sack`, `Store`, `Path`, `Bucket`, `Base Path`

## Subjects

A subject is a datum identified by a path in a sack that is mapped to a bucket

A path (*excluding the base path*) is a string that is made up of one or more `tokens` joined together by a dots
- A token can be of type `index` or `key`
- An index type token is any string that matches the pattern `[<int>]`. Examples: `[0]`, `[2]`, `[10]`, etc
- A key type token is any string that contains only alphabet, integer and underscore characters. Examples: `1`, `_`, `data01`, `int_num2`, etc
- Examples of path strings includes but not limited to the following: `[0]`, `email`, `data.users.[0].name`, `data.members.[0].roles.[1].key`, etc

The exact data type of a subject is only known outside of a sack. However, we can "kind of" deduce a custom type from the subject's path using the following logic
- Given a subject in a sack
- If there are other subjects in the sack whose path starts with the subject's path
- Then we associate a type to the subject by looking at the first token after the subject's path within each of the other subjects paths
    * If that first token is a key type token, then we say the subject is of `record` type
    * However, if that first token is an index type token, then we say the subject is of `array` type

**Note that:** We should have a constraint that a sack should only contain paths whose first tokens are homogeneous (i.e either key or index type but not both)

## Messages

These are texts that will be presented in the most user-frendly form to keep users informed about operations

As mentioned above, a set of one or more messages is refered to as a `bucket` of messages, where a bucket is always owned by a subject

A message can be one of two types, namely (1) Partial (2) Complete

A partial message is one that starts with the subject placeholder which can be any string, but it will be assigned to a global variable named `subject_placeholder`, so as to not break downstream codes. But for now, we will set the global variable as such -> `subject_placeholder = '{subject}'`

A message that is not partial is said to be complete regardless of whether or not it contains the subject placeholder, but in the wrong position

Internally, we will attempt to replace subject placeholders with string substitutes that makes an entire message read more user-friendly. But if that is impossible, we will fallback to the subject's path

## Public Interface

We have the `all` property which returns a flat list of formatted messages

We have the `map` property which returns a dictionary of paths mapped to buckets of formatted messages
