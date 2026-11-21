"""Chapter 2 — Novice Mage: Ars Nouveau basics (archwood, source, glyphs)."""
from model import Chapter, adv, biome, give, item, xp


def build(reg):
    ch = Chapter('novice', 'Novice Mage', 'journey', 'ars_nouveau:source_gem',
                 subtitle='Source, glyphs and the first tools of a mage.')

    ch.quest('start', 'The Study of Source', [item('ars_nouveau:worn_notebook')],
             [give('ars_nouveau:source_gem', 2), xp(25)],
             deps=['welcome/ready'], icon='ars_nouveau:worn_notebook', shape='gear', size=1.5,
             desc=['The &dWorn Notebook&r is the Ars Nouveau guide book. Everything in this chapter is '
                   'explained in it, step by step.',
                   '',
                   'Craft one (check EMI) and keep it handy.'])

    ch.quest('archwood_forest', 'Into the Archwood', [biome('ars_nouveau:archwood_forest')],
             [give('ars_nouveau:magebloom_crop', 4), xp(25)],
             deps=['start'], icon='ars_nouveau:green_archwood_sapling',
             desc=['&dArchwood Forests&r are where magic grows. Their colourful trees, Sourceberries and '
                   'creatures are all useful to a mage.'])

    ch.quest('archwood', 'Archwood Planks', [item('ars_nouveau:archwood_planks', 32, title='32 Archwood Planks')],
             [give('ars_nouveau:red_archwood_sapling'), give('ars_nouveau:blue_archwood_sapling'),
              give('ars_nouveau:purple_archwood_sapling'), give('ars_nouveau:green_archwood_sapling'), xp(20)],
             deps=['archwood_forest'], icon='ars_nouveau:archwood_planks',
             desc=['Archwood is the building material of Ars Nouveau. Every colour of archwood log makes '
                   'the same planks.'])

    ch.quest('sourceberry', 'Sourceberries', [item('ars_nouveau:sourceberry_bush', 4)],
             [give('ars_nouveau:source_berry_pie', 2), xp(15)],
             deps=['archwood_forest'], icon='ars_nouveau:sourceberry_bush',
             desc=['Sourceberries grow in Archwood Forests. Eating them restores mana, and they are a '
                   'fuel for some sourcelinks.'])

    ch.quest('magebloom', 'Magebloom', [adv('ars_nouveau:magebloom_crop'),
                                       item('ars_nouveau:magebloom_fiber', 4, title='4 Magebloom Fiber')],
             [give('minecraft:bone_meal', 16), xp(25)],
             deps=['archwood_forest'], icon='ars_nouveau:magebloom',
             desc=['Plant &dMagebloom&r and harvest it. Its fiber is used for mage armour, threads and '
                   'blank parchment.'])

    ch.quest('scribes_table', "Scribe's Table", [item('ars_nouveau:scribes_table')],
             [give('ars_nouveau:blank_parchment', 4), give('minecraft:lapis_lazuli', 8), xp(30)],
             deps=['archwood'], icon='ars_nouveau:scribes_table',
             desc=["Glyphs are crafted at a &dScribe's Table&r. Right-click it with your spell book "
                   'to open the glyph list, then place the ingredients on the table.'])

    ch.quest('imbuement', 'Imbuement Chamber', [adv('ars_nouveau:imbuement_chamber')],
             [give('minecraft:amethyst_shard', 16), xp(30)],
             deps=['archwood'], icon='ars_nouveau:imbuement_chamber',
             desc=['The &dImbuement Chamber&r turns amethyst into &dSource Gems&r. Without a source jar '
                   'nearby it works slowly on its own; with one it is much faster.'])

    ch.quest('source_gems', 'Source Gems', [item('ars_nouveau:source_gem', 16, title='16 Source Gems')],
             [give('ars_nouveau:source_gem_block'), xp(30)],
             deps=['imbuement'], icon='ars_nouveau:source_gem',
             desc=['Source Gems are needed for nearly everything. Keep the chamber busy.'])

    ch.quest('source_jar', 'Source Jar', [adv('ars_nouveau:source_jar')],
             [give('minecraft:glass', 16), xp(30)],
             deps=['source_gems'], icon='ars_nouveau:source_jar',
             desc=['&dSource Jars&r store source. Devices nearby draw from them automatically.'])

    ch.quest('sourcelink', 'Sourcelinks', [item('ars_nouveau:volcanic_sourcelink', key='volcanic'),
                                           item('ars_nouveau:agronomic_sourcelink', key='agronomic')],
             [give('ars_nouveau:source_gem', 8), give('minecraft:coal_block', 2), xp(50)],
             deps=['source_jar'], icon='ars_nouveau:volcanic_sourcelink',
             desc=['Sourcelinks generate source and fill nearby jars:',
                   '&6Volcanic&r burns fuel, &aAgronomic&r feeds on nearby crops growing.',
                   '',
                   'Mycelial, Vitalic and Alchemical sourcelinks come later.'])

    ch.quest('projectile', 'First Glyphs', [item('ars_nouveau:glyph_projectile', key='projectile'),
                                            item('ars_nouveau:glyph_break', key='break'),
                                            item('ars_nouveau:glyph_harm', key='harm')],
             [give('ars_nouveau:blank_parchment', 4), give('ars_nouveau:source_gem', 4), xp(40)],
             deps=['scribes_table', 'source_gems'], icon='ars_nouveau:glyph_projectile',
             desc=['Craft the &aProjectile&r form and the &aBreak&r and &aHarm&r effects.',
                   '',
                   'Hold each glyph for a moment so the quest sees it, then right-click to learn it. '
                   'Projectile + Harm is your first combat spell; Projectile + Break mines from range.'])

    ch.quest('utility_glyphs', 'Useful Magic', [item('ars_nouveau:glyph_light', key='light'),
                                                 item('ars_nouveau:glyph_leap', key='leap'),
                                                 item('ars_nouveau:glyph_heal', key='heal')],
             [give('minecraft:golden_carrot', 8), xp(40)],
             deps=['projectile'], icon='ars_nouveau:glyph_light',
             desc=['Light, Leap and Heal make survival much easier. Try Self + Heal, or Touch + Light.'])

    ch.quest('magelight', 'Magelight', [item('ars_nouveau:magelight_torch', 4)],
             [give('ars_nouveau:sourcestone', 32), xp(15)],
             deps=['source_gems'], icon='ars_nouveau:magelight_torch', optional=True,
             desc=['Decorative magical light. Sourcestone makes a fine wizard tower, too.'])

    ch.quest('dowsing_rod', 'Dowsing Rod', [item('ars_nouveau:dowsing_rod')],
             [give('ars_nouveau:source_gem', 2), xp(15)],
             deps=['source_gems'], icon='ars_nouveau:dowsing_rod', optional=True,
             desc=['Use a &dDowsing Rod&r to reveal hidden magical blocks and creatures nearby.'])

    ch.quest('warp_scroll', 'Warp Scroll', [adv('ars_nouveau:warp_scroll')],
             [give('waystones:warp_dust', 4), xp(20)],
             deps=['source_gems'], icon='ars_nouveau:warp_scroll', optional=True,
             desc=['Bind a &dWarp Scroll&r to a location, then use it to return there.'])

    ch.quest('ready', 'Novice No More', [item('ars_nouveau:source_gem', 32, title='32 Source Gems')],
             [give('ars_nouveau:source_gem_block', 2), give('minecraft:gold_ingot', 8), xp(100)],
             deps=['sourcelink', 'utility_glyphs', 'sourceberry', 'magebloom'],
             icon='ars_nouveau:source_gem_block', shape='hexagon', size=1.25,
             desc=['Stockpile some Source Gems: the next chapter builds a lot of magical machinery.',
                   '',
                   'Completing this quest unlocks &6Arcane Infrastructure&r.'])
    return ch
