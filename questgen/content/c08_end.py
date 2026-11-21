"""Chapter 8 — The End: stronghold, Ender Dragon (main goal), then the Ender Guardian epilogue."""
from model import Chapter, adv, give, item, kill, levels, potion, structure, xp

# Every boss that must be defeated before the dragon quest unlocks.
REQUIRED_BOSSES = [
    'apprentice/chimera',
    'nether/ignis', 'nether/monstrosity',
    'ancient/harbinger', 'ancient/remnant', 'ancient/maledictus', 'ancient/leviathan', 'ancient/scylla',
]


def build(reg):
    ch = Chapter('end', 'The End', 'journey', 'minecraft:dragon_egg',
                 subtitle='Slay the Ender Dragon, then face what waits beyond.')

    ch.quest('start', 'Eyes of Ender', [item('minecraft:ender_eye', 12, title='12 Eyes of Ender')],
             [give('minecraft:ender_pearl', 4), xp(100)],
             deps=['archmage/ready'], icon='minecraft:ender_eye', shape='gear', size=1.5, x=0, y=0,
             desc=['Craft Eyes of Ender. Some will break when thrown, and the portal needs up to 12.'])

    ch.quest('follow_eye', 'Follow the Eye', [adv('minecraft:story/follow_ender_eye')],
             [give('minecraft:torch', 32), xp(50)],
             deps=['start'], icon='minecraft:ender_pearl', x=2, y=0,
             desc=['Throw an Eye of Ender and follow it to a stronghold.'])

    ch.quest('stronghold', 'The Stronghold', [structure('minecraft:stronghold')],
             [give('minecraft:cooked_beef', 16), xp(80)],
             deps=['follow_eye'], icon='minecraft:end_portal_frame', x=4, y=0,
             desc=['Find the stronghold and its End Portal room.'])

    ch.quest('enter_end', 'The End', [adv('minecraft:story/enter_the_end')],
             [potion('long_slow_falling', 2), give('minecraft:water_bucket'), xp(100)],
             deps=['stronghold'], icon='minecraft:end_stone', x=6, y=0,
             desc=['Fill the portal and jump in. There is no way back except by winning or dying, so '
                   'bring everything you need: blocks, food, potions and a full spell book.'])

    ch.quest('dragon', 'The Ender Dragon', [adv('minecraft:end/kill_dragon', title='Defeat the Ender Dragon')],
             [give('minecraft:elytra'), give('ars_nouveau:source_gem_block', 8),
              give('minecraft:enchanted_golden_apple', 2), levels(30)],
             deps=['enter_end'] + REQUIRED_BOSSES,
             icon='minecraft:dragon_head', shape='heart', size=2.5, x=9, y=0,
             subtitle='The goal of the Journey',
             desc=['Destroy the End Crystals on the obsidian pillars, then bring down the &5Ender '
                   'Dragon&r.',
                   '',
                   'This quest unlocks only after every Cataclysm boss in the Overworld and Nether and '
                   'the Wilden Chimera are defeated.',
                   '',
                   '&6Congratulations, Archmage!&r'])

    # ---- epilogue
    ch.quest('dragon_egg', 'The Dragon Egg', [item('minecraft:dragon_egg')],
             [give('minecraft:item_frame', 2), xp(100)],
             deps=['dragon'], icon='minecraft:dragon_egg', x=9, y=-2.5, optional=True,
             desc=['The egg teleports when touched. Push it onto a torch to collect it.'])

    ch.quest('dragon_breath', "Dragon's Breath", [adv('minecraft:end/dragon_breath')],
             [give('minecraft:glass_bottle', 8), xp(50)],
             deps=['dragon'], icon='minecraft:dragon_breath', x=9, y=2.5, optional=True,
             desc=["Catch the dragon's breath in a glass bottle. Used for lingering potions."])

    ch.quest('gateway', 'Beyond the Gateway', [adv('minecraft:end/enter_end_gateway')],
             [give('minecraft:ender_pearl', 8), xp(100)],
             deps=['dragon'], icon='minecraft:ender_pearl', x=11, y=0,
             desc=['Throw an ender pearl into the End Gateway that appeared after the fight to reach '
                   'the outer islands.'])

    ch.quest('end_city', 'End City', [adv('minecraft:end/find_end_city')],
             [give('minecraft:golden_carrot', 16), xp(100)],
             deps=['gateway'], icon='minecraft:purpur_block', x=13, y=0,
             desc=['End Cities hold loot, shulkers and sometimes an End Ship with an elytra.'])

    ch.quest('shulker', 'Shulker Shells', [item('minecraft:shulker_shell', 4, title='4 Shulker Shells')],
             [give('minecraft:chest', 4), xp(80)],
             deps=['end_city'], icon='minecraft:shulker_shell', x=15, y=-1.5,
             desc=['Shulker shells are needed for the &6Eye of Void&r and for shulker boxes.'])

    ch.quest('elytra', 'Wings', [adv('minecraft:end/elytra')],
             [give('minecraft:firework_rocket', 32), xp(100)],
             deps=['end_city'], icon='minecraft:elytra', x=15, y=1.5, optional=True,
             desc=['Find an elytra on an End Ship. (The dragon already gave you one, but a spare never '
                   'hurts.)'])

    ch.quest('ender_golem', 'Ender Golem', [kill('cataclysm:ender_golem')],
             [give('minecraft:ender_pearl', 8), levels(5)],
             deps=['gateway'], icon='minecraft:obsidian', x=13, y=2.5, optional=True,
             desc=['An optional Cataclysm mini-boss that roams the outer End islands.'])

    ch.quest('void_eye', 'Eye of Void', [item('cataclysm:void_eye')],
             [potion('long_slow_falling', 2), xp(100)],
             deps=['shulker'], icon='cataclysm:void_eye', x=17, y=-1.5,
             desc=['Obtain an &6Eye of Void&r (check EMI). It leads to the &cRuined Citadel&r, found '
                   'only in the End Highlands and Midlands.'])

    ch.quest('citadel', 'The Ruined Citadel', [structure('cataclysm:ruined_citadel')],
             [give('minecraft:enchanted_golden_apple'), xp(100)],
             deps=['void_eye'], icon='cataclysm:altar_of_void', x=19, y=-1.5,
             desc=['Find the Ruined Citadel. The &5Ender Guardian&r sleeps within.'])

    ch.quest('ender_guardian', 'The Ender Guardian', [kill('cataclysm:ender_guardian')],
             [give('minecraft:netherite_ingot', 2), give('minecraft:nether_star'),
              give('ars_nouveau:source_gem_block', 8), levels(30)],
             deps=['citadel'], icon='cataclysm:music_disc_ender_guardian', shape='heart', size=2.0,
             x=21, y=0, subtitle='The final challenge',
             desc=['The last and strongest of the Cataclysm bosses. Its void attacks pull you in and '
                   'its blasts break through shields.',
                   '',
                   'Defeat it to complete &6The Journey&r. Well done.'])
    return ch
