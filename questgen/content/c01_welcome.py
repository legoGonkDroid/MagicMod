"""Chapter 1 — Welcome to MagicMod (main path start)."""
from model import Chapter, adv, check, give, item, xp


def build(reg):
    ch = Chapter('welcome', 'Welcome to MagicMod', 'journey', 'ars_nouveau:novice_spell_book',
                 subtitle='Your first steps toward becoming an Archmage.')

    ch.quest('start', 'Welcome, Apprentice', [check()],
             [give('minecraft:bread', 8), give('minecraft:torch', 16), xp(10)],
             icon='ftbquests:book', shape='gear', size=1.5, x=0, y=0,
             subtitle='The Path of the Archmage begins here.',
             desc=['This quest book will guide you from your first spell to the defeat of the Ender Dragon.',
                   '',
                   'Chapters in &6The Journey&r unlock one after another. Chapters in &bCodex & Collections&r are '
                   'open from the start: familiars, bestiary, music discs, relics, exploration and more.',
                   '',
                   'Click the checkmark to begin.'])

    ch.quest('spell_book', 'A Book of Spells', [item('ars_nouveau:novice_spell_book')],
             [give('ars_nouveau:blank_parchment', 4), xp(25)],
             deps=['start'], icon='ars_nouveau:novice_spell_book', x=2.5, y=-1.5,
             desc=['You arrived with a &dNovice Spell Book&r. It is the heart of Ars Nouveau magic.',
                   '',
                   'Hold it and press &eC&r to open the spell crafting screen. Combine a &aForm&r '
                   '(how the spell is cast) with &aEffects&r (what it does).',
                   '',
                   'Lost it? It can be crafted. Check EMI.'])

    ch.quest('emi', 'Looking Things Up', [check()],
             [give('minecraft:book', 2), xp(10)],
             deps=['start'], icon='emi:emi' if reg.has('item', 'emi:emi') else 'minecraft:knowledge_book',
             x=2.5, y=0,
             desc=['The item list on the right side of your inventory is &bEMI&r.',
                   '',
                   '&eR&r on an item shows how to craft it, &eU&r shows what it is used for.',
                   'Look at a block in the world and &bJade&r tells you what it is and which mod adds it.',
                   '',
                   'The vanilla recipe book is disabled outside creative mode. Use EMI instead.'])

    ch.quest('map', 'Mapping the World', [check()],
             [give('minecraft:compass'), xp(10)],
             deps=['start'], icon='minecraft:filled_map', x=2.5, y=1.5,
             desc=["The minimap in the corner is &bXaero's Minimap&r. Press &eM&r for the full world map.",
                   '',
                   'Press &eB&r to create a waypoint. Activated waystones show up on the map automatically.'])

    ch.quest('stone_age', 'Stone and Iron', [adv('minecraft:story/mine_stone'),
                                             adv('minecraft:story/smelt_iron')],
             [give('minecraft:iron_ingot', 4), give('minecraft:coal', 8), xp(25)],
             deps=['spell_book'], icon='minecraft:iron_ingot', x=5, y=-2,
             desc=['Even mages need tools. Mine some stone and smelt your first iron.'])

    ch.quest('bed', 'A Place to Rest', [adv('minecraft:adventure/sleep_in_bed')],
             [give('minecraft:lantern', 2), xp(20)],
             deps=['spell_book'], icon='minecraft:red_bed', x=5, y=-0.5,
             desc=['Sleep in a bed to set your respawn point and skip the night.'])

    ch.quest('food', 'Provisions', [item('minecraft:bread', 8, title='8 Bread')],
             [give('minecraft:wheat_seeds', 16), give('minecraft:carrot', 4), xp(20)],
             deps=['spell_book'], icon='minecraft:bread', x=5, y=1,
             desc=['Gather some food for the road. Farmer\'s Delight adds many more meals later on.',
                   '',
                   'Bread is only checked, not taken.'])

    ch.quest('backpack', 'Pack Your Bags', [item('sophisticatedbackpacks:backpack')],
             [give('sophisticatedbackpacks:upgrade_base', 2), xp(30)],
             deps=['stone_age'], icon='sophisticatedbackpacks:backpack', x=7.5, y=-2,
             desc=['Craft a &bSophisticated Backpack&r. Place it, or open it with the backpack key, for extra '
                   'storage.',
                   '',
                   'Upgrades add auto-pickup, magnets, feeding, and much more.'])

    ch.quest('waystone', 'Waystones', [check(title='Activate a waystone')],
             [give('waystones:warp_dust', 4), give('waystones:return_scroll', 2), xp(30)],
             deps=['map'], icon='waystones:waystone', x=5, y=2.5,
             desc=['Waystones are found in villages and in the wild. Right-click one to activate it, and you '
                   'can teleport between activated waystones for a small cost.',
                   '',
                   'Check this off once you have activated one.'])

    ch.quest('armor_stands', 'Statues and Swaps', [item('minecraft:armor_stand')],
             [give('minecraft:iron_ingot', 2), xp(15)],
             deps=['stone_age'], icon='minecraft:armor_stand', x=7.5, y=-0.5, optional=True,
             desc=['Armor stands are more useful here:',
                   '',
                   '&eSneak + right-click with an empty hand&r opens the &bArmor Statues&r menu to pose and '
                   'equip the stand.',
                   '&eSneak + right-click while holding an item&r swaps your armor with the stand\'s.'])

    ch.quest('ready', 'Ready for Magic', [check()],
             [give('ars_nouveau:source_gem', 4), give('ars_nouveau:blank_parchment', 2), xp(50),
              give('ars_nouveau:glyph_amplify')],
             deps=['backpack', 'bed', 'food', 'waystone'], icon='ars_nouveau:source_gem',
             shape='hexagon', size=1.25, x=10, y=0.5,
             desc=['You have the basics. Now it is time to study magic properly.',
                   '',
                   'Your reward includes a &aGlyph of Amplify&r: right-click it to learn it, then add it after '
                   'an effect to make that effect stronger.',
                   '',
                   'Completing this quest unlocks &6Novice Mage&r.'])
    return ch
