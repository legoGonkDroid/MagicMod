"""Chapter 13 — Ars Expansions (codex): one branch per Ars add-on."""
from model import Chapter, adv, check, give, item, kill, levels, structure, xp

ELEMENTS = [('fire', 'fire'), ('water', 'aqua'), ('air', 'air'), ('earth', 'earth')]  # (school, armour prefix)
ELEMANCY = ['cinder', 'lava', 'mire', 'silt', 'tempest', 'vapor']


def build(reg):
    ch = Chapter('expansions', 'Ars Expansions', 'codex', 'ars_elemental:fire_focus',
                 subtitle='The many add-ons to Ars Nouveau.')

    ch.quest('start', 'Beyond Ars Nouveau', [check()],
             [give('ars_nouveau:source_gem', 4), xp(10)],
             icon='ars_nouveau:annotated_codex', shape='gear', size=1.5, x=0, y=0,
             desc=['This pack has many Ars Nouveau add-ons. Each row here explores one of them. Most '
                   'need the matching Ars Nouveau progress first; EMI shows every recipe.'])

    def row(y, quests):
        """quests: list of (slug, title, tasks, rewards, icon, desc[, extra kw]). Chained left to right."""
        prev = 'start'
        for i, q in enumerate(quests):
            slug, title, tasks, rewards, icon, desc = q[:6]
            kw = q[6] if len(q) > 6 else {}
            ch.quest(slug, title, tasks, rewards, deps=[prev], icon=icon, x=2 + i * 1.75, y=y,
                     desc=desc if isinstance(desc, list) else [desc], **kw)
            prev = slug

    # Ars Elemental: foci and armour sets
    row(-6, [
        ('elemental_bangle', 'Elemental Bangles', [item('ars_elemental:base_bangle')],
         [give('minecraft:gold_ingot', 4), xp(40)], 'ars_elemental:base_bangle',
         '&bArs Elemental&r adds elemental schools, foci, armour, bangles, and new familiars.'),
        ('elemental_caster_bag', 'Caster Bag', [adv('ars_nouveau:caster_bag')],
         [give('minecraft:leather', 8), xp(40)], 'ars_elemental:caster_bag',
         'A curio bag that holds your spell books, tomes and parchments.'),
        ('elemental_spell_mirror', 'Spell Mirror', [item('ars_elemental:spell_mirror')],
         [give('minecraft:glass', 8), xp(40)], 'ars_elemental:spell_mirror', 'Reflects spells back.'),
    ] + [
        (f'elemental_{e}_robes', f'{a.title()} Robes', [item(f'ars_elemental:{a}_robes')],
         [give(f'ars_nouveau:{e}_essence', 4), xp(75)], f'ars_elemental:{a}_robes',
         f'The {e} school\'s mage armour.')
        for e, a in ELEMENTS
    ])

    # Ars Elemancy: hybrid schools
    row(-4, [
        (f'elemancy_{e}', f'{e.title()} Essence', [item(f'ars_elemancy:{e}_essence')],
         [xp(60)], f'ars_elemancy:{e}_essence',
         f'&bArs Elemancy&r combines two elements into a hybrid school. {e.title()} is one of them.')
        for e in ELEMANCY
    ] + [
        ('elemancy_elemancer', 'Elemancer', [item('ars_elemancy:elemancer_essence')],
         [give('ars_nouveau:source_gem_block', 2), levels(10)], 'ars_elemancy:elemancer_essence',
         'The essence of all elements at once.', {'shape': 'diamond'}),
    ])

    # Ars Additions + Ars Controle + Two-Way Portals
    row(-2, [
        ('additions_codex', 'Lost Knowledge', [item('ars_additions:codex_entry')],
         [give('ars_nouveau:blank_parchment', 4), xp(40)], 'ars_additions:codex_entry',
         '&bArs Additions&r hides codex entries in loot; read them to learn new glyphs.'),
        ('additions_haversack', 'Handy Haversack', [item('ars_additions:handy_haversack')],
         [give('minecraft:leather', 8), xp(40)], 'ars_additions:handy_haversack',
         'A bag that feeds blocks to your spells.'),
        ('additions_wayfinder', 'Wayfinder', [item('ars_additions:wayfinder')],
         [give('minecraft:compass'), xp(40)], 'ars_additions:wayfinder',
         'Points the way to a chosen structure.'),
        ('additions_ruined_portal', 'Ruined Portal', [adv('ars_additions:find_ruined_portal')],
         [give('ars_nouveau:source_gem', 8), xp(60)], 'minecraft:crying_obsidian',
         'Find one of the ruined magical portals added by Ars Additions.'),
        ('additions_warp_nexus', 'Warp Nexus', [item('ars_additions:warp_nexus')],
         [give('ars_nouveau:stable_warp_scroll'), xp(60)], 'ars_additions:warp_nexus',
         'A hub for teleporting between many locations.'),
        ('controle_remote', 'Ars Controle', [item('ars_controle:remote')],
         [give('minecraft:redstone', 16), xp(40)], 'ars_controle:remote',
         '&bArs Controle&r adds remotes and logic filters for spell automation.'),
        ('two_way_portal', 'Two-Way Portals', [item('ars_two_way_portals:double_sided_stable_warp_scroll')],
         [give('ars_nouveau:sourcestone', 32), xp(60)], 'ars_two_way_portals:double_sided_stable_warp_scroll',
         'Make Ars warp portals that work in both directions.'),
    ])

    # Ars Zero: staves and the necropolis
    row(0, [
        ('zero_staff', 'Novice Spell Staff', [item('ars_zero:novice_spell_staff')],
         [give('ars_nouveau:source_gem', 8), xp(50)], 'ars_zero:novice_spell_staff',
         '&bArs Zero&r adds spell staves that cast continuous and multi-phase spells.'),
        ('zero_mage_staff', 'Mage Spell Staff', [item('ars_zero:mage_spell_staff')],
         [give('ars_nouveau:source_gem_block'), xp(75)], 'ars_zero:mage_spell_staff', 'A stronger staff.'),
        ('zero_archmage_staff', 'Archmage Spell Staff', [item('ars_zero:archmage_spell_staff')],
         [give('ars_nouveau:source_gem_block', 2), levels(10)], 'ars_zero:archmage_spell_staff',
         'The strongest staff.'),
        ('zero_circlet', "Psion's Circlet", [item('ars_zero:spellcasting_circlet')],
         [give('minecraft:gold_ingot', 8), xp(75)], 'ars_zero:spellcasting_circlet',
         'Cast spells without a book in hand.'),
        ('zero_necropolis', 'Necropolis', [structure('ars_zero:necropolis')],
         [give('minecraft:golden_apple', 2), xp(100)], 'ars_zero:bone_chest',
         'Find the Necropolis, home of the Lich.'),
        ('zero_lich', 'The Lich', [kill('ars_zero:lich')],
         [give('minecraft:nether_star'), levels(15)], 'minecraft:wither_skeleton_skull',
         'Defeat the Lich that rules the Necropolis.', {'shape': 'octagon', 'size': 1.25}),
    ])

    # Ars Artillery: turrets by tier
    row(2, [
        ('artillery_crate', 'Turret Crate', [item('ars_artillery:fire_turret_crate')],
         [give('ars_nouveau:fire_essence', 4), xp(50)], 'ars_artillery:fire_turret_crate',
         '&bArs Artillery&r adds elemental turrets that defend an area. This one asks for a fire '
         'turret; any element is fine for your base.'),
        ('artillery_tier2', 'Tier 2 Upgrade', [item('ars_artillery:tier_2_upgrade')],
         [give('ars_nouveau:source_gem_block'), xp(75)], 'ars_artillery:tier_2_upgrade',
         'Upgrade a turret to tier 2.'),
        ('artillery_tier3', 'Tier 3 Upgrade', [item('ars_artillery:tier_3_upgrade')],
         [give('ars_nouveau:source_gem_block', 2), levels(10)], 'ars_artillery:tier_3_upgrade',
         'The strongest turret tier.'),
    ])

    # Starbunclemania, Ars Delight, Ars Caelum, Ars Affinity
    row(4, [
        ('starby_fluid', 'Starbunclemania', [item('starbunclemania:fluid_jar')],
         [give('minecraft:bucket', 2), xp(40)], 'starbunclemania:fluid_jar',
         '&bStarbunclemania&r teaches starbuncles to carry fluids and adds fun cosmetics.'),
        ('starby_hat', 'Fancy Starbuncle', [item('starbunclemania:star_hat')],
         [give('minecraft:golden_carrot', 8), xp(30)], 'starbunclemania:star_hat',
         'Dress up a starbuncle. Purely for style.', {'optional': True}),
        ('ars_delight', 'Ars Delight', [item('arsdelight:archwood_cabinet')],
         [give('ars_nouveau:source_berry_pie', 4), xp(40)], 'arsdelight:archwood_cabinet',
         '&bArs Delight&r brings magical cooking to Farmer\'s Delight.'),
        ('ars_affinity', 'Affinity', [adv('ars_affinity:affinity_initiate')],
         [give('ars_nouveau:source_gem', 8), xp(60)], 'ars_affinity:affinity_anchor_charm',
         '&bArs Affinity&r makes you better at the schools of magic you use the most.'),
        ('ars_affinity_mastery', 'Fire Affinity Mastery', [adv('ars_affinity:affinity_fire_mastery')],
         [levels(10)], 'ars_nouveau:fire_essence', 'Master one school completely. This quest tracks fire.',
         {'optional': True}),
    ])
    return ch
