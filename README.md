# sword-test

This repository is a collection of test cases for [Sword](https://www.crosswire.org/sword/index.jsp) module development.

## Installation

```
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
pytest --modulename HunKal --moduleconf ../HunKal/hunkal.conf --modulexml ../HunKal/osis.xml
```

The argument names speak for themselves.
