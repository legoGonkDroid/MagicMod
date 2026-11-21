"""Chapter 16 — Homestead (codex): cooking, storage, and quality-of-life mods."""
from model import Chapter, adv, check, give, item, levels, xp


def build(reg):
    ch = Chapter('homestead', 'Homestead', 'codex', 'farmersdelight:cooking_pot',
                 subtitle='Food, storage, and comforts of home.')

    ch.quest('start', 'Home Sweet Home', [check()],
             [give('minecraft:oak_log', 32), xp(10)],
             icon='minecraft:oak_door', shape='gear', size=1.5, x=0, y=0,
             desc=['Every mage needs a comfortable base. These quests cover cooking, storage and other '
                   'handy mods. Everything here is optional.',
                   '',
                   'Tip: &eCarry On&r lets you pick up chests and animals: shift + right-click with an '
                   'empty hand.'])

    def row(y, quests):
        prev = 'start'
        for i, (slug, title, tasks, rewards, icon, desc) in enumerate(quests):
            ch.quest(slug, title, tasks, rewards, deps=[prev], icon=icon, x=2 + i * 1.75, y=y, desc=[desc])
            prev = slug

    row(-3, [
        ('fd_knife', 'Kitchen Knife', [item('farmersdelight:flint_knife')],
         [give('farmersdelight:tomato_seeds', 4), xp(20)], 'farmersdelight:flint_knife',
         '&bFarmer\'s Delight&r: knives cut crops and harvest straw from grass.'),
        ('fd_cutting_board', 'Cutting Board', [item('farmersdelight:cutting_board')],
         [give('farmersdelight:rice', 8), xp(20)], 'farmersdelight:cutting_board',
         'Use a knife on a cutting board to process ingredients.'),
        ('fd_stove', 'Stove', [item('farmersdelight:stove')],
         [give('farmersdelight:canvas', 4), xp(30)], 'farmersdelight:stove', 'A heat source for cooking.'),
        ('fd_cooking_pot', 'Cooking Pot', [item('farmersdelight:cooking_pot')],
         [give('farmersdelight:onion', 8), xp(40)], 'farmersdelight:cooking_pot',
         'Put the pot on a stove to cook soups, stews and meals.'),
        ('fd_skillet', 'Skillet', [item('farmersdelight:skillet')],
         [give('minecraft:beef', 8), xp(30)], 'farmersdelight:skillet', 'Fry food on a stove, or hit mobs with it.'),
        ('fd_rich_soil', 'Rich Soil', [item('farmersdelight:rich_soil', 8)],
         [give('farmersdelight:organic_compost', 4), xp(40)], 'farmersdelight:rich_soil',
         'Rich soil makes crops grow faster and turns mushrooms into colonies.'),
        ('fd_hamburger', 'A Proper Meal', [item('farmersdelight:hamburger')],
         [give('farmersdelight:hamburger', 4), levels(3)], 'farmersdelight:hamburger', 'Make a hamburger.'),
        ('fd_balanced_diet', 'A Balanced Diet', [adv('minecraft:husbandry/balanced_diet')],
         [give('minecraft:enchanted_golden_apple'), levels(15)], 'minecraft:golden_apple',
         'Eat every kind of vanilla food.'),
    ])

    row(-1, [
        ('ss_chest', 'Sophisticated Storage', [item('sophisticatedstorage:chest')],
         [give('minecraft:iron_ingot', 8), xp(30)], 'sophisticatedstorage:chest',
         '&bSophisticated Storage&r chests and barrels can be upgraded in tier and given upgrades.'),
        ('ss_upgrade', 'Tier Upgrade', [item('sophisticatedstorage:basic_to_iron_tier_upgrade')],
         [give('minecraft:iron_ingot', 8), xp(30)], 'sophisticatedstorage:basic_to_iron_tier_upgrade',
         'Upgrade a placed chest or barrel without emptying it.'),
        ('ss_stack', 'Stack Upgrade', [item('sophisticatedstorage:stack_upgrade_tier_1')],
         [give('minecraft:gold_ingot', 4), xp(40)], 'sophisticatedstorage:stack_upgrade_tier_1',
         'Stack upgrades multiply how many items fit in each slot.'),
        ('ss_controller', 'Storage Controller', [item('sophisticatedstorage:controller')],
         [give('sophisticatedstorage:storage_link', 4), xp(60)], 'sophisticatedstorage:controller',
         'A controller links nearby storage into one inventory.'),
        ('sb_magnet', 'Magnetic Backpack', [item('sophisticatedbackpacks:magnet_upgrade')],
         [give('minecraft:iron_ingot', 4), xp(40)], 'sophisticatedbackpacks:magnet_upgrade',
         'A magnet upgrade pulls nearby items into your backpack.'),
        ('sb_diamond', 'Diamond Backpack', [item('sophisticatedbackpacks:diamond_backpack')],
         [give('minecraft:diamond', 4), levels(5)], 'sophisticatedbackpacks:diamond_backpack',
         'A bigger backpack with more upgrade slots.'),
        ('sb_netherite', 'Netherite Backpack', [item('sophisticatedbackpacks:netherite_backpack')],
         [give('minecraft:netherite_scrap', 2), levels(10)], 'sophisticatedbackpacks:netherite_backpack',
         'The best backpack, immune to fire and lava.'),
    ])

    row(1, [
        ('sup_sack', 'Supplementaries', [item('supplementaries:sack')],
         [give('supplementaries:rope', 32), xp(20)], 'supplementaries:sack',
         '&bSupplementaries&r adds many handy blocks: sacks, jars, ropes, globes and more.'),
        ('sup_jar', 'Jar', [item('supplementaries:jar')],
         [give('minecraft:glass', 8), xp(20)], 'supplementaries:jar', 'Jars hold fluids, fireflies or items.'),
        ('sup_globe', 'Globe', [item('supplementaries:globe')],
         [give('minecraft:map', 2), xp(30)], 'supplementaries:globe', 'A spinning globe of your world.'),
        ('sup_quiver', 'Quiver', [item('supplementaries:quiver')],
         [give('minecraft:arrow', 64), xp(30)], 'supplementaries:quiver', 'Holds several stacks of arrows.'),
        ('sup_safe', 'Safe', [item('supplementaries:safe')],
         [give('minecraft:iron_ingot', 4), xp(30)], 'supplementaries:safe', 'A storage block only you can open.'),
    ])

    row(3, [
        ('quark_trowel', 'Quark', [item('quark:trowel')],
         [give('minecraft:cobblestone', 64), xp(20)], 'quark:trowel',
         '&bQuark&r adds many small features. The trowel places random blocks from your hotbar.'),
        ('quark_pickarang', 'Pickarang', [item('quark:pickarang')],
         [give('minecraft:diamond', 2), xp(30)], 'quark:pickarang', 'A boomerang that mines blocks.'),
        ('quark_seed_pouch', 'Seed Pouch', [item('quark:seed_pouch')],
         [give('minecraft:wheat_seeds', 32), xp(20)], 'quark:seed_pouch', 'Holds and plants seeds in bulk.'),
        ('quark_crate', 'Crate', [item('quark:crate')],
         [give('minecraft:oak_planks', 32), xp(20)], 'quark:crate', 'Stores many different items.'),
        ('quark_abacus', 'Abacus', [item('quark:abacus')],
         [give('minecraft:stick', 16), xp(20)], 'quark:abacus', 'Measures distances between blocks.'),
    ])

    ch.quest('all', 'Comfortable Living', [check(title='Homestead complete')],
             [give('minecraft:diamond_block'), levels(15)],
             deps=['fd_balanced_diet', 'sb_netherite', 'ss_controller', 'sup_safe', 'quark_abacus'],
             icon='minecraft:red_bed', shape='heart', size=2.0, x=17, y=0,
             subtitle='Collection complete', desc=['Your home is complete.'])
    return ch
