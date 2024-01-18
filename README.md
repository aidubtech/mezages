<h1 align="center">Mezages</h1>
<p align="center">A package to handle the formatting of operational messages</p>

## Getting Started

Ensure you are using python version 3.11+

Clone the repository -> `git clone https://github.com/aidubtech/mezages.git`

Install pipenv with pip -> `python -m pip install pipenv`

Install all package dependencies into a local virtual environment -> `PIPENV_VENV_IN_PROJECT=true pipenv install`
* Note that once vscode loads the local virtual environment into your shells, dependency installations can just use `pipenv install`
* Otherwise, you will have to utilize the commands `pipenv shell` and `pipenv run` to work within the created local virtual environment

Hurray!!! You are now ready to start using the worklow commands below to work and contribute to package

## Workflow Commands

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

## Documentation

- [Overview](docs/overview.md)
- [Interface](docs/interface.md)

## Maintainers

[@belloibrahv](https://github.com/belloibrahv)
[@yuusuf4real](https://github.com/yuusuf4real)
[@abdulfataiaka](https://github.com/abdulfataiaka)

## License

Copyright © 2024 Aidub Technologies
