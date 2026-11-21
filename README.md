# MagicMod

A magic-focused Minecraft **1.21.1** modpack on **NeoForge 21.1.267**, built around
Ars Nouveau and its addons, with Cataclysm bosses, MineColonies and a generated FTB Quests book
that takes you from novice mage to the Ender Dragon.

**Highlights**
- Ars Nouveau and about 30 addons (Additions, Elemental, Zero, Trinkets, Affinity, Caelum, Fauna, ...)
- L_Ender's Cataclysm bosses, used as quest-book milestones
- MineColonies with Ars Structurize Archwood villages, and Waystones
- Relics and Reliquified Ars Nouveau
- Quality of life: EMI, Jade, Xaero's Minimap/World Map, Embeddium, Sophisticated Backpacks/Storage
- A Starter Kit with a novice spell book, Arcanist armour and a colony starter

Java 21 and about 8 GB of RAM for the game are recommended.

## Installing (Prism Launcher)

### Option A: import a release (simplest)
1. Download `MagicMod-x.y.z.mrpack` from the [latest release](https://github.com/jarroyer/MagicMod/releases/latest).
2. In Prism: **Add Instance → Import → select the .mrpack**.
3. To update later, import the newer `.mrpack` over the instance (Prism keeps your worlds).

### Option B: auto-update on every launch (packwiz)
1. In Prism: **Add Instance → Vanilla**. Pick Minecraft 1.21.1, then **Edit → Version → Install NeoForge 21.1.267**.
2. Download [`packwiz-installer-bootstrap.jar`](https://github.com/packwiz/packwiz-installer-bootstrap/releases/latest)
   and put it in the instance's `minecraft/` folder.
3. **Edit → Settings → Custom commands**: enable it and set the *Pre-launch command* to:
   ```
   "$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://raw.githubusercontent.com/jarroyer/MagicMod/pack/pack.toml
   ```
4. Launch. Mods and configs download before the game starts, and every launch picks up the latest release.

Some CurseForge mods don't allow third-party downloads. If packwiz-installer opens a window
listing mods to download by hand, grab those files from the links it shows.

## Repository layout

This repo **is** a Prism instance folder. It mirrors [ATM-10](https://github.com/AllTheMods/ATM-10):
only the pack definition is tracked, not the mod jars or anyone's worlds.

| Path | What |
|---|---|
| `mmc-pack.json` | Minecraft and NeoForge versions (Prism component list) |
| `instance.cfg.example` | Minimal Prism settings. Copy it to `instance.cfg` when cloning (the real one is per-machine and ignored) |
| `minecraft/mods/.index/*.pw.toml` | The mod list: where each mod comes from, its version and hash (packwiz format, written by Prism) |
| `minecraft/config/`, `defaultconfigs/` | Mod configs, including the generated FTB Quests book |
| `minecraft/kubejs/` | KubeJS scripts |
| `minecraft/datapacks/` | Custom datapacks (added per world, not loaded automatically) |
| `questgen/` | Python generator for the quest book (`python3 questgen/build.py`) |
| `tools/build_pack.py` | Turns the instance into a packwiz pack in `build/pack/` (used by CI) |
| `changelogs/`, `CHANGELOG.md` | Release notes |

## Developing the pack (maintainer)

The working copy is the live Prism instance, so play and edit in the same folder:

1. Add or update mods **through Prism's mod browser** (Modrinth/CurseForge), so a `.pw.toml` gets
   written to `mods/.index/`. A jar dropped in by hand won't reach anyone else.
2. Change configs or scripts. For quest changes, edit `questgen/content/` and run `python3 questgen/build.py`.
3. Add notes to `CHANGELOG.md` and commit.
4. Release: write `changelogs/vX.Y.Z.md`, then `git tag vX.Y.Z && git push --follow-tags`.
   CI ([build-pack.yml](.github/workflows/build-pack.yml)) publishes the `pack` branch and a GitHub Release
   with the `.mrpack`.

Don't set the packwiz pre-launch command on the maintainer's own instance. The working copy is the
source, not a consumer.

To clone it as a fresh dev instance: `git clone` into Prism's instances folder,
`cp instance.cfg.example instance.cfg`, remove the `PreLaunchCommand` line, restart Prism, then use the
packwiz-installer once (or import the release) to fetch the jars.
