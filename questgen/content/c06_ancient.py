"""Chapter 6 — Ancient Threats: the five Overworld Cataclysm bosses."""
from model import Chapter, check, give, item, kill, levels, potion, structure, xp

# slug, eye item, eye name, structure, structure name, boss entity, boss name, disc, hint, rewards, extra eye item
BOSSES = [
    ('harbinger', 'cataclysm:mech_eye', 'Eye of Mech', 'cataclysm:ancient_factory', 'Ancient Factory',
     'cataclysm:the_harbinger', 'The Harbinger', 'cataclysm:music_disc_the_harbinger',
     'A wither-like war machine buried underground. It fires missiles and lasers; fight it in the open '
     'chamber and keep moving.',
     [give('minecraft:netherite_ingot'), give('minecraft:enchanted_golden_apple'), levels(10)]),
    ('remnant', 'cataclysm:desert_eye', 'Eye of Desert', 'cataclysm:cursed_pyramid', 'Cursed Pyramid',
     'cataclysm:ancient_remnant', 'Ancient Remnant', 'cataclysm:music_disc_ancient_remnant',
     'A giant skeletal beast awakened by sandstorms. Watch for its charge and the earthquake slam.',
     [give('minecraft:diamond_block'), give('minecraft:enchanted_golden_apple'), levels(10)]),
    ('maledictus', 'cataclysm:cursed_eye', 'Eye of Curse', 'cataclysm:frosted_prison', 'Frosted Prison',
     'cataclysm:maledictus', 'Maledictus', 'cataclysm:music_disc_maledictus',
     'A cursed warrior spirit in a frozen prison. It leaps and rains phantom halberds; dodge sideways.',
     [give('minecraft:totem_of_undying'), give('minecraft:enchanted_golden_apple'), levels(10)]),
    ('leviathan', 'cataclysm:abyss_eye', 'Eye of Abyss', 'cataclysm:sunken_city', 'Sunken City',
     'cataclysm:the_leviathan', 'The Leviathan', 'cataclysm:music_disc_the_leviathan',
     'Summon it at the Altar of Abyss with an &6Abyssal Sacrifice&r. Fought underwater: bring water '
     'breathing, night vision and a ranged spell.',
     [give('minecraft:heart_of_the_sea'), give('minecraft:enchanted_golden_apple'), levels(10)]),
    ('scylla', 'cataclysm:storm_eye', 'Eye of Storm', 'cataclysm:acropolis', 'Acropolis',
     'cataclysm:scylla', 'Scylla', 'cataclysm:music_disc_scylla',
     'A storm goddess atop a sunken acropolis. She throws lightning spears; never stand still.',
     [give('minecraft:trident'), give('minecraft:enchanted_golden_apple'), levels(10)]),
]


def build(reg):
    ch = Chapter('ancient', 'Ancient Threats', 'journey', 'cataclysm:mech_eye',
                 subtitle='Five ancient horrors guard the way to the End.')

    ch.quest('start', 'Ancient Threats', [check()],
             [potion('long_regeneration', 2), potion('strong_healing', 4, 'minecraft:splash_potion'), xp(50)],
             deps=['nether/ready'], icon='cataclysm:ancient_metal_ingot', shape='gear', size=1.5, x=0, y=0,
             desc=['Five bosses from &cL_Ender\'s Cataclysm&r slumber in the Overworld. All of them '
                   'must fall before you may face the Ender Dragon.',
                   '',
                   'Each needs its own &6Eye&r: obtain it (check EMI with &eR&r), throw it to find the '
                   'structure, then defeat the boss. They can be done in any order.'])

    kills = []
    for row, (slug, eye, eye_name, struct, struct_name, boss, boss_name, disc, hint, rewards) in enumerate(BOSSES):
        y = (row - 2) * 2.0
        ch.quest(f'{slug}_eye', eye_name, [item(eye)],
                 [give('minecraft:ender_pearl', 2), xp(60)],
                 deps=['start'], icon=eye, x=2.5, y=y,
                 desc=[f'Obtain an &6{eye_name}&r. Throw it to point toward the {struct_name}.'])
        ch.quest(f'{slug}_structure', struct_name, [structure(struct)],
                 [give('minecraft:golden_apple', 2), xp(60)],
                 deps=[f'{slug}_eye'], icon=eye, x=4.5, y=y,
                 desc=[f'Find the &c{struct_name}&r.'])
        ch.quest(slug, boss_name, [kill(boss)], rewards,
                 deps=[f'{slug}_structure'], icon=disc, x=6.5, y=y, shape='octagon', size=1.5,
                 subtitle='Boss', desc=[hint])
        kills.append(slug)

    ch.quest('leviathan_sacrifice', 'Abyssal Sacrifice', [item('cataclysm:abyssal_sacrifice')],
             [potion('long_water_breathing', 2), potion('long_night_vision', 2), xp(60)],
             deps=['leviathan_structure'], icon='cataclysm:abyssal_sacrifice', x=5.5, y=3.0,
             desc=['The Leviathan is summoned with an &6Abyssal Sacrifice&r at the Altar of Abyss.'])
    # Leviathan kill also needs the sacrifice
    for q in ch.quests:
        if q.slug == 'leviathan':
            q.deps.append('leviathan_sacrifice')

    ch.quest('cataclysmfarer', 'The Cataclysmfarer', [item('cataclysm:music_disc_the_cataclysmfarer')],
             [give('minecraft:jukebox'), xp(50)],
             deps=['start'], icon='cataclysm:music_disc_the_cataclysmfarer', x=0, y=2.5, optional=True,
             desc=['A rare disc found in Cataclysm structures. Part of the &bMusic Discs&r collection.'])

    ch.quest('ready', 'Ancient Threats Ended', [check()],
             [give('minecraft:diamond_block', 2), give('ars_nouveau:source_gem_block', 4), levels(15)],
             deps=kills, icon='cataclysm:ancient_metal_ingot', shape='hexagon', size=1.5, x=9, y=0,
             desc=['All five ancient bosses are defeated.',
                   '',
                   'Completing this quest unlocks &6Archmage&r.'])
    return ch
