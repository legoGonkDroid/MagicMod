# MagicMod — FTB Quests questline ("Path of the Archmage")

## Context
MagicMod (NeoForge 1.21.1) now has FTB Quests 2101.1.39, FTB Teams and FTB Library installed, but no quests yet (`minecraft/config/ftbquests/` does not exist). The goal is a large quest book that guides players through the pack (mostly Ars Nouveau and its add-ons, Cataclysm bosses, exploration and colonies) and ends with defeating the Ender Dragon. It should also include many collectible quests: Ars familiars, every music disc, and unique items (relics, trinkets, boss gear).

**Decisions confirmed with the user:**
- **Structure:** one gated main path, chapter by chapter, toward the Dragon. Side chapters (collections, bestiary, exploration, colonies) are open from the start.
- **Rewards:** hand-picked items on each quest, chosen to fit the quest, rather than generic loot crates.
- **Bosses:** all Cataclysm bosses that can be reached before the End, plus the Wilden Chimera, are required before the Dragon.
  - The Ender Guardian is the exception. Its Ruined Citadel only generates in `end_highlands`/`end_midlands`, and its Eye of Void needs shulker shells and purpur from End cities.
  - So it becomes the closing quest right after the Dragon: Dragon → outer islands → Ender Guardian.

## Approach: generate the quest files from a Python script
With about 400 quests, building them by hand in the in-game editor would be slow and error-prone. Instead, a small generator in the repo will write FTB Quests' SNBT files.

The generator:
- **Keeps the quest content readable:** each chapter is a Python file listing its quests, tasks, rewards, text and dependencies.
- **Keeps quest IDs stable:** each ID is derived from a hash of `chapter-slug/quest-slug`, so regenerating the files never resets player progress.
- **Rejects bad IDs:** every item, entity, structure, biome and advancement ID is checked against what's actually in the installed jars, so typos and removed mods fail the build instead of showing as broken quests in game.
- **Lays out quests automatically:** quests are placed on a grid by their dependency depth, with optional manual x/y overrides.

### Files (all new)
- `MagicMod/questgen/` (tracked by git, outside `minecraft/`, so not loaded by the game)
  - `registry.py`: builds the set of valid IDs from `minecraft/mods/*.jar` and the vanilla client jar at `~/.local/share/PrismLauncher/libraries/net/minecraft/client/1.21.1-20240808.144430/client-1.21.1-20240808.144430-extra.jar`. It reads item models and lang files, `entity.*` lang keys, `data/*/worldgen/structure`, biomes and `data/*/advancement`. This is the same jar-scanning approach used earlier in this session.
  - `model.py`: `Chapter`, `Quest`, task helpers (`item`, `kill`, `observe`, `structure`, `biome`, `dimension`, `advancement`, `checkmark`) and reward helpers (`item`, `xp`, `choice`). Also deterministic IDs and automatic layout.
  - `snbt.py`: writes SNBT.
  - `build.py`: entry point. Validates everything, then writes the quest files. Fails on unknown IDs, missing or circular dependencies, and quests without a reward.
  - `content/NN_<chapter>.py`: one file per chapter, holding the quest data.
- Output: `MagicMod/minecraft/config/ftbquests/quests/` → `data.snbt`, `chapter_groups.snbt`, `chapters/*.snbt` and `lang/en_us*` (this version stores quest text in lang files; `TranslationManager`/`langFolder` are present in the jar).
- `.gitignore`: no change needed, since `config/` is already tracked. Player progress lives in `saves/<world>/`, which is already ignored.
- Root `CLAUDE.md`: add a short note on how to regenerate the quests.

### Step 0: confirm the exact file format (before writing the generator)
FTB Quests' SNBT layout for this version (key names, lang file layout, task/reward `type` IDs) needs to be confirmed with a real example. The user creates a sample, then the generator copies its format exactly:
1. In a creative test world, open the quest book, turn on edit mode, and create one chapter with one quest.
2. Give the quest an item task, a kill task, an observation task and an item reward.
3. Save, then share the generated `config/ftbquests/quests/` folder.

The task/reward classes found in the jar are: Item, Kill, Observation, Structure, Biome, Dimension, Location, Advancement, Checkmark, Stat, XP; rewards Item, XP, XPLevels, Choice, Random, Loot, Command, Toast.

## Chapters (~400 quests)

### Group "The Journey" (main path; each chapter unlocks after the previous chapter's final quest)
1. **Welcome to MagicMod** (~12): Novice spell book from the starter kit, Waystones (activate one), Xaero's map, EMI/Jade usage, Sophisticated Backpack, first shelter and food.
2. **Novice Mage** (~20): archwood, source gems, worn notebook, scribes table, first glyphs, imbuement chamber, source jar, sourcelinks. Where Ars Nouveau has a matching advancement (`novice_spell_book`, `source_jar`, `imbuement_chamber`, etc.), the quest uses it.
3. **Arcane Infrastructure** (~18): enchanting apparatus, arcane core and pedestals, relays, alteration table, ritual brazier, one quest per essence type.
4. **Apprentice Arcanist** (~16): apprentice book; sorcerer/arcanist/battlemage armour; threads; Wilden drops; Wilden Tribute → **kill the Wilden Chimera** (`ars_nouveau:wilden_boss`, required).
5. **Into the Nether** (~16): portal, fortress, blaze rods, bastion.
   - **Ignis:** craft Eye of Flame → find the Burning Arena (structure task) → kill Ignis.
   - **Netherite Monstrosity:** craft Eye of Monstrous → find the Soul Blacksmith → kill it.
6. **Ancient Threats** (~20). For each boss: craft its eye → find its structure → kill it.
   - **Harbinger:** Eye of Mech → Ancient Factory.
   - **Ancient Remnant:** Eye of Desert → Cursed Pyramid.
   - **Maledictus:** Eye of Curse → Frosted Prison.
   - **The Leviathan:** Eye of Abyss + Abyssal Sacrifice → Sunken City.
   - **Scylla:** Eye of Storm → Acropolis.
7. **Archmage** (~12): archmage book, top-tier armour, threads and glyphs.
8. **The End** (~14): eyes of ender → stronghold → End.
   - **Kill the Ender Dragon (★ main goal).** This depends on all 7 Cataclysm kills plus the Wilden Chimera.
   - Then the epilogue: End gateway → End city (shulker shells, purpur) → Eye of Void → Ruined Citadel → **Ender Guardian** (closing quest).

### Group "Codex & Collections" (open from the start, ★ marks a completion prize)
9. **Familiars** (~12): Ritual of Binding plus one quest per familiar (9 total).
   - Ars Nouveau's: starbuncle, whirlisprig, drygmy, wixie, bookwyrm, amethyst golem.
   - Ars Elemental's: Flashjack, Siren, Flarecannon.
   - Each task only checks that you have the familiar item and doesn't take it. Each quest's text says to complete it before using the item.
   - ★ all familiars.
10. **Bestiary** (~40): observation tasks (look at the creature) for:
    - Ars creatures: starbuncle, whirlisprig, drygmy, wixie, bookwyrm, amethyst golem, alakarkinos, Wilden types and weald walkers.
    - All 25 Ars Fauna variants (Cavebuncle through Zombuncle, plus the sprigs).
    - Ars Elemental and Ars Zero mobs. The Lich and Necromancer get kill tasks.
11. **Music Discs** (~55): the 19 vanilla 1.21.1 discs plus 35 modded discs:
    - Ars Musique 11, Ars Nouveau 3, Cataclysm 9 (each boss's disc, linked to that boss's quest), Quark 9, Biomes O' Plenty 1, Supplementaries 2.
    - ★ complete collection.
12. **Relics & Treasures** (~95):
    - Relics 25; Reliquified Ars Nouveau 19; Greatest Discount 3; Violetgold set 11.
    - Ars Trinkets' unique items (hearts, crown, top-tier rings and lotuses, about 15).
    - Each Cataclysm boss's signature weapons and armour.
    - ★ for each sub-collection.
13. **Ars Expansions** (~40): Elemental (focuses, elemental armour), Elemancy, Additions, Artillery turrets (tiers 1–3), Ars Zero, Starbunclemania, Ars Delight, Ars Controle, Two-Way Portals, Polymorphia.
14. **Exploration** (~30):
    - Biomes: Archwood Forest plus highlights from Biomes O' Plenty.
    - Structures: Archwood village (Ars Structurize), Ars Structurize sites, Dungeons Arise, Dungeons & Taverns, YUNG's Better Dungeons, Dungeon Crawl.
    - Waystones network milestones.
15. **Colonies** (~20): MineColonies supply camp/ship → town hall → builder → key huts; Archwood Colonies style buildings and the Archwood research.
16. **Homestead** (~20): Farmer's Delight, Sophisticated Storage, Supplementaries, Quark highlights, Immersive Aircraft, Carry On.

**Writing rewards** (each quest's `rewards` list in its chapter file):
- **Materials for the next step:** early quests give what the next quest needs (source gems, magebloom seeds, archwood saplings, blank parchment).
- **Boss quests:** themed gear or consumables, such as potions, threads, an experience gem, or that boss's eye-crafting materials.
- **Collectibles:** small XP plus a fitting item.
- **★ collection prizes:** something distinctive, but nothing that skips main-path progress. For example, never give a spell book above the player's current tier or Cataclysm boss gear.
- **Most quests** also get a small XP reward.

## Implementation order
1. Step 0: get the sample format from the user.
2. Write `registry.py`, `model.py`, `snbt.py` and `build.py`. Generate chapter 1 only, then check it in game.
3. Write chapters 2–8, the main path, including the dependency on all bosses before the Dragon.
4. Write side chapters 9–16. Where a full set is wanted (discs, relics, Ars Fauna), the list is built from the registry by namespace and pattern, so new discs or relics from future mod updates get added automatically.
5. Update the root `CLAUDE.md` with the regeneration command and the stable-ID rule: never rename a quest slug after release, or that quest's progress is lost.

## Verification
- **Build:** `python3 MagicMod/questgen/build.py` exits with 0 errors and reports the number of quests per chapter. A deliberately wrong item ID must fail the build.
- **In game (creative test world, after launching):**
  - The quest book opens.
  - No chapter shows a missing-item icon.
  - `logs/latest.log` has no FTB Quests parse errors.
  - Main-path chapters show as locked in order, and side chapters are open.
- **Test the task types:** in survival, complete chapter 1 normally. Then check one of each:
  - Kill task: summon a Wilden Chimera.
  - Observation task: look at a starbuncle.
  - Structure task: `/locate` and teleport to a Burning Arena.
  - Item task: get a music disc.
- **Test the finale:** fast-forward with FTB Quests' change-progress command to check that the Dragon quest unlocks only after all 8 boss quests are done, and that the Ender Guardian quest follows it.
- **Regeneration:** run `build.py` again after editing a quest's text and confirm in-game progress is kept.
