let releases = HEMTT_RFS.join("releases");
let src = releases.join(HEMTT.project().prefix() + "-latest.zip");
let dst = releases.join(HEMTT.project().name() + "_v" + HEMTT.project().version().to_string_short() + ".zip");

print("Moving zip to " + dst);
if src.is_file() && !src.move(dst) {
    fatal("Failed to move " + src + " to " + dst);
}
