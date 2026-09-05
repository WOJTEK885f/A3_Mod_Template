# Contributing Setup & Guidelines

Thanks for taking the time to contribute to TMP_MOD_NAME!

## Setting up the Development Environment

### Prerequisites

- Arma 3 and [CBA_A3](https://github.com/CBATeam/CBA_A3)
- [HEMTT](https://hemtt.dev/)
- Python 3.11+
- Git

### 1. Clone the repository

```cmd
git clone https://github.com/TMP_REPO_OWNER/TMP_REPO_NAME.git
cd TMP_REPO_NAME
```

If you are starting a new mod from this template instead, first replace all
`TMP_...` placeholders as described in the [README](../README.md)
(`docs/TEMPLATE-GUIDE.md`) before contributing.

### 2. Install HEMTT

The latest version of HEMTT can be installed by running:

```cmd
winget install hemtt
```

## Building and Validation

Run the same checks as the CI pipelines before opening a pull request:

```cmd
hemtt check --error-on-all --pedantic
python tools/config_style_checker.py
python tools/stringtable_validator.py
```

## Coding Guidelines

This mod follows the same coding guidelines as the ACE3 mod, which can be
found [here](https://ace3.acemod.org/wiki/development/coding-guidelines).

Stringtable keys follow the `STR_<ACRONYM>_<Component>_<Key>` format, with the
acronym uppercased (e.g. `STR_ABE_Common_DisplayName`). The acronym must use
the same letters as the mod's prefix.

## Pull Request Process

- Give the pull request a descriptive title following the format
  `Component - Add|Fix|Improve|Change|Make|Remove {changes}`.
- Split large changes into separate commits.
- Update the documentation in [`docs/`](../docs) if your change affects it.
- Make sure your branch is up to date with the base branch before requesting a review.