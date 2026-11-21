"""Chapter 15 — Colonies (codex): MineColonies with the Archwood Colonies style."""
from model import Chapter, adv, check, give, item, levels, xp

M = 'minecolonies:'
HUTS = [  # (advancement, title, icon, reward)
    ('production/build_lumberjack', 'Lumberjack', 'blockhutlumberjack', give('minecraft:iron_axe')),
    ('production/build_miner', 'Miner', 'blockhutminer', give('minecraft:iron_pickaxe')),
    ('production/build_farmer', 'Farmer', 'blockhutfarmer', give('minecraft:wheat_seeds', 32)),
    ('production/build_fisherman', 'Fisherman', 'blockhutfisherman', give('minecraft:fishing_rod')),
    ('production/build_cook', 'Cook', 'blockhutcook', give('minecraft:cooked_beef', 16)),
    ('production/build_warehouse', 'Warehouse', 'blockhutwarehouse', give('minecraft:chest', 8)),
    ('production/build_delivery_person', 'Courier', 'blockhutdeliveryman', give('minecraft:saddle')),
    ('production/build_sawmill', 'Sawmill', 'blockhutsawmill', give('minecraft:oak_log', 32)),
    ('production/build_stonemason', 'Stonemason', 'blockhutstonemason', give('minecraft:stone', 64)),
    ('production/build_smeltery', 'Smeltery', 'blockhutsmeltery', give('minecraft:coal', 32)),
    ('production/build_blacksmith', 'Blacksmith', 'blockhutblacksmith', give('minecraft:iron_ingot', 16)),
    ('production/build_library', 'Library', 'blockhutlibrary', give('minecraft:book', 16)),
    ('production/build_enchanter', 'Enchanter', 'blockhutenchanter', give('minecraft:lapis_lazuli', 32)),
    ('minecolonies/build_tavern', 'Tavern', 'blockhuttavern', give('minecraft:bread', 32)),
    ('minecolonies/build_guard_tower', 'Guard Tower', 'blockhutguardtower', give('minecraft:iron_sword')),
    ('military/build_barracks', 'Barracks', 'blockhutbarracks', give('minecraft:shield', 2)),
    ('minecolonies/build_mysticalsite', 'Mystical Site', 'blockhutmysticalsite', give('ars_nouveau:source_gem_block')),
]


def build(reg):
    ch = Chapter('colonies', 'Colonies', 'codex', M + 'blockhuttownhall',
                 subtitle='Found an Archwood colony with MineColonies.')

    ch.quest('start', 'Supply Camp', [adv(M + 'minecolonies/place_townhall', title='Place a Town Hall')],
             [give('minecraft:oak_log', 32), give('minecraft:bread', 16), xp(50)],
             icon=M + 'supplycampdeployer', shape='gear', size=1.5, x=0, y=0,
             desc=['You started with a &6Supply Camp&r, a &6Town Hall&r and a &6Build Tool&r.',
                   '',
                   'Place the Supply Camp on flat ground (16x17, no grass or flowers). Take the Town Hall '
                   'block from its chest, place it, and name your colony.'])

    ch.quest('archwood_style', 'Archwood Style', [check(title='Pick the Archwood style')],
             [give('ars_nouveau:archwood_planks', 64), xp(30)],
             deps=['start'], icon='ars_nouveau:green_archwood_log', x=0, y=2,
             desc=['When placing huts with the &6Build Tool&r, pick the &dArchwood&r style pack from '
                   '&bArchwood Colonies&r so your colony is built in Archwood designs.',
                   '',
                   'Check this off once you have chosen it.'])

    ch.quest('builder', "Builder's Hut", [adv(M + 'minecolonies/build_builder')],
             [give('minecraft:oak_planks', 64), give('minecraft:cobblestone', 64), xp(60)],
             deps=['start'], icon=M + 'blockhutbuilder', x=2, y=0,
             desc=['Use the &6Build Tool&r to place a Builder\'s Hut, then hire a builder. The builder '
                   'constructs everything else and requests materials through the clipboard.'])

    ch.quest('town_hall', 'Town Hall', [adv(M + 'minecolonies/build_town_hall')],
             [give('minecraft:iron_ingot', 16), xp(80)],
             deps=['builder'], icon=M + 'blockhuttownhall', x=4, y=0,
             desc=['Have your builder construct the Town Hall itself.'])

    ch.quest('clipboard', 'Clipboard', [item(M + 'clipboard')],
             [give('minecraft:paper', 16), xp(20)],
             deps=['builder'], icon=M + 'clipboard', x=4, y=2, optional=True,
             desc=['The clipboard lists every open request from your citizens.'])

    ch.quest('population_5', 'A Small Village', [adv(M + 'minecolonies/colony_population_5')],
             [give('minecraft:red_bed', 2), xp(60)],
             deps=['town_hall'], icon='minecraft:red_bed', x=6, y=-1)
    ch.quest('population_25', 'A Bustling Town', [adv(M + 'minecolonies/colony_population_25')],
             [give('minecraft:emerald', 16), levels(10)],
             deps=['population_5'], icon='minecraft:emerald', x=8, y=-1)
    ch.quest('population_50', 'A Great City', [adv(M + 'minecolonies/colony_population_50')],
             [give('minecraft:emerald_block', 4), levels(15)],
             deps=['population_25'], icon='minecraft:emerald_block', x=10, y=-1)

    hut_slugs = []
    cols = 6
    for i, (a, title, icon, reward) in enumerate(HUTS):
        slug = 'hut_' + a.split('/')[-1].replace('build_', '')
        ch.quest(slug, title, [adv(M + a)], [reward, xp(50)], deps=['town_hall'], icon=M + icon, size=0.85,
                 x=6 + (i % cols) * 1.25, y=1 + (i // cols) * 1.25,
                 desc=[f'Build a &6{title}&r hut.'])
        hut_slugs.append(slug)

    ch.quest('town_hall_5', 'Seat of Power', [adv(M + 'minecolonies/build_town_hall_5')],
             [give('minecraft:diamond_block', 2), levels(20)],
             deps=['population_25'] + hut_slugs, icon=M + 'blockhuttownhall', shape='heart', size=2.0, x=14.5, y=1,
             subtitle='Collection complete',
             desc=['Upgrade the Town Hall to level 5: your colony is complete.'])
    return ch
