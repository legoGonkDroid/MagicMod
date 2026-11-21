"""Chapter 7 — Archmage: archmage book, elemental foci, top-tier gear."""
from model import Chapter, adv, give, item, levels, xp


def build(reg):
    ch = Chapter('archmage', 'Archmage', 'journey', 'ars_nouveau:archmage_spell_book',
                 subtitle='Reach the height of Ars Nouveau magic.')

    ch.quest('start', 'Archmage Spell Book', [adv('ars_nouveau:archmage_spell_book')],
             [give('ars_nouveau:source_gem_block', 4), levels(10)],
             deps=['ancient/ready'], icon='ars_nouveau:archmage_spell_book', shape='gear', size=1.5,
             desc=['Upgrade to the &dArchmage Spell Book&r in the Enchanting Apparatus. It holds the '
                   'most spells and unlocks tier 3 glyphs.'])

    ch.quest('tier3_glyphs', 'Archmage Glyphs', [item('ars_nouveau:glyph_split', key='split'),
                                                 item('ars_nouveau:glyph_linger', key='linger'),
                                                 item('ars_nouveau:glyph_lightning', key='lightning')],
             [give('ars_nouveau:air_essence', 4), give('ars_nouveau:conjuration_essence', 4), xp(150)],
             deps=['start'], icon='ars_nouveau:glyph_lightning',
             desc=['&aSplit&r, &aLinger&r and &aLightning&r are among the strongest glyphs in the book.'])

    ch.quest('spell_prism', 'Spell Prism', [adv('ars_nouveau:spell_prism')],
             [give('minecraft:quartz_block', 8), xp(80)],
             deps=['start'], icon='ars_nouveau:spell_prism', optional=True,
             desc=['Prisms redirect spell projectiles. Combine them with turrets for complex machines.'])

    ch.quest('lesser_focus', 'Lesser Focus', [item('ars_elemental:lesser_fire_focus', key='fire'),
                                              ], [give('ars_nouveau:fire_essence', 4), xp(80)],
             deps=['start'], icon='ars_elemental:lesser_fire_focus',
             desc=['Ars Elemental foci boost one school of magic. Any element works here, but this quest '
                   'asks for a &6Lesser Fire Focus&r, the easiest to start with. Check EMI for the others.'])

    ch.quest('focus', 'Elemental Focus', [item('ars_elemental:fire_focus')],
             [give('ars_nouveau:fire_essence', 8), levels(5)],
             deps=['lesser_focus'], icon='ars_elemental:fire_focus',
             desc=['Upgrade to a full elemental focus. It greatly strengthens fire spells and grants '
                   'fire immunity.'])

    ch.quest('mark', 'Mark of Mastery', [adv('ars_nouveau:mark_of_mastery')],
             [give('minecraft:nether_star'), levels(10)],
             deps=['focus'], icon='ars_elemental:mark_of_mastery',
             desc=['The &6Mark of Mastery&r is needed for the strongest Ars Elemental gear.'])

    ch.quest('elemental_armor', 'Elemental Armour', [item('ars_elemental:fire_robes')],
             [give('ars_nouveau:thread_spellpower'), levels(5)],
             deps=['mark'], icon='ars_elemental:fire_robes', optional=True,
             desc=['Ars Elemental armour boosts one school. Any element is fine for you, but this quest '
                   'tracks the fire set. See the &bArs Expansions&r chapter for the rest.'])

    ch.quest('experience', 'Experience Gems', [item('ars_nouveau:greater_experience_gem', 4)],
             [give('ars_nouveau:greater_experience_gem', 4), xp(50)],
             deps=['start'], icon='ars_nouveau:greater_experience_gem', optional=True,
             desc=['Greater Experience Gems store experience for enchanting and repairs.'])

    ch.quest('flight', 'Ritual of Flight', [item('ars_nouveau:ritual_flight')],
             [give('minecraft:feather', 16), give('minecraft:phantom_membrane', 4), xp(100)],
             deps=['start'], icon='ars_nouveau:ritual_flight',
             desc=['The &dRitual of Flight&r grants creative-style flight to nearby players while it '
                   'runs. A huge help for building.'])

    ch.quest('ready', 'Archmage', [item('ars_nouveau:source_gem_block', 8, title='8 Source Gem Blocks')],
             [give('minecraft:ender_pearl', 12), give('minecraft:blaze_rod', 6), levels(15)],
             deps=['tier3_glyphs', 'mark', 'flight'],
             icon='ars_nouveau:archmage_spell_book', shape='hexagon', size=1.25,
             desc=['You have mastered Ars Nouveau. One challenge remains.',
                   '',
                   'Completing this quest unlocks &6The End&r.'])
    return ch
