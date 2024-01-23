<h1 align="center">Overview</h1>

Mezages is a package that defines a standard interface for collecting, organizing and formatting operational messages

The following are the topics that will be discussed under this package
* [Sacks](#sacks)
* [Tokens](#tokens)
* [Paths](#paths)
* [Buckets](#buckets)
* [Subjects](#subjects)
    - [Path Types](#path-types)
    - [Child Subjects](#child-subjects)
    - [Subject Types](#subject-types)

# Sacks

The core of the package will be a sack class that defines an interface for managing of a store, adding new messages, outputing formatted messages, and any other necessary functionalities that will make us achieve our set goals and objectives for the package

A `sack` is simply an instance of the sack class defined above

The `store` managed within a sack is simply a dictionary of string keys each one mapped to a unique array of one or more strings. Each string key will be called a `path`, and each string within the array will be called a `message`, while the array as a whole will be called a `bucket`

A path will be used to represent external entities for which we want to record messages. Each one of these entities will be called a `subject`

The store managed within a sack might look something like this

```python
{
    '%root%': {
        'Must be an object of record type',
        'Root subjects cannot hold partial messages',
    },
    'person': {
        'Must be an object of record type',
        'Unknown type subjects cannot hold partial messages',
    },
    'person.{roles}': {
        '{subject} cannot be an empty array',
        'Subject can hold both complete and partial messages',

    },
}
```

# Tokens

A `token` is a string that must be used in the construction of a path

It must conform to the specification of one of the `token types` listed below

`Index`
* This is a string that conforms to the format - `[<content>]`
* Where `<content>` is any integer greater than or equal to zero
* Examples include: `[0]`, `[10]`, `[213]`, `[5050]`, `[23231]`, etc

`Symbol`
* This is a string that conforms to the format - `{<content>}`
* Where `<content>` is a string that contains only alphabet, integer and underscore characters
* Examples include: `{data}`, `{recrod01}`, `{id_005}`, `{email_address}`, `{person_01_id}`, etc

`Unknown`
* This is a string that contains only alphabet, integer and underscore characters
* Examples include: `data`, `recrod01`, `id_005`, `email_address`, `person_01_id`, etc

# Paths

*See the introductry definition of a path and what it represent within a sack under the [Sacks](#sacks) section above*

A path is a string that must be made up of one or more tokens, each one joined to the next with a single dot character

Examples include:
* `0`
* `data`
* `[0]`
* `{user}`
* `data.{users}.[0].{name}`
* `records.[0].{person}.{role}.{name}`

Looking at the token and path examples above, we can deduce the statement that: `All tokens can be paths, but not all paths can be tokens`

We can see that a path shows the lineage of the subject it represents. However, the subject itself is identified by the last token in the path. Therefore, given a subject with the path `records.[0].{person}`, we will say that the subject's token is `{person}` and the subject's path is `records.[0].{person}`

# Buckets

*See the introductry definition of a bucket and what it represent within a sack under the [Sacks](#sacks) section above*

A message can be partial or complete. A message is said to be `partial` if it starts with the global `subject placeholder` value. Otherwise, it is `complete`

**Note:** Subject placeholders used at positions other than the start of a message will be ignored when formatting such message

Examples of partial messages include but are not limited to the following
* `{subject} cannot be an integer`
* `{subject} must have a value that is of string type`
* `{subject} given the name {subject} must be a boolean`

Examples of complete messages include but are not limited to the following
* `The {subject} must be of integer type`
* `Some user with id provided does not exist in the cache`
* `Propery name in {subject} with id {subject} is not valid`

The global placeholder can be any string value which can be changed at any time. For this reason, changes to this value can break downstream codes. Therefore, we will assign it to a global variable named `subject_placeholder` to prevent such issue. But within the context of this document, we will assume that it has been set to `{subject}`

Internally, we will attempt to replace only the first subject placeholder in partial messages with substitutes that makes the messages read more user-friendly. However, if we are unable to come up with a good substitute, we will fallback to the subject's path

**Constraint:** Only complete messages can be associated with root subjects and child subjects of unknown type

# Subjects

*See the introductry definition of a subject and how it is represented within a sack under the [Sacks](#sacks) section above*

A subject is also seen as an entity that can own a sack or just a bucket within a sack. A subject that owns a sack is called a `root subject`, while a subject that owns a bucket within a sack is called a `child subject`

### Path Types

A child subject will always have a path mapped to a bucket within a sack. Therefore, the path will be called a `child path`, which must conform to the constraints defined under the [Paths](#paths) section above

Subjects exist only because we want to associate messages with them. But the root subject is outside its own sack. We will need to represent it in one way or the other, so that we can associate messages with it. For this reason, we will have a special path called the `root path` that will represent a root subject within its own sack. But within the context of this documentation, we will assume that the root path has been set to `%root%`

The root path can be any string value which can be changed at any time. For this reason, changes to this value can break downstream codes. Therefore, we will assign it to a global variable named `root_path` to prevent such issue

### Child Subjects

A subject is said to have `child subjects` or `children` if
* It is a root subject with child subjects represented within its sack
* Or it's path starts the path of one or more child subjects within a sack

**Constraint:** The first token in each child's path of any subject must be of the same token type

### Subject Types

The true essence of a subject is only known outside of this package. Therefore, we cannot know it real type. For this reason, we will define some custom subject types that can be associate with subjects, to aid the proper formatting of messages associated with them

The following are the custom subject types that will be supported, along with how they will be associated with subjects
* A subject is said to be of `Record` type, if it has children, and the first token in each of its child's path is a `key` type token
* A subject is said to be of `Array` type, if it has children, and the first token in each of its child's path is an `index` type token
* A subject is said to be of `Unknown` type, if it has no children or the first token in each of its child's path is an `unknown` type token

### Example

Given a root subject that own a sack with the store below

```python
{
    '%root%': {
        'Must be an object of record type',
        'Root subjects cannot hold partial messages',
    },
    'person': {
        'Must be an object of record type',
        'Unknown type subjects cannot hold partial messages',
    },
    'person.{roles}': {
        '{subject} cannot be an empty array',
        'Subject can hold both complete and partial messages',

    },
    'person.{roles}.[0]': {
        'Item at index 0 must be of record type',
        '{subject} can hold both complete and partial messages',
    },
    'person.{gender}': {
        '{subject} must be a gender string value from the genders list',
    },
    
}
```

Then, we will can say the following
* The root subject have exactly four children
* Subject with the path `person` have exactly two children
* Subject with the path `person.{roles}` have exactly one child
* Subject with the path `person` has the root subject as its parent
* Subject with the path `person.{roles}.[0]` is not a child of subject with the path `person`
* Subject with the path `person.{roles}` has subject with the path `person` as its parent
* Subject with the path `person.{roles}.[0]` has subject with the path `person.{roles}` as its parent
* Subject with the path `person.{roles}` is of array type because the first token of its child paths is an index type token - `[0]`
* Subject with the path `person` is of record type because the first token of its child paths is a key type token - `{roles}` and `{gender}`