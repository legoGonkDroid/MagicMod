"""Chapter 12 — Relics & Treasures (codex): unique items, one sub-collection per row."""
from model import Chapter, check, give, item, levels, xp

COLLECTIONS = [
    ('relics', 'Relics', 'relics:relic_experience_bottle',
     'Relics are found in loot chests all over the world. They level up as you use them.',
     ['relics:chorus_staff', 'relics:clot_of_time', 'relics:cut_glass_boot', 'relics:experience_disperser',
      'relics:ghostly_mantle', 'relics:glitchy_mantle', 'relics:golden_tooth', 'relics:hunting_belt',
      'relics:jellyfish_necklace', 'relics:kinetic_belt', 'relics:leafy_mantle', 'relics:midnight_mantle',
      'relics:pet_bone', 'relics:piglin_mask', 'relics:reflective_necklace', 'relics:rider_flute',
      'relics:ring_of_the_seven_deadly_sins', 'relics:roller_skate', 'relics:shield_of_retaliation',
      'relics:sphere_of_self_sacrifice', 'relics:springy_boot', 'relics:chef_hat'],
     [give('relics:relic_experience_bottle', 8)]),
    ('reliquified', 'Reliquified Ars Nouveau', 'reliquified_ars_nouveau:mana_ring',
     'Magical relics themed around Ars Nouveau, found in loot or crafted (check EMI).',
     ['reliquified_ars_nouveau:architects_staff', 'reliquified_ars_nouveau:archmage_glove',
      'reliquified_ars_nouveau:ballistarian_bracer', 'reliquified_ars_nouveau:cloak_of_concealment',
      'reliquified_ars_nouveau:emblem_of_assault', 'reliquified_ars_nouveau:emblem_of_defense',
      'reliquified_ars_nouveau:emblem_of_devotion', 'reliquified_ars_nouveau:flaming_bracer',
      'reliquified_ars_nouveau:horn_of_the_wild_hunter', 'reliquified_ars_nouveau:illusionists_mantle',
      'reliquified_ars_nouveau:mana_ring', 'reliquified_ars_nouveau:quantum_bubble',
      'reliquified_ars_nouveau:ring_of_last_will', 'reliquified_ars_nouveau:ring_of_thrift',
      'reliquified_ars_nouveau:spiked_cloak', 'reliquified_ars_nouveau:staff_of_the_spectral_walker',
      'reliquified_ars_nouveau:whirling_broom', 'reliquified_ars_nouveau:wing_of_the_wild_stalker'],
     [give('relics:relic_experience_bottle', 8)]),
    ('trinkets', 'Ars Trinkets', 'ars_trinkets:omnipotence_crown',
     'Powerful trinkets from Ars Trinkets. Check EMI for how to make each.',
     ['ars_trinkets:essence_core_1', 'ars_trinkets:essence_core_2', 'ars_trinkets:essence_core_3',
      'ars_trinkets:holy_heart', 'ars_trinkets:putrid_heart', 'ars_trinkets:omnipotence_crown',
      'ars_trinkets:unholy_focus', 'ars_trinkets:essence_ring_10', 'ars_trinkets:essence_lotus_10',
      'ars_trinkets:monocle_10', 'ars_trinkets:eternity_rune', 'ars_trinkets:mage_rune_greater',
      'ars_trinkets:life_rune_greater', 'ars_trinkets:warrior_rune_greater', 'ars_trinkets:death_rune_greater'],
     [give('ars_nouveau:source_gem_block', 4)]),
    ('discount', 'Greatest Discount', 'greatest_discount:ring_of_greatest_discount',
     'The best mana trinkets in the pack.',
     ['greatest_discount:ring_of_greatest_discount', 'greatest_discount:amulet_of_greater_mana_regen',
      'greatest_discount:scarf_of_greatest_mana_regen'],
     [give('ars_nouveau:source_gem_block', 2)]),
    ('violetgold', 'Violetgold Equipment', 'ars_violetgold_equipment:violetgold_ingot',
     'Violetgold gear from Ars Violetgold Equipment.',
     ['ars_violetgold_equipment:violetgold_helmet', 'ars_violetgold_equipment:violetgold_chestplate',
      'ars_violetgold_equipment:violetgold_leggings', 'ars_violetgold_equipment:violetgold_boots',
      'ars_violetgold_equipment:violetgold_blade', 'ars_violetgold_equipment:violetgold_wand',
      'ars_violetgold_equipment:violetgold_amulet', 'ars_violetgold_equipment:violetgold_ring_of_discount'],
     [give('ars_violetgold_equipment:violetgold_ingot', 4)]),
    ('cataclysm', 'Cataclysm Arsenal', 'cataclysm:the_incinerator',
     'Signature weapons and gear forged from Cataclysm boss drops.',
     ['cataclysm:the_incinerator', 'cataclysm:bulwark_of_the_flame', 'cataclysm:gauntlet_of_guard',
      'cataclysm:gauntlet_of_bulwark', 'cataclysm:the_annihilator', 'cataclysm:infernal_forge',
      'cataclysm:void_forge', 'cataclysm:the_immolator', 'cataclysm:wither_assault_shoulder_weapon',
      'cataclysm:void_assault_shoulder_weapon', 'cataclysm:laser_gatling', 'cataclysm:wrath_of_the_desert',
      'cataclysm:sandstorm_in_a_bottle', 'cataclysm:soul_render', 'cataclysm:cursed_bow',
      'cataclysm:tidal_claws', 'cataclysm:gauntlet_of_maelstrom', 'cataclysm:astrape', 'cataclysm:ceraunus',
      'cataclysm:zweiender', 'cataclysm:ignitium_helmet', 'cataclysm:cursium_helmet',
      'cataclysm:monstrous_helm', 'cataclysm:final_fractal'],
     [give('minecraft:netherite_ingot')]),
    ('thunder', 'Harsh Encounters', 'harsh_encounters:thunder_spear',
     'Spoils from the Thunderous Tower and its Deviser.',
     ['harsh_encounters:thunder_spear', 'harsh_encounters:voltaic_hammer', 'harsh_encounters:deviser_gauntlet',
      'harsh_encounters:spark_rod', 'harsh_encounters:soul_of_thunder'],
     [give('minecraft:lightning_rod', 4)]),
]


def build(reg):
    ch = Chapter('relics', 'Relics & Treasures', 'codex', 'relics:relic_experience_bottle',
                 subtitle='Unique items from every corner of the world.')

    ch.quest('start', 'Treasure Hunter', [check()],
             [give('minecraft:compass'), xp(10)],
             icon='minecraft:chest', shape='gear', size=1.5, x=0, y=0,
             desc=['A catalogue of the rarest items in the pack: relics, trinkets, and boss weapons.',
                   '',
                   'Items are only checked, never taken. &eLootr&r chests mean every player gets their '
                   'own loot.'])

    y = -7.0
    caps = []
    cols = 8
    for slug, title, icon, desc, items, prize in COLLECTIONS:
        slugs = []
        for i, it in enumerate(items):
            qslug = slug + '_' + it.split(':')[1]
            ch.quest(qslug, reg.name(it) or it, [item(it)], [xp(50)],
                     deps=['start'], icon=it, size=0.75, x=2 + (i % cols) * 1.25, y=y + (i // cols) * 1.25,
                     desc=[desc])
            slugs.append(qslug)
        rows = (len(items) + cols - 1) // cols
        ch.quest(slug + '_all', title, [check(title=f'All {len(items)} collected')], prize + [levels(10)],
                 deps=slugs, icon=icon, shape='diamond', size=1.25,
                 x=2 + cols * 1.25 + 0.75, y=y + (rows - 1) * 0.625,
                 desc=[f'Every item in &6{title}&r.'])
        caps.append(slug + '_all')
        y += rows * 1.25 + 0.75

    ch.quest('all', 'Curator', [check(title='Every collection complete')],
             [give('minecraft:nether_star', 2), give('minecraft:diamond_block', 4), levels(30)],
             deps=caps, icon='minecraft:nether_star', shape='heart', size=2.0, x=15, y=0,
             subtitle='Collection complete',
             desc=['Every treasure in the pack has passed through your hands.'])
    return ch
