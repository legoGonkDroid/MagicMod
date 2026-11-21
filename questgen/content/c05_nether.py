"""Chapter 5 — Into the Nether: vanilla Nether + Ignis + Netherite Monstrosity."""
from model import Chapter, adv, give, item, kill, levels, potion, structure, xp


def build(reg):
    ch = Chapter('nether', 'Into the Nether', 'journey', 'minecraft:netherrack',
                 subtitle='Fire, fortresses, and two Cataclysm bosses.')

    ch.quest('start', 'Through the Portal', [adv('minecraft:story/enter_the_nether')],
             [give('minecraft:fire_charge', 4), give('minecraft:gold_ingot', 8), xp(50)],
             deps=['apprentice/ready'], icon='minecraft:obsidian', shape='gear', size=1.5,
             desc=['Build a Nether portal and step through. Wear gold so piglins leave you alone.'])

    ch.quest('fortress', 'Nether Fortress', [adv('minecraft:nether/find_fortress')],
             [give('minecraft:golden_apple'), xp(50)],
             deps=['start'], icon='minecraft:nether_bricks',
             desc=['Find a Nether Fortress. Blazes and wither skeletons live here.'])

    ch.quest('blaze', 'Blaze Rods', [item('minecraft:blaze_rod', 8, title='8 Blaze Rods')],
             [give('ars_nouveau:fire_essence', 2), xp(50)],
             deps=['fortress'], icon='minecraft:blaze_rod',
             desc=['Blaze rods are needed for brewing, eyes of ender and much more.'])

    ch.quest('bastion', 'Bastion Remnant', [adv('minecraft:nether/find_bastion')],
             [give('minecraft:gold_block', 2), xp(50)],
             deps=['start'], icon='minecraft:gilded_blackstone', optional=True,
             desc=['Bastions are full of loot and piglin brutes. Be careful.'])

    ch.quest('debris', 'Ancient Debris', [adv('minecraft:nether/obtain_ancient_debris')],
             [give('minecraft:tnt', 8), xp(60)],
             deps=['start'], icon='minecraft:ancient_debris',
             desc=['Ancient Debris is found deep in the Nether, around Y 15. A Break spell with '
                   'Amplify helps, and TNT works well.'])

    ch.quest('netherite', 'Netherite', [item('minecraft:netherite_ingot')],
             [give('minecraft:netherite_upgrade_smithing_template'), xp(80)],
             deps=['debris'], icon='minecraft:netherite_ingot',
             desc=['Combine netherite scraps with gold to make an ingot.'])

    ch.quest('brewing', 'Brewing', [adv('minecraft:nether/brew_potion')],
             [give('minecraft:nether_wart', 16), give('minecraft:glass_bottle', 8), xp(40)],
             deps=['blaze'], icon='minecraft:brewing_stand', optional=True,
             desc=['Fire resistance potions make the Nether and its bosses much safer.'])

    # --- Ignis
    ch.quest('flame_eye', 'Eye of Flame', [item('cataclysm:flame_eye')],
             [potion('long_fire_resistance', 2), xp(60)],
             deps=['blaze'], icon='cataclysm:flame_eye',
             desc=['Obtain an &6Eye of Flame&r (check EMI). Throw it like an Eye of Ender and it '
                   'leads you to the &cBurning Arena&r.'])
    ch.quest('burning_arena', 'The Burning Arena', [structure('cataclysm:burning_arena')],
             [give('minecraft:golden_apple', 2), xp(60)],
             deps=['flame_eye'], icon='cataclysm:altar_of_fire',
             desc=['Find the Burning Arena in the Nether. Ignis waits at its altar.'])
    ch.quest('ignis', 'Ignis', [kill('cataclysm:ignis')],
             [give('minecraft:netherite_scrap', 2), give('minecraft:enchanted_golden_apple'), levels(10)],
             deps=['burning_arena'], icon='cataclysm:music_disc_ignis', shape='octagon', size=1.5,
             subtitle='Boss',
             desc=['Defeat &cIgnis&r, the flaming knight. Fire resistance is essential; it gets far '
                   'more aggressive at low health.'])

    # --- Netherite Monstrosity
    ch.quest('monstrous_eye', 'Eye of Monstrous', [item('cataclysm:monstrous_eye')],
             [potion('long_fire_resistance', 2), xp(60)],
             deps=['netherite'], icon='cataclysm:monstrous_eye',
             desc=['Obtain an &6Eye of Monstrous&r (check EMI). It leads to the &cSoul Blacksmith&r.'])
    ch.quest('soul_black_smith', 'The Soul Blacksmith', [structure('cataclysm:soul_black_smith')],
             [give('minecraft:golden_apple', 2), xp(60)],
             deps=['monstrous_eye'], icon='cataclysm:monstrous_horn',
             desc=['Find the Soul Blacksmith, a ruined forge in the Nether.'])
    ch.quest('monstrosity', 'Netherite Monstrosity', [kill('cataclysm:netherite_monstrosity')],
             [give('minecraft:netherite_ingot'), give('minecraft:enchanted_golden_apple'), levels(10)],
             deps=['soul_black_smith'], icon='cataclysm:music_disc_netherite_monstrosity',
             shape='octagon', size=1.5, subtitle='Boss',
             desc=['Defeat the &cNetherite Monstrosity&r. It hits very hard and shoots lava bombs: '
                   'keep moving.'])

    ch.quest('revenant', 'Ignited Revenant', [kill('cataclysm:ignited_revenant')],
             [give('minecraft:bone_block', 4), xp(60)],
             deps=['fortress'], icon='minecraft:bone', optional=True,
             desc=['An optional mini-boss that guards Cataclysm Nether structures.'])

    ch.quest('ready', 'Conqueror of Fire', [item('minecraft:blaze_rod', 12, title='12 Blaze Rods')],
             [give('minecraft:ender_pearl', 8), give('minecraft:diamond', 4), xp(200)],
             deps=['ignis', 'monstrosity'], icon='minecraft:blaze_powder', shape='hexagon', size=1.25,
             desc=['Both Nether bosses are defeated. Bring extra blaze rods: Ancient Threats and the '
                   'End will need them.',
                   '',
                   'Completing this quest unlocks &6Ancient Threats&r.'])
    return ch
