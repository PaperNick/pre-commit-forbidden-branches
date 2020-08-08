# Pre-commit hook to forbid commits

[![Test Status](https://github.com/papernick/pre-commit-forbidden-branches/workflows/CI/badge.svg)](https://github.com/PaperNick/pre-commit-forbidden-branches/actions)

The purpose of this pre-commit hook is to prevent accidental commits in a specified list of branches, e.g. `master`, `develop`, etc.


## Dependencies:

* [Git](https://git-scm.com/)
* [Pre-commit](https://github.com/pre-commit/)


## Installation

If this is your first time configuring `pre-commit`, follow the installation instructions:
https://pre-commit.com/#install

Add this to your `.pre-commit-config.yaml` file under the `repos` key:

```
- repo: https://github.com/PaperNick/pre-commit-forbidden-branches
  rev: 0.2.0
  hooks:
  - id: forbid-commits-hook
    args: ['master']
    pass_filenames: false
```


### Specify the forbidden branches

You can use the `args` key to specify more than one branch:

```
args: ['master', 'develop']
```


## Development

Create a virtual environment:

```
python3 -m venv venv/
```

Activate the venv:

```
source venv/bin/activate
```

Install the development requirements:

```
pip install -r requirements_dev.txt
```

Run the tests:

```
python -m pytest tests/ --cov pre_commit_hook/
```
