# A3_Mod_Template — Development Guide

Mod project template for Arma 3 using [HEMTT](https://hemtt.dev/) and [CBA_A3](https://github.com/CBATeam/CBA_A3).

This document is for mod developers who build a mod from this template. It explains the setup, structure, and tooling provided here. The user-facing `README.md` describes the finished mod and is promoted from `docs/` on release — this file is not part of the released mod.

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
4. Add a `LICENSE.md` for your project.

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
| `python tools/release.py` | Bump version, validate, release. |

## Tooling

`tools/` contains Python helpers used by the project and CI:

- `config_style_checker.py` — validates `.cpp/.hpp/.rvmat/.cfg` style (tabs, brackets, class formatting).
- `stringtable_validator.py` — validates `stringtable.xml` structure and style.
- `release.py` — orchestrates a release (version bump, validation, release).
- `logger.py` — shared logging and project-prefix helpers used by the other tools.

The SQF and stringtable *usage* lints are handled natively by HEMTT (`lints.toml`), so the tools focus on what HEMTT does not check.

## Versioning

Versions are managed in `addons/main/script_version.hpp` via `.hemtt/scripts/update_*.rhai`. The README is promoted from `docs/` to the repo root on every release, so the root `README.md` reflects the latest released version while `docs/README.md` remains the maintained copy. A post-release hook renames the output archive (`releases/<prefix>-latest.zip`) to `<name>_v<version>.zip` (e.g. `TMP_MOD_NAME_v0.0.0.zip`).

## License

- The template's original files are licensed under the **MIT** license — see the repo root `LICENSE.md`.
- `tools/config_style_checker.py` and `tools/stringtable_validator.py` are derived from other projects and remain under the **GPLv2** license; they are not covered by the MIT license.

When building a mod from this template, replace the `TMP_MOD_LICENSE` placeholder in `README.md` with your own mod's license (for example `APL`/`APL-SA`/`APL-ND`). The template scaffolding keeps the licenses documented above, while your addon content is licensed however you choose.
