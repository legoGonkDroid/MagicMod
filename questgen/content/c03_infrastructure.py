"""Chapter 3 — Arcane Infrastructure: apparatus, essences, relays, rituals."""
from model import Chapter, adv, check, give, item, xp

ESSENCES = [
    ('air', 'Air', 'minecraft:feather'),
    ('earth', 'Earth', 'minecraft:wheat_seeds'),
    ('fire', 'Fire', 'minecraft:blaze_powder'),
    ('water', 'Water', 'minecraft:kelp'),
    ('abjuration', 'Abjuration', 'minecraft:milk_bucket'),
    ('conjuration', 'Conjuration', 'minecraft:book'),
    ('manipulation', 'Manipulation', 'minecraft:clock'),
]


def build(reg):
    ch = Chapter('infrastructure', 'Arcane Infrastructure', 'journey', 'ars_nouveau:enchanting_apparatus',
                 subtitle='Build a proper workshop.')

    ch.quest('start', 'The Arcane Core', [item('ars_nouveau:arcane_core')],
             [give('ars_nouveau:source_gem', 4), xp(40)],
             deps=['novice/ready'], icon='ars_nouveau:arcane_core', shape='gear', size=1.5,
             desc=['The &dArcane Core&r is the base of the Enchanting Apparatus. Craft one to begin.'])

    ch.quest('pedestals', 'Arcane Pedestals', [item('ars_nouveau:arcane_pedestal', 4, title='4 Arcane Pedestals')],
             [give('minecraft:gold_ingot', 6), xp(30)],
             deps=['start'], icon='ars_nouveau:arcane_pedestal',
             desc=['Pedestals hold the ingredients for apparatus recipes and rituals.'])

    ch.quest('apparatus', 'Enchanting Apparatus', [adv('ars_nouveau:enchanting_apparatus')],
             [give('ars_nouveau:source_gem', 8), give('minecraft:lapis_lazuli', 16), xp(75)],
             deps=['pedestals'], icon='ars_nouveau:enchanting_apparatus',
             desc=['Place the &dEnchanting Apparatus&r on top of the Arcane Core, surround it with '
                   'pedestals and give it source. It crafts most advanced Ars items and can apply '
                   'enchantments.'])

    prev = []
    for slug, name, reward in ESSENCES:
        ch.quest(f'essence_{slug}', f'{name} Essence', [item(f'ars_nouveau:{slug}_essence')],
                 [give(reward, 4 if reward != 'minecraft:milk_bucket' else 1), xp(25)],
                 deps=['apparatus'], icon=f'ars_nouveau:{slug}_essence',
                 desc=[f'Essences are imbued in the Imbuement Chamber. &d{name} Essence&r unlocks '
                       f'{name.lower()} glyphs and items.'])
        prev.append(f'essence_{slug}')

    ch.quest('all_essences', 'Elemental Theory', [check(title='All seven essences studied')],
             [give('ars_nouveau:source_gem_block', 2), xp(100)],
             deps=prev, icon='ars_nouveau:manipulation_essence', shape='diamond',
             desc=['You have handled all seven essences. Every school of magic is now open to you.'])

    ch.quest('relay', 'Source Relays', [item('ars_nouveau:relay', 2, title='2 Relays')],
             [give('ars_nouveau:source_gem', 4), xp(30)],
             deps=['apparatus'], icon='ars_nouveau:relay',
             desc=['&dRelays&r move source between jars over a distance. Link them with a '
                   '&dDominion Wand&r.'])

    ch.quest('dominion_wand', 'Dominion Wand', [item('ars_nouveau:dominion_wand')],
             [give('minecraft:gold_nugget', 9), xp(15)],
             deps=['relay'], icon='ars_nouveau:dominion_wand',
             desc=['Use the Dominion Wand to link relays, turrets and starbuncles to blocks.'])

    ch.quest('relay_splitter', 'Splitting Source', [item('ars_nouveau:relay_splitter')],
             [give('ars_nouveau:source_jar', 2), xp(30)],
             deps=['dominion_wand'], icon='ars_nouveau:relay_splitter', optional=True,
             desc=['A Relay Splitter spreads source evenly to several jars.'])

    ch.quest('alteration', 'Alteration Table', [adv('ars_nouveau:alteration_table')],
             [give('ars_nouveau:blank_thread', 2), xp(40)],
             deps=['apparatus'], icon='ars_nouveau:alteration_table',
             desc=['The &dAlteration Table&r lets you change the perks (threads) on mage armour.'])

    ch.quest('ritual_brazier', 'Ritual Brazier', [adv('ars_nouveau:ritual_brazier')],
             [give('ars_nouveau:source_gem', 8), xp(40)],
             deps=['apparatus'], icon='ars_nouveau:ritual_brazier',
             desc=['Place a ritual tablet on the &dRitual Brazier&r to start a ritual. Some rituals '
                   'take items as augments.'])

    ch.quest('first_ritual', 'A First Ritual', [item('ars_nouveau:ritual_sunrise', key='sunrise')],
             [give('ars_nouveau:magebloom_fiber', 8), xp(30)],
             deps=['ritual_brazier'], icon='ars_nouveau:ritual_sunrise',
             desc=['The &dRitual of Sunrise&r turns night into day. Craft the tablet to complete this.'])

    ch.quest('turret', 'Spell Turret', [adv('ars_nouveau:basic_spell_turret')],
             [give('ars_nouveau:spell_parchment', 2), xp(30)],
             deps=['apparatus'], icon='ars_nouveau:basic_spell_turret', optional=True,
             desc=['Spell turrets cast an inscribed spell when powered by redstone. Great for farms.'])

    ch.quest('potion_jar', 'Potion Jars', [adv('ars_nouveau:potion_jar')],
             [give('minecraft:nether_wart', 8), xp(20)],
             deps=['apparatus'], icon='ars_nouveau:potion_jar', optional=True,
             desc=['Potion Jars hold many doses of a potion. Wixies can brew into them.'])

    ch.quest('storage', 'Arcane Storage', [item('ars_nouveau:storage_lectern'),
                                           item('ars_nouveau:repository')],
             [give('ars_nouveau:repository', 2), xp(40)],
             deps=['apparatus'], icon='ars_nouveau:storage_lectern', optional=True,
             desc=['A &dStorage Lectern&r connected to &dRepositories&r is a simple magical storage '
                   'network.'])

    ch.quest('ready', 'Master of the Workshop', [item('ars_nouveau:source_jar', 4, title='4 Source Jars')],
             [give('ars_nouveau:source_gem_block', 3), give('minecraft:diamond', 2), xp(150)],
             deps=['all_essences', 'dominion_wand', 'alteration', 'first_ritual'],
             icon='ars_nouveau:source_jar', shape='hexagon', size=1.25,
             desc=['A good workshop runs on plenty of stored source.',
                   '',
                   'Completing this quest unlocks &6Apprentice Arcanist&r.'])
    return ch
