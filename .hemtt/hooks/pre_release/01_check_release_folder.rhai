// Fail-fast guard for the release folder.
//
// HEMTT copies `[hemtt.release] folder` verbatim into the archive entry names
// and performs no validation, so a value containing Windows-illegal characters
// produces a zip that cannot be extracted on Windows. `python tools/release.py`
// sanitizes it automatically; this hook protects manual `hemtt release` runs.

fn is_safe_name(name) {
    let forbidden = "<>:\"/\\|?*";
    let reserved = ["CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"];

    if name.len == 0 {
        return false;
    }
    for ch in name.chars() {
        if ch < ' ' || forbidden.contains(ch) {
            return false;
        }
    }
    let trimmed = name;
    trimmed.trim();
    if trimmed != name {
        return false;
    }
    if name.ends_with(".") || name.ends_with(" ") {
        return false;
    }
    if reserved.contains(name.to_upper()) {
        return false;
    }
    true
}

let prefix = HEMTT.project().prefix();
if !is_safe_name(prefix) {
    fatal("Project prefix is not a valid Windows name: '" + prefix + "'");
}

// `HEMTT.project()` does not expose the release folder, so read it from the
// project file directly and only consider the [hemtt.release] section.
let toml = HEMTT_RFS.join(".hemtt").join("project.toml").open_file().read();
let section = "";
let folder = "";
let has_folder = false;
for line in toml.split('\n') {
    let text = line;
    text.trim();
    if text.starts_with("[") && text.ends_with("]") {
        section = text;
    } else if section == "[hemtt.release]" && text.starts_with("folder") {
        let parts = text.split('"');
        if parts.len >= 2 {
            folder = parts[1];
            has_folder = true;
        }
    }
}

if has_folder && !is_safe_name(folder) {
    fatal("[hemtt.release] folder is not Windows-safe: '" + folder +
        "'. Run `python tools/release.py` to fix it automatically.");
}
