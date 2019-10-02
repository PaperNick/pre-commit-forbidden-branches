# Pre-commit hook to forbid commits

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
  rev: 0.0.1
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
py.test --cov pre_commit_hook tests/
```