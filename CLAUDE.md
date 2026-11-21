# MagicMod — instance + git repo

This folder is both the live Prism instance and the pack's git repo (remote: `jarroyer/MagicMod`). The layout follows AllTheMods/ATM-10: only the pack definition is tracked. See `README.md` for details.

- **Mod jars are not committed.** Each mod is tracked through the packwiz-format metadata Prism writes to `minecraft/mods/.index/<slug>.pw.toml`. Add or update mods **through Prism's mod browser** so that file exists. A hand-dropped jar is silently missing for everyone else. Jars with no `.pw.toml` (check with `comm` against the `filename =` lines) have to be fixed before release.
- `instance.cfg` is ignored (Prism rewrites it, and it holds the Java path and playtime). `instance.cfg.example` is the shareable version and includes the packwiz `PreLaunchCommand` for friends. Never set that command on this working copy.
- `mmc-pack.json` is tracked: it holds the MC and NeoForge versions. `tools/build_pack.py` reads them from there.
- Release flow: commit → write `changelogs/vX.Y.Z.md` → `git tag vX.Y.Z && git push --follow-tags`. `.github/workflows/build-pack.yml` runs `tools/build_pack.py`, which copies the overrides and flattens `.index/*.pw.toml` → `mods/` (packwiz-installer installs jars next to their metafile, so Prism's `.index/` layout can't be served as-is). It then runs `packwiz refresh`, force-pushes `build/pack/` to the `pack` branch, and attaches the CurseForge zip to a GitHub Release. All mods are CurseForge-sourced (no .mrpack). Mods whose authors block third-party downloads (Archwood Colonies, Ars Nouveau: Chapters) have hand-written `.pw.toml` files in `metadata:curseforge` mode, so launchers prompt players to download them by hand. Keep the README table of manual downloads in sync.
- When adding new game-dir folders that belong in the pack, update both `.gitignore` and `OVERRIDE_DIRS` in `tools/build_pack.py`.
- Saves were backed up to `~/Backups/MagicMod-saves-*.tar.gz` before the repo was set up.
