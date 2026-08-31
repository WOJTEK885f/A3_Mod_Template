# A3_Mod_Template

**Version: 0.0.0**

Mod project template for Arma 3 using [HEMTT](https://hemtt.dev/) and [CBA_A3](https://github.com/CBATeam/CBA_A3).

This repository is a starting point for a new Arma 3 mod. It wires up a modern HEMTT build pipeline, CI validation, and a set of reusable tooling so you can focus on writing your mod instead of configuring your toolchain.

## Features

- HEMTT-based build pipeline (`check`, `dev`, `release`, `launch`) with version management.
- GitHub Actions validation: HEMTT lints plus config-style and stringtable validation.
- Tooling under `tools/` for style checks and structured releases.
- Workshop mod presets for launching and testing against common dependencies.

## Prerequisites

- [HEMTT](https://hemtt.dev/installation) (install via `winget install hemtt`).
- [CBA_A3](https://steamcommunity.com/sharedfiles/filedetails/?id=450814997) for development/testing.

## Setup

The template uses placeholder values that must be renamed for your own mod. Replace every occurrence of the following:

| Placeholder       | Where                                             |
| ----------------- | ------------------------------------------------- |
| `TMP_MOD_NAME`    | `.hemtt/project.toml` (`name`)                    |
| `TMP_MOD_AUTHOR`  | `.hemtt/project.toml` (`author`, `[properties]`)  |
| `TMP_MOD_PREFIX`  | `.hemtt/project.toml` (`prefix`), addon names, logos |

Concretely:

1. Open `.hemtt/project.toml` and set `name`, `author`, and `prefix`.
2. Rename the logo files to match your prefix (e.g. `logo_<prefix>_ca.paa`, `logo_<prefix>_over_ca.paa`).
3. Create your addons under `addons/` (e.g. `addons/<prefix>_main`). The `mainprefix = "z"` should match each addon's `$PBOPREFIX$` (`z\<prefix>\addons\<addon>`).
4. Add a `LICENSE.md` for your project (see the **License** section below).

## Project Structure

```
.
├── .hemtt/          # HEMTT configuration, hooks, and version scripts
│   ├── project.toml
│   ├── lints.toml
│   ├── launch.toml
│   ├── hooks/       # pre_build / post_release hooks
│   └── scripts/     # version bump scripts
├── addons/          # Your addons (one folder per PBO)
├── docs/            # Source-of-truth README (promoted to root on release)
├── tools/           # Python tooling for style checks and releases
├── mod.cpp          # Mod metadata (include via [files])
└── README.md        # Version-stamped mirror of docs/README.md
```

## Commands

| Command                 | Purpose                                            |
| ----------------------- | -------------------------------------------------- |
| `hemtt check`           | Validate the project for errors and lints.         |
| `hemtt dev`             | Development build for testing.                     |
| `hemtt release`         | Build a signed, versioned release.                 |
| `hemtt launch`          | Launch Arma 3 with the mod and configured mods.    |
| `python tools/release.py` | Bump version, write loadorder, validate, release. |

## Tooling

`tools/` contains Python helpers used by the project and CI:

- `config_style_checker.py` — validates `.cpp/.hpp/.rvmat/.cfg` style (tabs, brackets, class formatting).
- `stringtable_validator.py` — validates `stringtable.xml` structure and style.
- `release.py` — orchestrates a release (version bump, loadorder, validation).
- `logger.py` — shared logging and project-prefix helpers used by the other tools.

The SQF and stringtable *usage* lints are handled natively by HEMTT (`lints.toml`), so the tools focus on what HEMTT does not check.

## Versioning

Versions are managed in `addons/main/script_version.hpp` via `.hemtt/scripts/update_*.rhai`. The README is promoted from `docs/` to the repo root on every release, so the root `README.md` reflects the latest released version while `docs/README.md` remains the maintained copy.

## License

This template reuses and adapts tooling from other Arma 3 projects (ACE3, and others) which may carry their own licenses. Add a `LICENSE.md` compatible with those upstream licenses before distributing your work.
