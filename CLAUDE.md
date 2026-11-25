# MagicMod — instance + git repo

This folder is both the live Prism instance and the pack's git repo
(remote: `git@github.com:legoGonkDroid/MagicMod.git`; the GitHub account was renamed from `jarroyer`, and old
`jarroyer/MagicMod` URLs in `README.md` / `instance.cfg.example` still redirect). The layout follows AllTheMods/ATM-10:
only the pack definition is tracked. See `README.md` for the player-facing install guide.

This file is the self-contained handoff for working on the pack from any machine. The parent folder
`~/Projects/minecraft` is the workspace repo `legoGonkDroid/minecraft-dev`: its `scripts/workspace.py clone` checks
this repo out (branch from its `structure.json`) next to our mods and the reference source of our dependencies.

## Pack at a glance
- Minecraft **1.21.1**, NeoForge **21.1.267**, Java 21 (Prism-managed runtime `java-runtime-delta`).
- Magic pack: Ars Nouveau 5.13.5 and ~30 addons (Additions, Elemental, Zero, Trinkets, Affinity, Caelum, Fauna,
  Deco, Structurize, ...), L_Ender's Cataclysm bosses, MineColonies + Structurize + Archwood Colonies,
  Waystones, Xaero's Minimap/World Map, EMI (+ JEI), Jade, Sodium/Embeddium, Curios, Relics + Reliquified Ars Nouveau,
  FTB Quests (generated book), KubeJS, Starter Kit.
- Our own mods also run in this instance (see "Our dev mods" below).

## Setting up on a new machine
1. Install Prism Launcher. Optional but used here: set `InstanceDir=<...>/Projects/minecraft/prism-instances` in
   `~/.local/share/PrismLauncher/prismlauncher.cfg` so the instances folder lives next to `mods/`.
2. Clone the workspace (`git clone git@github.com:legoGonkDroid/minecraft-dev.git ~/Projects/minecraft`) and run
   `scripts/workspace.py clone`; it clones this repo into `prism-instances/MagicMod` on the working branch.
3. `cp instance.cfg.example instance.cfg` and **delete the `PreLaunchCommand` / `OverrideCommands` lines** (this
   copy is the source, not a packwiz consumer). Restart Prism.
4. Fetch the jars once: import the latest release zip into a throwaway instance and copy its `minecraft/mods/*.jar`
   over, or temporarily run packwiz-installer against the `pack` branch. Archwood Colonies and Ars Nouveau: Chapters
   must be downloaded by hand (see README table).
5. Build and copy in our dev mods (`ars_kingdom`, `ars_resources`) — they have no `.pw.toml`, so nothing fetches them.
6. Launch once so Prism downloads the vanilla client jar (questgen needs it, see below).
7. Worlds (`minecraft/saves/`) are not in git. Copy them from the old machine if wanted; old backups were made to
   `~/Backups/MagicMod-saves-*.tar.gz`. Never delete a save without asking.

Tools used: `git`, `python3` (3.12), Prism. `packwiz` and `gh` are only needed in CI (not installed locally).

## Rules for the repo
- **Mod jars are not committed.** Each mod is tracked through the packwiz-format metadata Prism writes to
  `minecraft/mods/.index/<slug>.pw.toml`. Add or update mods **through Prism's mod browser** so that file exists. A
  hand-dropped jar is silently missing for everyone else. `python3 tools/build_pack.py --check` lists jars without
  metadata; fix them before a release (our two dev jars are the known, expected exceptions until they're published).
- `instance.cfg` is ignored (Prism rewrites it, and it holds the Java path and playtime). `instance.cfg.example` is
  the shareable version and includes the packwiz `PreLaunchCommand` for friends. Never set that command on this
  working copy.
- `mmc-pack.json` is tracked: it holds the MC and NeoForge versions. `tools/build_pack.py` reads them from there.
  Close Prism before editing it or `instance.cfg`; Prism rewrites both (it also adds noise like `cachedVolatile`).
- When adding new game-dir folders that belong in the pack, update both `.gitignore` and `OVERRIDE_DIRS` in
  `tools/build_pack.py`.
- Crash debugging: `minecraft/logs/latest.log`, `minecraft/crash-reports/`.

## Release flow
commit → write `changelogs/vX.Y.Z.md` (and `CHANGELOG.md`) → `git tag vX.Y.Z && git push --follow-tags`.
`.github/workflows/build-pack.yml` runs `tools/build_pack.py`, which copies the overrides and flattens
`.index/*.pw.toml` → `mods/` (packwiz-installer installs jars next to their metafile, so Prism's `.index/` layout can't
be served as-is). It then runs `packwiz refresh`, force-pushes `build/pack/` to the `pack` branch, and attaches the
CurseForge zip to a GitHub Release. All mods are CurseForge-sourced (no .mrpack). Mods whose authors block third-party
downloads (Archwood Colonies, Ars Nouveau: Chapters) have hand-written `.pw.toml` files in `metadata:curseforge` mode,
so launchers prompt players to download them by hand. Keep the README table of manual downloads in sync.

## Our dev mods in this instance
Source lives in `~/Projects/minecraft/mods/` (separate repos):
- `ars_kingdom` — `legoGonkDroid/ArsKingdom` (in development; see its `CLAUDE.md` and `PLAN.md`).
- `ars_resources` — `legoGonkDroid/ArsReSources` (released on CurseForge as `ars-resources`).

To test: `./gradlew build` in the mod repo, then copy `build/libs/<mod>-1.21.1-<version>.jar` into
`minecraft/mods/` (replace the old jar). They are hand-dropped (no `.pw.toml`), so they don't ship with the pack.
Before a pack release, either add them through Prism's CurseForge browser (once published) or remove the jars.
`minecraft/config/jei/client/recipe-category-sort-order.ini` picks up `ars_kingdom:arcanist` while the dev jar is in.

## Custom content
### Datapacks (`minecraft/datapacks/`)
Not auto-loaded (no global datapack mod); add per world. `archwood_village_waystones` adds a waystone piece to Ars
Structurize Archwood villages (Waystones only auto-injects into pools ending in `/houses`).

### KubeJS (2101.7.x on the bundled Rhino 2101.2.8) — `minecraft/kubejs/startup_scripts/`
- `armor_statues_menu.js`: empty-hand sneak+right-click on an armor stand opens Armor Statues' menu (calls
  `fuzs.armorstatues.handler.ArmorStandInteractHandler.onUseEntityAt` at HIGHEST priority and cancels the click,
  because Armor Quick Swap uses the same click and otherwise wins). Sneak+right-click holding an item is left to
  Armor Quick Swap.
- `hide_recipe_book.js` (client): removes the vanilla recipe-book button and keeps the book closed unless in creative
  (EMI is the recipe viewer).
- `hide_ars_trinkets_changelog.js`: suppresses Ars Trinkets' once-per-version login chat message (no config toggle;
  marks `PlayerPersisted.ars_trinkets_changelog_seen` at HIGHEST priority before the mod checks).
- `domum_item_colors.js` (client): fixes Domum Ornamentum inventory icons ignoring their materials. Continuity's
  emissive wrapper (needed for Ars Lumos/Elemental/Supplementaries glow) makes Sodium's FRAPI item path skip NeoForge
  `getRenderPasses`, so at LOWEST-priority `ModelEvent.ModifyBakingResult` it unwraps `EmissiveBakedModel` from
  `domum_ornamentum:*#inventory` models only. Load that Continuity class **inside** the handler, never at script top
  level: early loading initialises Continuity's `RenderUtil` with a null ModelManager → NPE on the first resource
  reload and a startup hang.

Startup scripts need a full game restart after edits. Rhino/KubeJS quirks:
- use `var` in functions and inside any `{}` block (even a top-level `if`); `const`/`let` there throws
  "redeclaration of var";
- `$`-prefix class handles; no template strings or destructuring;
- KubeJS blocks `getClass()` on Java objects (use `instanceof` a loaded class);
- the class filter blocks `Java.loadClass('net.neoforged.fml.ModList')`: use `Platform.isLoaded(id)`,
  `Platform.getInfo(id).getVersion()`;
- wrap NativeEvents handlers in try/catch: an uncaught error in a screen/client event crashes the game.

### Starter Kit
Gives an Ars Nouveau novice spell book, worn tier 1 Arcanist armour (hood/robes/leggings/boots), the Structurize
Build Tool (`structurize:sceptergold`), a MineColonies Supply Camp and Town Hall on first join:
`minecraft/config/serilum/starterkit/kits/Novice_Mage.txt`. The real config dir is `config/serilum/starterkit/`
(settings in `config/serilum/starterkit.json`). Every `.txt` in `kits/` is an active kit and multiple active kits are
handed out at random, so the generated `Default` kit is parked in `kits/inactive/`. Format: `'head'/'chest'/'legs'/
'feet'/'offhand'` lines, slot lines `0`–`35`, then `'effects'`.

### Removed on purpose (don't re-add)
- Curious Armor Stands and all curio-swapping: armor stands have no curio support (user request).
- Reliquified L_Ender's Cataclysm: its newest release (0.1.1) targets Relics 0.10/0.11 and crashes on Relics 0.12+
  (`IRelicItem` moved to `it.hurts.sskirillss.relics.api.relics`), while Reliquified Ars Nouveau 0.8.2 needs Relics ≥0.12.3.

## Quest book (FTB Quests) — generated, never edited in game
- `python3 questgen/build.py` (`--check` = validate only) writes `minecraft/config/ftbquests/quests/`
  (`chapter_groups.snbt`, `chapters/*.snbt`, `lang/en_us.snbt`; `data.snbt` only if missing). It deletes chapter
  files it didn't generate, so in-game edits are overwritten.
- Content: `questgen/content/cNN_*.py`, each exposes `build(reg) -> Chapter`; file order = chapter order.
- Validation: every item/entity/structure/biome/advancement ID is checked against the installed jars
  (`registry.py`, cached in `questgen/.cache/`) — so the jars must be present. It also reads the vanilla client jar
  from `~/.local/share/PrismLauncher/libraries/net/minecraft/client/1.21.1-20240808.144430/` (hard-coded in
  `registry.py`; launch the instance once on a new machine). Fails on unknown IDs, missing deps, cycles, or quests
  without rewards.
- Quest/task/reward IDs are hashes of slugs (`model.make_id`): **never rename a chapter or quest slug** once players
  have progress, or that progress is lost.
- Chapters 01–08 group *The Journey* (welcome → novice → infrastructure → apprentice [Wilden Chimera] → nether
  [Ignis, Netherite Monstrosity] → ancient [Harbinger, Remnant, Maledictus, Leviathan, Scylla] → archmage → end
  [Dragon, then Ender Guardian]); each chapter's `start` depends on the previous chapter's `ready`, and `end/dragon`
  lists every boss in `REQUIRED_BOSSES`. 09–16 group *Codex & Collections* (familiars, bestiary, music [discs
  auto-listed from the registry], relics, expansions, exploration, colonies, homestead), no gating.
- Format gotchas: observation tasks need `observe_type: 5` (ENTITY_TYPE ordinal; it overrides `observation_type` on
  load); potion rewards use `model.potion()` (item components).
- Design and decisions: `questgen/PLAN.md` (main path ends at the Ender Dragon, gated behind all Overworld/Nether
  Cataclysm bosses + Wilden Chimera; Ender Guardian is the post-Dragon closing quest; rewards are hand-picked items
  per quest).

## Current state (update this section whenever you stop working)
_Last updated 2026-11-25._
- Branches: `main` (released state) and `integration` (working branch, one commit ahead: "Save point"). Work on
  `integration`; merge to `main` before tagging a release.
- No release tag has been pushed yet.
- Uncommitted at handoff: Prism noise in `mmc-pack.json` (`cachedVolatile`) and the JEI sort-order line for the
  `ars_kingdom` dev jar — both harmless.
- Next up: nothing pending in the pack itself; most active work is Ars Kingdom (tested in this instance).
