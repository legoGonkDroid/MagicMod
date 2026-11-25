#!/usr/bin/env python3
"""Assemble a packwiz pack from this Prism instance.

Prism stores mod metadata in minecraft/mods/.index/*.pw.toml (packwiz format),
but packwiz-installer installs each jar next to its .pw.toml, so the metadata
has to live in mods/ inside the pack. This script copies the tracked game-dir
content plus the flattened metadata into build/pack/ and writes pack.toml.
Run `packwiz refresh --build` inside build/pack/ afterwards (CI does this).

Usage: python3 tools/build_pack.py [--version 1.2.3]
       python3 tools/build_pack.py --check   # run locally before tagging a release
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAME = ROOT / "minecraft"
OUT = ROOT / "build" / "pack"

# Game-dir folders that are part of the pack (everything else is personal/runtime).
OVERRIDE_DIRS = ["config", "defaultconfigs", "kubejs", "datapacks", "resourcepacks", "shaderpacks"]
OVERRIDE_FILES = ["icon.png"]
# Same exclusions as .gitignore, for local builds from a dirty working tree.
EXCLUDE = shutil.ignore_patterns(
    "exported", "probe", "jsconfig.json", "probe-settings.json", "recovery",
    "embeddium-fingerprint.json", "xaeropatreon.txt", "indigo-renderer.properties",
    "search_index",
)


SIDE_RE = re.compile(r"^side = .*$", re.M)
FILENAME_RE = re.compile(r"""^filename = (['"])(.*)\1$""", re.M)


def check():
    """Lint the local mods folder against the tracked metadata (needs the jars, so run locally)."""
    mods = GAME / "mods"
    files = {p.name for p in mods.iterdir() if p.is_file()}
    problems, seen = [], {}
    for meta in sorted((mods / ".index").glob("*.pw.toml")):
        text = meta.read_text()
        m = FILENAME_RE.search(text)
        name = m.group(2) if m else None
        if name in seen:
            problems.append(f"{meta.name}: duplicate of {seen[name]} (same jar {name})")
        seen[name] = meta.name
        if "[update.curseforge]" not in text:
            problems.append(f"{meta.name}: not sourced from CurseForge")
        if name + ".disabled" in files:
            problems.append(f"{meta.name}: jar is disabled locally but would ship in the pack "
                            "(remove the mod in Prism if it shouldn't be in the pack)")
        elif name not in files:
            problems.append(f"{meta.name}: metadata for {name} but the jar is missing")
    for f in sorted(files):
        if f.endswith(".jar") and f not in seen:
            problems.append(f"{f}: jar has no .pw.toml (reinstall it via Prism's CurseForge browser)")
    for p in problems:
        print("  " + p)
    print(f"{len(problems)} problem(s)")
    return not problems


def component_versions():
    pack = json.loads((ROOT / "mmc-pack.json").read_text())
    versions = {c["uid"]: c["version"] for c in pack["components"]}
    return versions["net.minecraft"], versions["net.neoforged"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="dev")
    ap.add_argument("--check", action="store_true", help="lint mods/ vs metadata, don't build")
    args = ap.parse_args()
    if args.check:
        sys.exit(0 if check() else 1)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for d in OVERRIDE_DIRS:
        src = GAME / d
        if src.is_dir() and any(src.iterdir()):
            shutil.copytree(src, OUT / d, ignore=EXCLUDE)
    for f in OVERRIDE_FILES:
        if (GAME / f).is_file():
            shutil.copy2(GAME / f, OUT / f)

    mods_out = OUT / "mods"
    mods_out.mkdir()
    metas = sorted((GAME / "mods" / ".index").glob("*.pw.toml"))
    for meta in metas:
        # Prism's CurseForge metadata often has side = 'server' or '' (it misreads CF's
        # environment data); packwiz-installer would then skip the mod on clients.
        text = SIDE_RE.sub("side = 'both'", meta.read_text(), count=1)
        (mods_out / meta.name).write_text(text)

    mc, neoforge = component_versions()
    (OUT / "index.toml").write_text('hash-format = "sha256"\n')
    (OUT / "pack.toml").write_text(
        'name = "MagicMod"\n'
        'author = "jarroyer"\n'
        f'version = "{args.version}"\n'
        'pack-format = "packwiz:1.1.0"\n\n'
        "[index]\n"
        'file = "index.toml"\n'
        'hash-format = "sha256"\n'
        'hash = ""\n\n'
        "[versions]\n"
        f'minecraft = "{mc}"\n'
        f'neoforge = "{neoforge}"\n'
    )
    # Keep packwiz from indexing its own helper files.
    (OUT / ".packwizignore").write_text("README.md\n")

    print(f"Assembled {len(metas)} mods + overrides into {OUT.relative_to(ROOT)} "
          f"(MC {mc}, NeoForge {neoforge}, version {args.version})")


if __name__ == "__main__":
    main()
