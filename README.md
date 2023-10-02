# turtled_server
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31010/)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
forked fastapi-skeleton from https://github.com/als95/fastapi-skeleton

## Installation

upload image to docker for local environment
```bash
c```

install dependencies of this project
```bash
python3 -m pip install --upgrade pip
pip3 install poetry==1.4.0
poetry install
```

## Run

### server
```bash
poetry run task server
```

### dev
```bash
poetry run task dev
```

### test
```bash
poetry run task test
```

### lint
```bash
poetry run task lint
poetry run black .
poetry run isort .
```
