<h1 align="center">
    <img src="logo.png" alt="logo" width="25px">
    Mezages
</h1>

<p align="center">A library for the collection and organization of operational messages</p>

<a href="" title="message icons">Message icons created by Freepik - Flaticon</a>

## Overview

An operation message is a description of the outcome of an action which can be an execution within a function, class or module

An operational message can be about an error, warning or just an information about what is going on

Operational messages will usually have a summary and description of the situation been described

Operational messages are usually defined within a context which gives them their meaning

Contexts can be chained, thereby having sub-contexts other some parent context

A sack is an object that present an interface for registering and organizing operational messages

Its structure looks something libe the below

```python

{
    'global': {
        'notice': [
            {
                'ctx': 'global',
                'type': 'notice',
                'summary': 'Some summary about current situation',
                'description': 'This should describe how the consumer of the message should address it',
            },
        ],
    },
    'some_context': {
        'error': [
            {
                'ctx': 'some_context',
                'type': 'error',
                'summary': 'Some summary about current situation',
                'description': None,
            },
        ],
    },
    'parent_context.child_context': {
        'warning': [
            {
                'ctx': 'parent_context.child_context',
                'type': 'warning',
                'summary': 'Some summary about current situation',
                'description': 'This should describe how the consumer of the message should address it',
            },
        ],
    },
},

```

> Adding messages into the default context (global)
> Adding a message into a named context
> Mounting the sack on a mount context path
> Merging a sack into a current instance

## Getting Started

1. Ensure to be using python version 3.11+

2. Clone the repository

```bash

$ git clone https://github.com/aidubtech/mezages.git

```

3. Install the prefered environment and dependencies manager

```bash

$ python -m pip install pipenv

```

4. Install the required dependencies into a local virtual environment

```bash

$ PIPENV_VENV_IN_PROJECT=true pipenv install

```

## Workflow Commands

1. Ensure that the virtual environment has been activated or execute

```bash

$ source .venv/bin/activate

```

2. Format the codebase with [black](https://black.readthedocs.io/en/stable/index.html)

```bash

$ black src tests

```

3. Run unit tests with [pytest](https://docs.pytest.org/en/8.0.x/contents.html)

```bash

$ pytest --no-header tests

```

4. Run type checks with [pyright](https://microsoft.github.io/pyright)

```bash

$ pyright src tests

```

## Maintainers

<table>
    <tbody>
        <tr>
            <td align="center">
                <a href="https://github.com/belloibrahv">
                    <img src="https://github.com/belloibrahv.png" width="80px" alt="avatar">
                </a>
                <br>
                <div>Bello Ibrahim</div>
            </td>
            <td align="center">
                <a href="https://github.com/yuusuf4real">
                    <img src="https://github.com/yuusuf4real.png" width="80px" alt="avatar">
                </a>
                <br>
                <div>Yusuf Ariyibi</div>
            </td>
            <td align="center">
                <a href="https://github.com/abdulfataiaka">
                    <img src="https://github.com/abdulfataiaka.png" width="80px" alt="avatar">
                </a>
                <br>
                <div>Abdulfatai Aka</div>
            </td>
        </tr>
    </tbody>
</table>

## License

Licensed under the [MIT](LICENSE) License

Copyright © 2024 Aidub Technologies
