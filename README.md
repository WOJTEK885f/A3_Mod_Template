# A3_Mod_Template by WOJTEK885

Arma 3 mod project template using [HEMTT](https://hemtt.dev/) and [CBA_A3](https://github.com/CBATeam/CBA_A3). Includes basic configuration, automation scripts, additional utilities and other QoL features. Made with the [ACE3 Coding Guidelines](https://ace3.acemod.org/wiki/development/) in mind and general good practices to make your modding life easier.

For HEMTT installation and configuration please refer to [The HEMTT Book](https://hemtt.dev/index.html).

> [!NOTE]
> This guide just tells about the template, it's not intended to be a mod readme, nor be a part of the released mod.
>
> - Mod README template can be found in [`docs/README.md`](./docs/README.md).

## Initial Project Setup

1. Find and replace every occurrence of the following: (Ctrl+Shift+F in VSCode)

| Placeholder       | Replace with      | Comments                   | Example                     |
| ----------------- | ----------------- | -------------------------- | --------------------------- |
| `TMP_MOD_NAME`    | Mod's full name   |                            | Advanced Banana Environment |
| `TMP_MOD_AUTHOR`  | Mod's author      | that's you or your team    | ABE Team                    |
| `TMP_REPO_OWNER`  | GitHub repo owner |                            | ABE-Organization            |
| `TMP_REPO_NAME`   | GitHub repo name  | no spaces, use _ or - or . | ABE3                        |
| `TMP_MOD_PREFIX`  | Mod's prefix      | all lowercase              | abe                         |
| `TMP_MOD_LICENSE` | Chosen license    |                            | APL-ND                      |
| `TMP_MOD_ID`      | Steam Workshop ID | after the initial upload   | 1234567890                  |

2. Add a logo file named `logo_TMP_MOD_PREFIX_ca.paa` (referenced in `./mod.cpp`).
3. Add a `LICENSE.md` for your project, replacing the template's license.

### After the initial setup:

* Root [`README.md`](./README.md) file should be replaced with [`docs/README.md`](./docs/README.md).
* Content of the guide you're reading now can be later found in [`docs/TEMPLATE-GUIDE.md`](docs/TEMPLATE-GUIDE.md) or deleted if not needed.

> [!IMPORTANT]
> Remember that `docs/README.md` is treated as the source-of-truth and overwrites the root `README.md` after every release.

## Project Structure

```
.
├── .github/         # GitHub config and CI/CD workflows
├── .hemtt/          # HEMTT configuration
│   ├── project.toml
│   ├── lints.toml
│   ├── launch.toml     # Launch mods are configured here (includes some suggested mods and presets)
│   ├── hooks/          # Automated scripts on build / release
│   └── scripts/        # Version bump scripts used by tools
├── addons/          # Your addons (one folder per PBO)
│   ├── common/         # Add shared assets, scripts and other content here
│   └── main/           # Main addon with some utility macros
├── docs/            # Add your mod documentation here
├── tools/           # Python tooling for lints and other automation
├── mod.cpp          # Mod metadata seen by the game
└── README.md        # Version-stamped mirror of docs/README.md
```

## License

- The template's original files are licensed under the **MIT** license - see the repo root [`LICENSE.md`](./LICENSE.md).
- `tools/config_style_checker.py` and `tools/stringtable_validator.py` are derived from the ACE project and remain under the **GPLv2** license; they are not covered by the MIT license - see [`THIRD-PARTY-NOTICES.md`](./THIRD-PARTY-NOTICES.md).

When building a mod from this template, replace the `TMP_MOD_LICENSE` placeholder and the license file with your own mod's license. MIT means you can do whatever you want and your addon content is licensed however you choose.

> [!TIP]
> Not sure which license to pick? You can use one of the official Arma Public Licenses (for example `APL`/`APL-SA`/`APL-ND`). You can read their full terms on the [Bohemia Interactive Licenses](https://www.bohemia.net/community/licenses) page.
