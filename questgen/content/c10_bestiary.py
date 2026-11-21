"""Chapter 10 — Bestiary (codex): look at (observe) the pack's magical creatures."""
from model import Chapter, check, give, item, kill, levels, observe, xp

SECTIONS = [
    ('ars', 'Creatures of Ars Nouveau', 'ars_nouveau:starbuncle_charm', [
        'ars_nouveau:starbuncle', 'ars_nouveau:whirlisprig', 'ars_nouveau:drygmy', 'ars_nouveau:wixie',
        'ars_nouveau:bookwyrm', 'ars_nouveau:amethyst_golem', 'ars_nouveau:alakarkinos',
        'ars_nouveau:wilden_hunter', 'ars_nouveau:wilden_stalker', 'ars_nouveau:wilden_guardian',
        'ars_nouveau:blazing_weald_walker', 'ars_nouveau:cascading_weald_walker',
        'ars_nouveau:flourishing_weald_walker', 'ars_nouveau:vexing_weald_walker',
    ], give('ars_nouveau:source_gem_block', 2)),
    ('elemental', 'Creatures of Ars Elemental', 'ars_elemental:siren_charm', [
        'ars_elemental:siren_entity', 'ars_elemental:firenando_entity', 'ars_elemental:flashjack_entity',
        'ars_elemental:flashing_weald_walker', 'ars_elemental:fire_mage', 'ars_elemental:water_mage',
        'ars_elemental:air_mage', 'ars_elemental:earth_mage',
    ], give('ars_elemental:mark_of_mastery')),
    ('quark', 'Curious Critters', 'minecraft:spider_eye', [
        'quark:stoneling', 'quark:toretoise', 'quark:crab', 'quark:foxhound', 'quark:shiba',
        'quark:wraith', 'quark:forgotten',
    ], give('minecraft:name_tag', 3)),
]


def build(reg):
    ch = Chapter('bestiary', 'Bestiary', 'codex', 'minecraft:spyglass',
                 subtitle='Catalogue the strange creatures of this world.')

    ch.quest('start', 'The Bestiary', [check()],
             [give('minecraft:spyglass'), xp(10)],
             icon='minecraft:spyglass', shape='gear', size=1.5, x=0, y=0,
             desc=['Every quest here only asks you to &elook at&r a creature: aim your crosshair at it '
                   'and the task completes. No need to fight anything.',
                   '',
                   'A spyglass helps for creatures far away.'])

    y = -6.0
    capstones = []
    sections = list(SECTIONS)
    fauna = [e for e in reg.find('entity', r'^ars_fauna:') if e != 'ars_fauna:starbuncle_swarm']
    sections.insert(1, ('fauna', 'Ars Fauna', 'ars_nouveau:starbuncle_shards', fauna,
                        give('ars_nouveau:starbuncle_plush')))
    for sec_slug, sec_title, sec_icon, entities, prize in sections:
        slugs = []
        cols = 7
        for i, ent in enumerate(entities):
            slug = sec_slug + '_' + ent.split(':')[1]
            name = reg.name(ent, 'entity') or ent
            ch.quest(slug, name, [observe(ent)], [xp(25)],
                     deps=['start'], x=2 + (i % cols) * 1.25, y=y + (i // cols) * 1.25,
                     icon=sec_icon, size=0.75,
                     desc=[f'Look at a &b{name}&r.'])
            slugs.append(slug)
        rows = (len(entities) + cols - 1) // cols
        ch.quest(sec_slug + '_all', sec_title, [check(title='Every creature observed')],
                 [prize, levels(5)], deps=slugs, icon=sec_icon, shape='diamond', size=1.25,
                 x=2 + cols * 1.25 + 0.75, y=y + (rows - 1) * 0.625,
                 desc=[f'You have seen every creature in &6{sec_title}&r.'])
        capstones.append(sec_slug + '_all')
        y += rows * 1.25 + 1.0

    # Dangerous foes: kill tasks
    foes = [('ars_zero:lich', 'The Lich'), ('ars_zero:necromancer', 'Necromancer'),
            ('harsh_encounters:deviser', 'The Deviser')]
    for i, (ent, title) in enumerate(foes):
        ch.quest('foe_' + ent.split(':')[1], title, [kill(ent)],
                 [give('minecraft:diamond', 3), levels(5)], deps=['start'], shape='octagon',
                 icon='minecraft:wither_skeleton_skull', x=2 + i * 2.0, y=y + 0.5,
                 desc=[f'Defeat &c{title}&r. A dangerous foe found in this pack\'s dungeons.'])

    ch.quest('all', 'Master Naturalist', [check(title='Every bestiary page complete')],
             [give('minecraft:golden_apple', 4), levels(15)],
             deps=capstones, icon='minecraft:writable_book', shape='heart', size=2.0, x=14.5, y=-2,
             subtitle='Collection complete',
             desc=['Every creature catalogued.'])
    return ch
