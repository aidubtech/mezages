<h1 align="center">Mezages</h1>
<p align="center">A package to handle the formatting of operational messages</p>

## Getting Started

Ensure you are using python version 3.11+

*Clone the repository*

```bash

$ git clone https://github.com/aidubtech/mezages.git

```

*Install pipenv with pip*

```bash

$ python -m pip install pipenv

```

*Install all package dependencies into a local virtual environment*

```bash

$ PIPENV_VENV_IN_PROJECT=true pipenv install

```

**Note:** Once VSCode loads the local virtual environment into your shells, dependency installations can be done simply by using the below commands. Otherwise, you will have to utilize the `pipenv shell` and `pipenv run` commands to work within the created local virtual environment

```bash

$ pipenv install

# OR

$ pipenv install <dependency>

```

## Quick Actions

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
$ pytest --no-header tests

```

## Learn More

* [Overview](docs/overview.md)

## Maintainers

<div style="display: flex; align-items: center; column-gap: 1rem">
    <div style="display: flex; align-items: center">
        <img src="https://github.com/belloibrahv.png" alt="avatar" style="width: 1.6rem; height: 1.6rem; border-radius: 50%" />
        <span style="margin-left: 0.3rem">Bello Ibrahim</span>
    </div>
    <div style="display: flex; align-items: center">
        <img src="https://github.com/yuusuf4real.png" alt="avatar" style="width: 1.6rem; height: 1.6rem; border-radius: 50%" />
        <span style="margin-left: 0.3rem">Yuusuf Ariyibi</span>
    </div>
    <div style="display: flex; align-items: center">
        <img src="https://github.com/abdulfataiaka.png" alt="avatar" style="width: 1.6rem; height: 1.6rem; border-radius: 50%" />
        <span style="margin-left: 0.3rem">Abdulfatai Aka</span>
    </div>
</div>

## License

Licensed under the [MIT](LICENSE) License

Copyright © 2024 Aidub Technologies
