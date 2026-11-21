"""Chapter 9 — Familiars (codex): Ritual of Binding + every familiar item."""
from model import Chapter, adv, check, give, item, levels, xp

# familiar item, title, charm (the creature you bind), reward
FAMILIARS = [
    ('ars_nouveau:familiar_starbuncle', 'Starbuncle', 'ars_nouveau:starbuncle_charm',
     give('minecraft:golden_carrot', 16)),
    ('ars_nouveau:familiar_whirlisprig', 'Whirlisprig', 'ars_nouveau:whirlisprig_charm',
     give('minecraft:sweet_berries', 16)),
    ('ars_nouveau:familiar_drygmy', 'Drygmy', 'ars_nouveau:drygmy_charm',
     give('minecraft:leather', 16)),
    ('ars_nouveau:familiar_wixie', 'Wixie', 'ars_nouveau:wixie_charm',
     give('minecraft:nether_wart', 16)),
    ('ars_nouveau:familiar_bookwyrm', 'Bookwyrm', 'ars_nouveau:bookwyrm_charm',
     give('minecraft:book', 8)),
    ('ars_nouveau:familiar_amethyst_golem', 'Amethyst Golem', 'ars_nouveau:amethyst_golem_charm',
     give('minecraft:amethyst_block', 8)),
    ('ars_elemental:firenando_familiar', 'Flarecannon', 'ars_elemental:firenando_charm',
     give('minecraft:magma_block', 8)),
    ('ars_elemental:flashjack_familiar', 'Flashjack', 'ars_elemental:flashjack_charm',
     give('minecraft:feather', 16)),
    ('ars_elemental:siren_familiar', 'Siren', 'ars_elemental:siren_charm',
     give('minecraft:prismarine_crystals', 8)),
]


def build(reg):
    ch = Chapter('familiars', 'Familiars', 'codex', 'ars_nouveau:familiar_starbuncle',
                 subtitle='Bind a companion from every magical species.')

    ch.quest('start', 'Ritual of Binding', [item('ars_nouveau:ritual_binding')],
             [give('ars_nouveau:source_gem', 8), xp(50)],
             icon='ars_nouveau:ritual_binding', shape='gear', size=1.5, x=0, y=0,
             desc=['Familiars are small companions that follow you and grant bonuses. Only one can be '
                   'summoned at a time.',
                   '',
                   'To get one: summon the creature (usually from its &dcharm&r), then run the &dRitual '
                   'of Binding&r next to it. The ritual turns it into a familiar item.',
                   '',
                   'Familiar quests only check that you have the item, so it is never taken. Complete '
                   'the quest before you use the item, because using it binds it to you.'])

    ch.quest('first', 'A Loyal Companion', [adv('ars_nouveau:familiar')],
             [give('minecraft:cake'), xp(50)],
             deps=['start'], icon='minecraft:lead', x=0, y=2.5, optional=True,
             desc=['Summon your first familiar.'])

    ids = []
    for i, (fam, title, charm, reward) in enumerate(FAMILIARS):
        slug = fam.split(':')[1].replace('familiar_', '').replace('_familiar', '')
        col, row = i % 3, i // 3
        ch.quest(slug, f'{title} Familiar', [item(fam)], [reward, xp(75)],
                 deps=['start'], icon=fam, x=2.5 + col * 1.75, y=(row - 1) * 1.75,
                 desc=[f'Bind a &d{title}&r. Summon one from its &6{reg.name(charm) or charm}&r first.',
                       '', 'Each familiar grants a different bonus; see the Worn Notebook.'])
        ids.append(slug)

    ch.quest('all', 'Menagerie', [check(title='Every familiar collected')],
             [give('ars_nouveau:starbuncle_plush'), give('ars_nouveau:source_gem_block', 4), levels(10)],
             deps=ids, icon='ars_nouveau:starbuncle_plush', shape='heart', size=2.0, x=9, y=0,
             subtitle='Collection complete',
             desc=['You have bound every kind of familiar. Here is a plush to remember them by.'])
    return ch
