"""Chapter 14 — Exploration (codex): biomes, structures and travel."""
from model import Chapter, adv, biome, check, give, item, levels, structure, xp

BIOMES = [
    'ars_nouveau:archwood_forest', 'ars_elemental:blazing_forest', 'ars_elemental:cascading_forest',
    'ars_elemental:flashing_forest', 'ars_elemental:flourishing_forest', 'ars_elemental:vexing_caves',
    'ars_zero:blight_forest', 'quark:glimmering_weald',
    'biomesoplenty:mystic_grove', 'biomesoplenty:redwood_forest', 'biomesoplenty:lavender_field',
    'biomesoplenty:jacaranda_glade', 'biomesoplenty:snowblossom_grove', 'biomesoplenty:auroral_garden',
    'biomesoplenty:origin_valley', 'biomesoplenty:volcano', 'biomesoplenty:crystalline_chasm',
    'biomesoplenty:glowing_grotto', 'biomesoplenty:ominous_woods', 'biomesoplenty:tropics',
]

# (slug, title, task, icon)
STRUCTURES = [
    ('archwood_village', 'Archwood Village', structure('ars_structurize:archwoodvillage'), 'ars_nouveau:archwood_planks'),
    ('wixie_hut', 'Wixie Hut', structure('ars_structurize:wixie_hut'), 'ars_nouveau:wixie_charm'),
    ('bookwyrm_library', 'Bookwyrm Library', structure('ars_structurize:bookwrym_library'), 'ars_nouveau:bookwyrm_charm'),
    ('drygmy_pens', 'Drygmy Pens', structure('ars_structurize:drygmy_pens'), 'ars_nouveau:drygmy_charm'),
    ('golem_geode', 'Golem Geode', structure('ars_structurize:golem_geode'), 'ars_nouveau:amethyst_golem_charm'),
    ('whirlisprig_clearing', 'Whirlisprig Clearing', structure('ars_structurize:whirlsprig_clearing'), 'ars_nouveau:whirlisprig_charm'),
    ('starbuncle_shrine', 'Starbuncle Shrine', structure('ars_elemental:starbuncle_shrine'), 'ars_nouveau:starbuncle_charm'),
    ('wilden_den', 'Wilden Den', structure('ars_nouveau:hunter_wilden_den'), 'ars_nouveau:wilden_horn'),
    ('arcane_library', 'Arcane Library', structure('ars_additions:arcane_library'), 'minecraft:bookshelf'),
    ('nexus_tower', 'Nexus Tower', structure('ars_additions:nexus_tower'), 'ars_additions:warp_nexus'),
    ('dungeon_crawl', 'Dungeon Crawl', structure('dungeoncrawl:dungeon'), 'minecraft:mossy_stone_bricks'),
    ('better_dungeons', 'All Better Dungeons', adv('betterdungeons:all_dungeons'), 'minecraft:spawner'),
    ('thunderous_tower', 'Thunderous Tower', structure('harsh_encounters:thunderous_tower'), 'harsh_encounters:thunderium'),
    ('tavern', 'A Warm Tavern', adv('nova_structures:adventure/find_tavern'), 'minecraft:barrel'),
    ('illager_structures', 'Illager Hunter', adv('nova_structures:adventure/find_all_illager_structures'), 'minecraft:crossbow'),
    ('nova_minibosses', 'Shrine Champion', adv('nova_structures:adventure/kill_all_minibosses'), 'minecraft:iron_sword'),
    ('coliseum', 'Coliseum', adv('dungeons_arise:find_coliseum'), 'minecraft:chiseled_stone_bricks'),
    ('typhon', 'Typhon', adv('dungeons_arise:find_typhon'), 'minecraft:prismarine'),
    ('keep_kayra', 'Keep Kayra', adv('dungeons_arise:find_keep_kayra'), 'minecraft:stone_bricks'),
    ('shiraz_palace', 'Shiraz Palace', adv('dungeons_arise:find_shiraz_palace'), 'minecraft:smooth_sandstone'),
    ('mechanical_nest', 'Mechanical Nest', adv('dungeons_arise:find_mechanical_nest'), 'minecraft:cobweb'),
    ('heavenly', 'Heavenly Conqueror', adv('dungeons_arise:find_heavenly_conqueror'), 'minecraft:feather'),
    ('pirate_ship', 'Undead Pirate Ship', adv('dungeons_arise:find_undead_pirate_ship'), 'minecraft:oak_boat'),
    ('bop_village', 'Mystic Village', structure('bopvillage:village_mystic'), 'biomesoplenty:magic_planks'),
]


def build(reg):
    ch = Chapter('exploration', 'Exploration', 'codex', 'minecraft:compass',
                 subtitle='See the world: biomes, dungeons, and wonders.')

    ch.quest('start', 'Wanderlust', [check()],
             [give('minecraft:map', 4), give('minecraft:cooked_beef', 16), xp(10)],
             icon='minecraft:compass', shape='gear', size=1.5, x=0, y=0,
             desc=['The world is full of new biomes and structures. Xaero\'s World Map (&eM&r) keeps '
                   'track of where you have been; waystones help you get back.'])

    # waystone network row
    ch.quest('waystone_warp_stone', 'Warp Stone', [item('waystones:warp_stone')],
             [give('waystones:warp_dust', 8), xp(40)], deps=['start'], icon='waystones:warp_stone', x=2, y=-7.5,
             desc=['A reusable item that teleports you to any activated waystone.'])
    ch.quest('waystone_sharestone', 'Sharestone', [item('waystones:sharestone')],
             [give('waystones:warp_dust', 8), xp(40)], deps=['waystone_warp_stone'], icon='waystones:sharestone',
             x=3.75, y=-7.5, desc=['Sharestones of the same colour link to each other for everyone.'])
    ch.quest('waystone_warp_plate', 'Warp Plate', [item('waystones:warp_plate')],
             [give('waystones:warp_dust', 8), xp(40)], deps=['waystone_sharestone'], icon='waystones:warp_plate',
             x=5.5, y=-7.5, desc=['Warp plates send anything standing on them to a paired plate.'])
    ch.quest('aircraft', 'Take to the Skies', [item('immersive_aircraft:biplane')],
             [give('minecraft:coal_block', 4), xp(75)], deps=['start'], icon='immersive_aircraft:biplane',
             x=7.5, y=-7.5, desc=['&bImmersive Aircraft&r lets you build planes and airships. A biplane '
                                  'is the classic first aircraft.'])
    ch.quest('lootr', 'Lootr', [adv('lootr:10loot')],
             [give('minecraft:chest', 4), xp(40)], deps=['start'], icon='lootr:lootr_chest', x=9.25, y=-7.5,
             desc=['Loot chests in this pack are per-player (&bLootr&r). Open 10 of them.'])

    # biomes
    cols = 10
    bslugs = []
    for i, b in enumerate(BIOMES):
        slug = 'biome_' + b.split(':')[1]
        title = reg.name(b, 'biome') or b.split(':')[1].replace('_', ' ').title()
        ch.quest(slug, title, [biome(b)], [xp(30)], deps=['start'], icon='minecraft:grass_block', size=0.75,
                 x=2 + (i % cols) * 1.25, y=-5.5 + (i // cols) * 1.25, desc=[f'Visit a &a{title}&r biome.'])
        bslugs.append(slug)
    ch.quest('biomes_all', 'Globetrotter', [check(title='Every biome visited')],
             [give('minecraft:filled_map'), give('biomesoplenty:jacaranda_sapling', 4), levels(10)],
             deps=bslugs, icon='minecraft:filled_map', shape='diamond', size=1.25, x=2 + cols * 1.25 + 0.75, y=-4.875,
             desc=['You have seen every biome on the list.'])
    ch.quest('adventuring_time', 'Adventuring Time', [adv('minecraft:adventure/adventuring_time')],
             [give('minecraft:diamond_boots'), levels(20)], deps=['biomes_all'], icon='minecraft:diamond_boots',
             x=2 + cols * 1.25 + 2.5, y=-4.875, optional=True,
             desc=['The vanilla challenge: visit every Overworld biome.'])

    # structures
    sslugs = []
    for i, (slug, title, task, icon) in enumerate(STRUCTURES):
        ch.quest('struct_' + slug, title, [task], [give('minecraft:golden_apple'), xp(60)], deps=['start'],
                 icon=icon, size=0.85, x=2 + (i % cols) * 1.25, y=-1.5 + (i // cols) * 1.25,
                 desc=[f'Find the &6{title}&r. Use a Wayfinder (Ars Additions) or explore.'])
        sslugs.append('struct_' + slug)
    rows = (len(STRUCTURES) + cols - 1) // cols
    ch.quest('structures_all', 'Cartographer', [check(title='Every structure found')],
             [give('minecraft:diamond', 8), give('ars_nouveau:source_gem_block', 2), levels(15)],
             deps=sslugs, icon='minecraft:cartography_table', shape='diamond', size=1.25,
             x=2 + cols * 1.25 + 0.75, y=-1.5 + (rows - 1) * 0.625,
             desc=['You have found every notable structure on the list.'])

    ch.quest('all', 'World Explorer', [check(title='Exploration complete')],
             [give('minecraft:elytra'), levels(20)],
             deps=['biomes_all', 'structures_all', 'waystone_warp_plate'],
             icon='minecraft:elytra', shape='heart', size=2.0, x=18, y=-3,
             subtitle='Collection complete', desc=['There is little left that you haven\'t seen.'])
    return ch
