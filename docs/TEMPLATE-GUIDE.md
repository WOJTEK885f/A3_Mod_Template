# A3_Mod_Template by WOJTEK885

This guide is for mod developers who build a mod from this template. It explains setup, structure and tooling provided. This file is not part of the released mod.

* Target mod README template can be found in [`docs/README.md`](./docs/README.md)

After initial setup:

* Root [`README.md`](./README.md) file should be replaced with [`docs/README.md`](./docs/README.md) (this is also done automatically after release).
* Content of the file you're reading now can be later found in [`docs/TEMPLATE-GUIDE.md`](docs/TEMPLATE-GUIDE.md) or deleted if not needed.

## Initial Project Setup

The template uses placeholders that must be renamed for your own mod. Find and replace every occurrence of the following (Ctrl+Shift+F in VSCode):

| Placeholder       | Replace with      | Comments                   | Example                     |
| ----------------- | ----------------- | -------------------------- | --------------------------- |
| `TMP_MOD_NAME`    | Mod's full name   |                            | Advanced Banana Environment |
| `TMP_MOD_AUTHOR`  | Mod's author      | you or your team           | ABE Team                    |
| `TMP_REPO_OWNER`  | GitHub repo owner |                            | ABE Organization            |
| `TMP_REPO_NAME`   | GitHub repo name  | no spaces, use _ or - or . | ABE3                        |
| `TMP_MOD_PREFIX`  | Mod's prefix      | lowercase                  | abe                         |
| `TMP_MOD_LICENSE` | Chosen license    |                            | APL-ND                      |

TODO: Update everything below
Concretely:

1. Open `.hemtt/project.toml` and set `name`, `author`, and `prefix`. The mod's display title (`TMP_MOD_NAME`, e.g. in `README.md` and `mod.cpp`) and GitHub repo URL (from `TMP_MOD_AUTHOR`/`TMP_REPO_NAME`) should be set to your own values.
2. Rename the logo files to match your prefix (e.g. `logo_<prefix>_ca.paa`, `logo_<prefix>_over_ca.paa`).
3. Create your addons under `addons/` (e.g. `addons/<prefix>_main`). The `mainprefix = "z"` should match each addon's `$PBOPREFIX$` (`z\<prefix>\addons\<addon>`). Per-addon `README.md` files are optional and not required by the build.
4. Add a `LICENSE.md` for your project.

Files referenced but **not shipped** by the template are author-supplied and expected to be created for your mod:

- `meta.cpp` — referenced by `.hemtt/project.toml` (`[files] include`).
- `logo_TMP_MOD_PREFIX_ca.paa` and `logo_TMP_MOD_PREFIX_over_ca.paa` — referenced by `.hemtt/project.toml` and `mod.cpp`.

The user-facing `README.md` also uses self-explanatory `<...>` placeholders alongside the `TMP_MOD_*` tokens (e.g. `<One-liner>`, `<Feature>`, `<How to ...>`) that you should fill in with your own content.

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
