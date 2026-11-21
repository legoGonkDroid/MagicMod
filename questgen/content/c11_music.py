"""Chapter 11 — Music Discs (codex): every disc in the pack, built from the registry."""
from model import Chapter, check, give, item, levels, xp

SKIP = {'minecraft:template_music_disc', 'minecraft:music_disc_creator_music_box'}
GROUPS = [
    ('minecraft', 'Vanilla Discs', 'minecraft:jukebox'),
    ('ars_musique', 'Ars Musique', 'ars_musique:bards_bandeau'),
    ('ars_nouveau', 'Ars Nouveau', 'ars_nouveau:music_disc_aria_biblio'),
    ('cataclysm', 'Cataclysm', 'cataclysm:music_disc_the_cataclysmfarer'),
    ('quark', 'Quark', 'quark:music_disc_endermosh'),
    ('*', 'Other Mods', 'minecraft:note_block'),
]


def build(reg):
    ch = Chapter('music', 'Music Discs', 'codex', 'minecraft:music_disc_pigstep',
                 subtitle='Collect every music disc.')

    discs = [d for d in reg.find('item', r':music_disc_') if d not in SKIP]
    known = {g[0] for g in GROUPS if g[0] != '*'}

    ch.quest('start', 'Jukebox', [item('minecraft:jukebox')],
             [give('minecraft:note_block', 4), xp(20)],
             icon='minecraft:jukebox', shape='gear', size=1.5, x=0, y=0,
             desc=['Collect every music disc in the pack. Discs are only checked, never taken.',
                   '',
                   'Vanilla discs drop when a skeleton kills a creeper, or from chests. Boss discs drop '
                   'from Cataclysm bosses. Others are found in dungeon loot.'])

    y = -5.0
    caps = []
    for ns, title, icon in GROUPS:
        group = [d for d in discs if (d.split(':')[0] == ns if ns != '*' else d.split(':')[0] not in known)]
        if not group:
            continue
        slugs = []
        cols = 8
        for i, d in enumerate(group):
            slug = d.replace(':', '_').replace('music_disc_', '')
            ch.quest(slug, reg.name(d) or d, [item(d)], [xp(30)],
                     deps=['start'], icon=d, size=0.75,
                     x=2 + (i % cols) * 1.25, y=y + (i // cols) * 1.25)
            slugs.append(slug)
        rows = (len(group) + cols - 1) // cols
        gslug = 'all_' + (ns if ns != '*' else 'other')
        ch.quest(gslug, title, [check(title=f'All {len(group)} discs')],
                 [give('minecraft:jukebox'), levels(5)], deps=slugs, icon=icon, shape='diamond',
                 size=1.25, x=2 + cols * 1.25 + 0.75, y=y + (rows - 1) * 0.625,
                 desc=[f'Every disc from &6{title}&r.'])
        caps.append(gslug)
        y += rows * 1.25 + 0.75

    ch.quest('all', 'Complete Discography', [check(title=f'All {len(discs)} discs')],
             [give('minecraft:music_disc_pigstep', key='pigstep'), give('minecraft:diamond_block', 2), levels(20)],
             deps=caps, icon='minecraft:music_disc_otherside', shape='heart', size=2.0, x=15, y=0,
             subtitle='Collection complete',
             desc=[f'You own all {len(discs)} music discs in the pack. Have a spare Pigstep.'])
    return ch
