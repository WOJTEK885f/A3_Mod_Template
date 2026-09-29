let releases = HEMTT_RFS.join("releases");
let src = releases.join(HEMTT.project().prefix() + "-latest.zip");

// Build a Windows-safe file name from the project name.
// Drop characters Windows forbids (< > : " / \ | ? *) and control characters.
let forbidden = "<>:\"/\\|?*";
let name = "";
for ch in HEMTT.project().name().chars() {
    if ch >= ' ' && !forbidden.contains(ch) {
        name += ch;
    }
}
name.trim();

// Windows silently strips trailing dots and spaces from file names.
while name.len > 0 && (name.ends_with(".") || name.ends_with(" ")) {
    name.pop();
}

// Windows reserves these device names (case-insensitive) for any extension.
let reserved = ["CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"];
if reserved.contains(name.to_upper()) {
    name = "_" + name;
}

let dst = releases.join(name + "_v" + HEMTT.project().version().to_string_short() + ".zip");

print("Moving zip to " + dst);
if src.is_file() && !src.move(dst) {
    fatal("Failed to move " + src + " to " + dst);
}
