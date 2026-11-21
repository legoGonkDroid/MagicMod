"""Chapter 4 — Apprentice Arcanist: apprentice book, mage armour, threads, Wilden Chimera."""
from model import Chapter, adv, give, item, kill, levels, potion, xp


def build(reg):
    ch = Chapter('apprentice', 'Apprentice Arcanist', 'journey', 'ars_nouveau:apprentice_spell_book',
                 subtitle='Better spells, mage armour, and the Wilden Chimera.')

    ch.quest('start', 'Apprentice Spell Book', [adv('ars_nouveau:apprentice_spell_book')],
             [give('ars_nouveau:source_gem', 8), xp(100)],
             deps=['infrastructure/ready'], icon='ars_nouveau:apprentice_spell_book', shape='gear', size=1.5,
             desc=['Upgrade your book in the Enchanting Apparatus. The &dApprentice Spell Book&r holds '
                   'more spells and lets you learn tier 2 glyphs.'])

    ch.quest('tier2_glyphs', 'Apprentice Glyphs', [item('ars_nouveau:glyph_explosion', key='explosion'),
                                                   item('ars_nouveau:glyph_pierce', key='pierce'),
                                                   item('ars_nouveau:glyph_aoe', key='aoe')],
             [give('minecraft:gunpowder', 16), give('ars_nouveau:fire_essence', 2), xp(60)],
             deps=['start'], icon='ars_nouveau:glyph_aoe',
             desc=['&aArea of Effect&r widens any effect and &aPierce&r lets projectiles pass through targets. '
                   'Explosion is a strong tier 2 combat effect.'])

    # Mage armour: any one set
    for slug, name, desc in [
        ('sorcerer', 'Sorcerer', 'Light armour focused on mana.'),
        ('arcanist', 'Arcanist', 'Balanced armour for all-round mages.'),
        ('battlemage', 'Battlemage', 'Heavy armour for mages who fight up close.'),
    ]:
        ch.quest(f'armor_{slug}', f'{name} Robes', [item(f'ars_nouveau:{slug}_robes')],
                 [give(f'ars_nouveau:{slug}_hood'), xp(40)],
                 deps=['start'], icon=f'ars_nouveau:{slug}_robes',
                 desc=[f'{desc} Each set has a different stat profile; crafting any one set completes '
                       'the next quest.'])

    ch.quest('armor', 'Dressed for Magic', [item('ars_nouveau:blank_thread')],
             [give('ars_nouveau:magebloom_fiber', 16), xp(50)],
             deps=['armor_sorcerer', 'armor_arcanist', 'armor_battlemage'], min_deps=1,
             icon='ars_nouveau:arcanist_hood', shape='diamond',
             desc=['Mage armour has slots for &dThreads&r, which add perks. Get a blank thread and '
                   'apply it at the Alteration Table.'])

    ch.quest('threads', 'Threads of Power', [item('ars_nouveau:thread_spellpower', key='spellpower'),
                                             item('ars_nouveau:thread_magic_capacity', key='capacity')],
             [give('ars_nouveau:blank_thread', 2), xp(60)],
             deps=['armor'], icon='ars_nouveau:thread_spellpower',
             desc=['&dSpell Power&r and &dMagic Capacity&r threads are two of the most useful. Socket '
                   'them at the Alteration Table.'])

    ch.quest('hunter', 'Wilden Hunter', [kill('ars_nouveau:wilden_hunter'), item('ars_nouveau:wilden_horn')],
             [give('minecraft:cooked_beef', 8), xp(40)],
             deps=['start'], icon='ars_nouveau:wilden_horn',
             desc=['Wilden roam magical forests at night. Hunters drop &dWilden Horns&r.'])
    ch.quest('stalker', 'Wilden Stalker', [kill('ars_nouveau:wilden_stalker'), item('ars_nouveau:wilden_wing')],
             [give('minecraft:arrow', 32), xp(40)],
             deps=['start'], icon='ars_nouveau:wilden_wing',
             desc=['Stalkers leap at you from above. They drop &dWilden Wings&r.'])
    ch.quest('guardian', 'Wilden Defender', [kill('ars_nouveau:wilden_guardian'), item('ars_nouveau:wilden_spike')],
             [give('minecraft:shield'), xp(40)],
             deps=['start'], icon='ars_nouveau:wilden_spike',
             desc=['Defenders curl up into spiked balls. They drop &dWilden Spikes&r.'])

    ch.quest('summon_ritual', 'Ritual of the Wild', [item('ars_nouveau:ritual_wilden_summon')],
             [give('minecraft:golden_apple', 2), potion('long_regeneration'), xp(60)],
             deps=['hunter', 'stalker', 'guardian'], icon='ars_nouveau:ritual_wilden_summon',
             desc=['The &dRitual of the Wild&r summons Wilden. Augment it with a horn, a wing and a '
                   'spike (check the Worn Notebook) to summon the &cWilden Chimera&r instead.',
                   '',
                   'Prepare: armour, healing, food and a strong spell.'])

    ch.quest('chimera', 'The Wilden Chimera', [kill('ars_nouveau:wilden_boss')],
             [give('minecraft:diamond', 4), give('ars_nouveau:source_gem_block', 2), levels(5)],
             deps=['summon_ritual'], icon='ars_nouveau:wilden_tribute', shape='octagon', size=1.5,
             subtitle='Boss',
             desc=['Defeat the &cWilden Chimera&r. It changes phases, charges, and fires spikes.',
                   '',
                   'It drops the &dWilden Tribute&r, needed for powerful items later.'])

    ch.quest('tribute', 'Wilden Tribute', [item('ars_nouveau:wilden_tribute')],
             [give('ars_nouveau:source_gem', 8), xp(50)],
             deps=['chimera'], icon='ars_nouveau:wilden_tribute',
             desc=['Keep the Tribute safe. Check EMI (&eU&r) to see what it is used for.'])

    ch.quest('ready', 'Apprentice Arcanist', [item('ars_nouveau:source_gem_block', 4, title='4 Source Gem Blocks')],
             [give('minecraft:obsidian', 10), give('minecraft:flint_and_steel'), xp(150)],
             deps=['tier2_glyphs', 'threads', 'tribute'],
             icon='ars_nouveau:apprentice_spell_book', shape='hexagon', size=1.25,
             desc=['You are ready to leave the Overworld behind for a while.',
                   '',
                   'Completing this quest unlocks &6Into the Nether&r.'])
    return ch
