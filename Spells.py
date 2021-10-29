from c_Spell import Spell
from Effects import Effect
from Effects import Target
from Effects import Trigger
from Effects import Triggered_Effect
from Effects import Shop_Effect
from Effects import Modifier
from Characters import Character
from Characters import master_char_list
from Characters import Cat_1_1
from Characters import Pigomorph_Pig
from copy import deepcopy
import random

def Eenie_Meenie_Miney_Mo_effect(spell):
    chars = [i for i in spell.owner.shop if isinstance(i, Character)]
    if chars != []:
        selected = random.choice(chars)
        spell.owner.shop.remove(selected)
        selected.change_atk_mod(1)
        selected.change_hlth_mod(1)
        if spell.owner.game.verbose_lvl>=3:
            print('Eenie Meenie Miney Mo selects',selected)
        selected.add_to_hand(spell.owner, store_in_shop=True)
    else:
        if spell.owner.game.verbose_lvl>=3:
            print('Eenie Meenie Miney Mo has no creatures selects')



Eenie_Meenie_Miney_Mo = Spell(
    name = 'Eenie Meenie Miney Mo',
    lvl=2,
    cost=2,
    effect= Eenie_Meenie_Miney_Mo_effect
)

def Free_Roll_effect(spell):
    plyr = spell.owner
    plyr.roll_shop(free=True)

Free_Roll = Spell(
    name='Free Roll',
    lvl=2,
    cost=0,
    effect=Free_Roll_effect
)

def Forbidden_Fruit_effect(spell):
    spell.owner.current_gold +=1
    spell.owner.life_loss(2)

Forbidden_Fruit = Spell(
    name='Forbidden Fruit',
    lvl=2,
    cost=0,
    effect=Forbidden_Fruit_effect
)


def For_Glory_char_effect(source):
    if source.last_combat=='won':
        elig_pool = [i for i in source.game.char_pool if
            i.lvl==source.lvl]
        selected = random.choice(elig_pool)
        source.game.char_pool.remove(selected)
        if source.game.verbose_lvl>=3:
            print(source,'gains',selected,'from For Glory')
        selected.add_to_hand(source, store_in_shop=True)

def For_Glory_effect(spell):
    effect=Triggered_Effect(
        name='For Glory triggered effect',
        effect_func = For_Glory_char_effect,
        trigger = Trigger(
            name='For Glory Effect trigger',
            type='end of turn'
        )
    )
    effect.apply_effect(spell.owner)

For_Glory = Spell(
    name = 'For Glory!',
    lvl=2,
    cost=1,
    effect = For_Glory_effect
)

def Genies_Wish_effect(spell):
    elig_spells = [i for i in spell.owner.game.spells if i.target==None and i.name!="Genie's Wish"
        and i.spell_for_turn]
    selected = random.choice(elig_spells)
    selected.cast(spell.owner)

# Genie's Wish
Genies_Wish = Spell(
    name = "Genie's Wish",
    lvl=2,
    cost=1,
    effect = Genies_Wish_effect
)


def Magic_Research_reverse_effect(source):
    if source.owner != None and source.owner.last_combat != 'won':
        source.change_atk_mod(-1)
        source.change_hlth_mod(-1)




def Magic_Research_effect(spell):
    spell.selected_target.change_atk_mod(1)
    spell.selected_target.change_hlth_mod(1)
    copy = Magic_Research_reverse_trig_effect = Effect(
        name='Magic Research reverse effect',
        reverse_effect_func = Magic_Research_reverse_effect
    )
    copy.source = spell.selected_target
    spell.selected_target.eob_reverse_effects.append(copy)


# Magic Research
Magic_Research = Spell(
    name='Magic Research',
    lvl=2,
    cost=1,
    effect = Magic_Research_effect,
    target = Target(
        name ="Magic Research Target"
    )
)

def Shard_of_the_Ice_Queen_effect(spell):
    elig_pool = [i for i in spell.selected_target.game.char_pool if
        i.lvl==spell.selected_target.lvl and i.get_alignment() == 'Evil']
    selected = random.choice(elig_pool)
    selected.change_atk_mod(1)
    selected.change_hlth_mod(1)
    spell.selected_target.transform(selected)

# Shard of the Ice Queen
Shard_of_the_Ice_Queen = Spell(
    name = 'Shard of the Ice Queen',
    lvl=2,
    cost=0,
    effect = Shard_of_the_Ice_Queen_effect,
    target = Target(
        name ="Shard of the Ice Queen Target",
        condition = lambda char: char.get_alignment()=='Good'
    )
)

def Shrink_Spell_effect(spell):
    for i in spell.owner.shop:
        if isinstance(i, Character):
            i.current_cost = max(0, i.current_cost - 1)

Shrink_Spell=Spell(
    name='Shrink Spell',
    lvl=2,
    cost=2,
    effect = Shrink_Spell_effect
)



def Sugar_and_Spice_effect(spell):
    spell.selected_target.change_atk_mod(1)
    spell.selected_target.change_hlth_mod(1)

Sugar_and_Spice = Spell(
    name="Sugar and Spice",
    lvl=2,
    cost=1,
    effect = Sugar_and_Spice_effect,
    target = Target(
        name ="Sugar and Spice Target",
        condition = lambda char: char.get_alignment()=='Good'
    )
)


def Witchs_Brew_effect(spell):
    spell.selected_target.change_atk_mod(1)
    spell.selected_target.change_hlth_mod(1)

Witchs_Brew = Spell(
    name="Witch's Brew",
    lvl=2,
    cost=1,
    effect = Witchs_Brew_effect,
    target = Target(
        name ="Witch's Brew Target",
        condition = lambda char: char.get_alignment()=='Evil'
    )
)

def Beautys_Influence_effect(spell):
    spell.selected_target.change_hlth_mod(4)
    spell.selected_target.alignment_mod.append('Good')

Beautys_Influence = Spell(
    name = "Beauty's Influence",
    lvl=3,
    cost=1,
    effect = Beautys_Influence_effect,
    target = Target(
        name ="Beauty's Influence Target",
        condition = lambda char: char.get_alignment()=='Evil'
    )
)

def Candy_Rain_effect(spell):
    for char in spell.owner.to_hand_this_turn:
        char.change_atk_mod(1)
        char.change_hlth_mod(1)

Candy_Rain = Spell(
    name = 'Candy Rain',
    lvl=3,
    cost=0,
    effect = Candy_Rain_effect
)

def Cats_Call_summon_effect(source):
    for i in range(1,5):
        if source.board[i] == None:
            token = Cat_1_1.create_copy(source, "Cat's Call Summon")
            token.add_to_board(plyr = source, position = i)
    # remove a copy of the cats call summon effect after it's been triggered
    rm_eff = [i for i in source.effects if i.name == "Cat's Call summon effect"][0]
    rm_eff.remove_effect(source)

def Cats_Call_effect(spell):
    eff = Triggered_Effect(
        name= "Cat's Call summon effect",
        effect_func = Cats_Call_summon_effect,
        trigger=Trigger(
            name="Cat's Call Trigger",
            type='clear front row'
        ),
        eob = True
    )
    eff.apply_effect(spell.owner)


Cats_Call = Spell(
    name="Cat's Call",
    lvl=3,
    cost=2,
    effect = Cats_Call_effect
)

def Earthquake_dmg_effect(source):
    for i in range(1,5):
        if source.opponent.board[i] != None:
            source.opponent.board[i].take_damage(2, source=source)


def Earthquake_effect(spell):
    effect=Triggered_Effect(
        name = 'Earthquake triggered effect',
        effect_func = Earthquake_dmg_effect,
        trigger = Trigger(
            name='Earthquake Effect trigger',
            type='start of combat'
        )
    )
    effect.apply_effect(spell.owner)



Earthquake = Spell(
    name = 'Earthquake',
    lvl = 3,
    cost = 1,
    effect = Earthquake_effect
)

def Falling_Stars_dmg_effect(source):
    for i in range(1,8):
        if source.opponent.board[i] != None:
            source.opponent.board[i].take_damage(1, source=source)
        if source.board[i] != None:
            source.board[i].take_damage(1, source=source)

def Falling_Stars_effect(spell):
    effect=Triggered_Effect(
        name = 'Falling Stars triggered effect',
        effect_func = Falling_Stars_dmg_effect,
        trigger = Trigger(
            name='Falling Stars Effect trigger',
            type='start of combat'
        )
    )
    effect.apply_effect(spell.owner)


Falling_Stars = Spell(
    name = 'Falling Stars',
    lvl = 3,
    cost = 0,
    effect = Falling_Stars_effect
)

Flourish = Spell(
    name='Flourish',
    lvl=3,
    cost=2,
    effect = lambda spell: spell.selected_target.change_hlth_mod(6),
    target = Target(
        name ="Flourish Target",
        condition = lambda char: 'Treant' in char.type
    )
)

def Gingerbread_Party_effect(char):
    char.change_atk_mod(1)
    char.change_hlth_mod(1)

def Gingerbread_Party_reverse_effect(char):
    char.change_atk_mod(-1)
    char.change_hlth_mod(-1)

Gingerbread_Party = Spell(
    name= 'Gingerbread Party',
    lvl=3,
    cost=3,
    effect = lambda spell: spell.owner.effects.append(
        Shop_Effect(
            name='Gingerbread Party Effect',
            char_effect_func = Gingerbread_Party_effect,
            char_reverse_effect_func = Gingerbread_Party_reverse_effect
        )
    )
)

Healing_Potion = Spell(
    name='Healing Potion',
    lvl=3,
    cost=1,
    effect = lambda spell: spell.owner.life_gain(1),
    spell_for_turn = False
)

def Kidnap_char_effect(source):
    if source.last_opponent.chars_dead != []:
        copy = source.last_opponent.chars_dead[0].create_copy(source, 'Kidnap spell effect')
        copy.current_cost = 0
        copy.add_to_hand(source, store_in_shop=True)
        if source.game.verbose_lvl >=3:
            print('Kidnap creates', copy,'for',source)

def Kidnap_effect(spell):
    effect=Triggered_Effect(
        name='Kidnap triggered effect',
        effect_func = Kidnap_char_effect,
        trigger = Trigger(
            name='Kidnap Effect trigger',
            type='end of turn'
        )
    )
    effect.apply_effect(spell.owner)


# Kidnap
Kidnap = Spell(
    name='Kidnap',
    lvl=3,
    cost=2,
    effect = Kidnap_effect
)

def Lunas_Grace_effect(spell):
    spell.selected_target.change_eob_atk_mod(3)
    spell.selected_target.change_eob_hlth_mod(3)


Lunas_Grace = Spell(
    name="Luna's Grace",
    lvl=3,
    cost=1,
    effect= Lunas_Grace_effect,
    target = Target(
        name ="Luna's Grace target"
    )
)

# Mixawihizzle


Potion_of_Heroism = Spell(
    name="Potion of Heroism",
    lvl=3,
    cost=1,
    effect= lambda spell: spell.selected_target.change_eob_atk_mod(2),
    target = Target(
        name ="Potion of Heroism target"
    ),
    spell_for_turn = False
)

def Spinning_Gold_effect_func(source):
    if source.last_combat=='won':
        source.next_turn_addl_gold += 3

def Spinning_Gold_effect(spell):
    effect = Triggered_Effect(
        name = 'Spinning Gold Triggered Effect',
        effect_func = Spinning_Gold_effect_func,
        trigger = Trigger(
            name='Spinning Gold Effect trigger',
            type='end of turn'
        )
    )
    effect.apply_effect(spell.owner)

Spinning_Gold = Spell(
    name = 'Spinning Gold',
    lvl=3,
    cost=1,
    effect = Spinning_Gold_effect
)

def True_Loves_Kiss_effect(spell):
    elig_pool = [i for i in spell.owner.game.char_pool if i.lvl==min(spell.selected_target.lvl+1,6)]
    selected = random.choice(elig_pool)
    spell.selected_target.transform(selected)

True_Loves_Kiss = Spell(
    name = "True Love's Kiss",
    lvl=3,
    cost=3,
    effect = True_Loves_Kiss_effect,
    target = Target(
        name ="True Love's Kiss target"
    )
)

Turkish_Delight = Spell(
    name = 'Turkish Delight',
    lvl=3,
    cost=4,
    effect = lambda spell: spell.owner.gain_exp(1)
)


def Wish_Upon_A_Star_effect_func(source):
    if source.last_combat=='won':
        source.gain_exp(1)
    rm_eff = [i for i in source.effects if i.name == "Wish Upon a Star Triggered Effect"][0]
    rm_eff.remove_effect(source)

def Wish_Upon_A_Star_effect(spell):
    spell.owner.gain_exp(1)
    effect = Triggered_Effect(
        name = 'Wish Upon a Star Triggered Effect',
        effect_func = Wish_Upon_A_Star_effect_func,
        trigger = Trigger(
            name='Wish Upon a Star Effect trigger',
            type='end of turn'
        )
    )
    effect.apply_effect(spell.owner)


Wish_Upon_A_Star= Spell(
    name='Wish Upon a Star',
    lvl=3,
    cost=5,
    effect= Wish_Upon_A_Star_effect
)


def Worm_Root_effect(spell):
    spell.selected_target.change_hlth_mod(3)
    spell.selected_target.change_atk_mod(3)

Worm_Root = Spell(
    name = "Worm Root",
    lvl=3,
    cost=2,
    effect = Worm_Root_effect,
    target = Target(
        name ="Worm Root Target",
        condition = lambda char: 'Monster' in char.type
    )
)

def Blessing_of_Athena_effect(spell):
    for i in spell.owner.hand:
        i.change_atk_mod(1)
        i.change_hlth_mod(1)

def Blessing_of_Athena_battle_effect(spell):
    for i in spell.owner.board.values():
        if i!= None:
            i.change_atk_mod(1)
            i.change_hlth_mod(1)

Blessing_of_Athena = Spell(
    name="Blessing of Athena",
    lvl=4,
    cost=4,
    effect = Blessing_of_Athena_effect,
    battle_effect = Blessing_of_Athena_battle_effect
)

def Burning_Palm_effect(spell):
    spell.selected_target.change_atk_mod(3)

Burning_Palm = Spell(
    name = 'Burning Palm',
    lvl=4,
    cost=2,
    effect = Burning_Palm_effect,
    target = Target(
        name ="Burning Palm Target"
    )
)

def Feed_the_Kraken_effect(spell):
    spell.owner.current_gold += 2
    spell.selected_target.remove_from_hand()

Feed_the_Kraken = Spell(
    name = 'Feed the Kraken',
    lvl=4,
    cost=0,
    effect = Feed_the_Kraken_effect,
    target = Target(
        name ="Feed the Kraken Target"
    )
)

def Fireball_dmg_effect(source):
    front_pos = [i for i in range(1,5) if source.opponent.board[i]!= None]
    if front_pos != []:
        selected = random.choice(front_pos)
        source.opponent.board[selected].take_damage(4, source=source)
        back_targets = {1:[5], 2:(5,6), 3:(6,7), 4:[7]}
        for i in back_targets[selected]:
            if source.opponent.board[i] != None:
                source.opponent.board[i].take_damage(4, source=source)

def Fireball_effect(spell):
    effect=Triggered_Effect(
        name = 'Fireball triggered effect',
        effect_func = Fireball_dmg_effect,
        trigger = Trigger(
            name='Fireball Effect trigger',
            type='start of combat'
        )
    )
    effect.apply_effect(spell.owner)

Fireball = Spell(
    name='Fireball',
    lvl=4,
    cost=1,
    effect = Fireball_effect
)

def Hi_Ho_effect(spell):
    elig_pool = [i for i in spell.owner.game.char_pool if 'Dwarf' in i.type]
    selected = random.choice(elig_pool)
    spell.owner.game.char_pool.remove(selected)
    if spell.owner.game.verbose_lvl>=3:
        print(spell.owner,'gains',selected,'from Hi Ho!')
    selected.add_to_hand(spell.owner, store_in_shop=True)
    dwarves = [i for i in spell.owner.hand if 'Dwarf' in i.type]
    for i in dwarves:
        i.change_atk_mod(1)
        i.change_hlth_mod(1)

Hi_Ho = Spell(
    name = 'Hi Ho!',
    lvl=4,
    cost=4,
    effect = Hi_Ho_effect
)

def Lightning_Bolt_dmg_effect(source):
    back_pos = [i for i in range(5,8) if source.opponent.board[i]!= None]
    if back_pos != []:
        selected = random.choice(back_pos)
        source.opponent.board[selected].take_damage(10, source=source)

def Lightning_Bolt_effect(spell):
    effect=Triggered_Effect(
        name = 'Lightning Bolt triggered effect',
        effect_func = Lightning_Bolt_dmg_effect,
        trigger = Trigger(
            name='Lightning Bolt Effect trigger',
            type='start of combat'
        )
    )
    effect.apply_effect(spell.owner)

Lightning_Bolt = Spell(
    name='Lightning Bolt',
    lvl=4,
    cost=2,
    effect = Lightning_Bolt_effect
)

def Masquerade_Ball_effect(spell):
    lvl_of_shop = [i.lvl for i in spell.owner.shop if isinstance(i, Character)]
    for i in spell.owner.shop:
        i.scrub_buffs(eob_only=False)
        i.owner = None
        if isinstance(i, Character) and i.inshop:
            spell.owner.game.add_to_char_pool(i)

    spell.owner.shop=[]
    game = spell.owner.game
    lvl_of_shop = [min(6, i+1) for i in lvl_of_shop]
    shop=[]
    for lvl in lvl_of_shop:
        elig_pool = [i for i in game.char_pool if i.lvl == lvl and i not in shop]
        choice = random.choice(elig_pool)
        elig_pool.remove(choice)
        shop.append(choice)
    for i in shop:
        game.char_pool.remove(i)
        i.owner = spell.owner
        i.set_zone('shop')

    spell.owner.shop=shop

    for eff in spell.owner.effects:
        if isinstance(eff, Shop_Effect):
            for obj in spell.owner.shop:
                eff.apply_effect(obj)

Masquerade_Ball = Spell(
    name = 'Masquerade Ball',
    lvl=4,
    cost=2,
    effect = Masquerade_Ball_effect
)

def Merlins_Test_reverse_effect(source):
    if source.owner != None and source.owner.last_combat != 'won':
        source.change_atk_mod(-4)
        source.change_hlth_mod(-4)

def Merlins_Test_effect(spell):
    spell.selected_target.change_atk_mod(4)
    spell.selected_target.change_hlth_mod(4)
    copy = Effect(
        name="Merlin's Test reverse effect",
        reverse_effect_func = Merlins_Test_reverse_effect
    )
    copy.source = spell.selected_target
    spell.selected_target.eob_reverse_effects.append(copy)



Merlins_Test = Spell(
    name="Merlin's Test",
    lvl=4,
    cost=3,
    effect = Merlins_Test_effect,
    target = Target(
        name ="Merlin's Test Target"
    )
)

def Queens_Grace_effect(spell):
    spell.selected_target.change_eob_atk_mod(7)
    spell.selected_target.change_eob_hlth_mod(7)

Queens_Grace = Spell(
    name="Queen's Grace",
    lvl=4,
    cost=2,
    effect = Queens_Grace_effect,
    target = Target(
        name ="Queen's Grace target",
        condition = lambda char: 'Prince' in char.type or 'Princess' in char.type
    )
)


def Ride_of_the_Valkyries_effect(spell):
    for i in spell.owner.hand:
        i.change_eob_atk_mod(3)

Ride_of_the_Valkyries = Spell(
    name= "Ride of the Valkyries",
    lvl=4,
    cost=2,
    effect = Ride_of_the_Valkyries_effect
)

def Stoneskin_effect(spell):
    spell.selected_target.change_hlth_mod(3)


Stoneskin = Spell(
    name = 'Stoneskin',
    lvl=4,
    cost=2,
    effect = Stoneskin_effect,
    target = Target(
        name ="Stoneskin Target"
    )
)

def The_End_effect(spell):
    spell.owner.gain_exp(1)
    spell.selected_target.remove_from_hand()

The_End = Spell(
    name='The End',
    lvl=4,
    cost=3,
    effect = The_End_effect,
    target = Target(
        name ="The End Target"
    )
)

def Toil_and_Trouble_effect(spell):
    if len(spell.owner.hand)>=2:
        selected = random.sample(spell.owner.hand, 2)
    elif len(spell.owner.hand)==1:
        selected = [spell.owner.hand[0]]
    else:
        return
    for i in selected:
        i.change_atk_mod(2)
        i.change_hlth_mod(2)

Toil_and_Trouble = Spell(
    name='Toil and Trouble',
    lvl=4,
    cost=2,
    effect = Toil_and_Trouble_effect
)

def Lucky_Coin_effect(spell):
    spell.owner.current_gold += 1

Lucky_Coin = Spell(
    name= 'Lucky Coin',
    lvl=5,
    cost=0,
    effect = Lucky_Coin_effect,
    spell_for_turn=False
)

def Poison_Apple_dmg_effect(source):
    if any([i !=None for i in source.opponent.board.values()]):
        selected = random.choice([i for i in source.opponent.board.values() if i != None])
        hlth_mod = (selected.hlth() - 1) * -1
        selected.change_eob_hlth_mod(hlth_mod)

def Poison_Apple_effect(spell):
    effect=Triggered_Effect(
        name = 'Poison Apple triggered effect',
        effect_func = Poison_Apple_dmg_effect,
        trigger = Trigger(
            name='Poison Apple Effect trigger',
            type='start of combat'
        )
    )
    effect.apply_effect(spell.owner)

Poison_Apple = Spell(
    name = 'Poison Apple',
    lvl=5,
    cost=2,
    effect= Poison_Apple_effect
)

def Shrivel_dmg_effect(source):
    if any([i !=None for i in source.opponent.board.values()]):
        selected = random.choice([i for i in source.opponent.board.values() if i != None])
        selected.change_eob_atk_mod(-12)
        selected.change_eob_hlth_mod(-12)


def Shrivel_effect(spell):
    effect=Triggered_Effect(
        name = 'Shrivel triggered effect',
        effect_func = Shrivel_dmg_effect,
        trigger = Trigger(
            name='Shrivel Effect trigger',
            type='start of combat'
        )
    )
    effect.apply_effect(spell.owner)

Shrivel = Spell(
    name='Shrivel',
    lvl=5,
    cost=2,
    effect=Shrivel_effect
)

def Drink_Me_Potion_effect(spell):
    for i in spell.owner.shop:
        i.scrub_buffs(eob_only=False)
        i.owner = None
        if isinstance(i, Character) and i.inshop:
            spell.owner.game.add_to_char_pool(i)

    spell.owner.shop = []

    elig_spell_pool = [i for i in spell.owner.game.spells if i.lvl <= spell.owner.lvl]
    spell.owner.shop = random.sample(list(elig_spell_pool),6)

    for eff in spell.owner.effects:
        if isinstance(eff, Shop_Effect):
            for obj in spell.owner.shop:
                eff.apply_effect(obj)


Drink_Me_Potion = Spell(
    name = 'Drink Me Potion',
    lvl=6,
    cost = 1,
    effect = Drink_Me_Potion_effect,
    spell_for_turn = False
)

def Evil_Twin_effect(spell):
    selected = spell.selected_target
    copy = selected.create_copy(spell.owner, 'Evil Twin copy', plain_copy=True)
    copy.alignment = 'Evil'
    copy.add_to_hand(spell.owner, store_in_shop=True)

Evil_Twin = Spell(
    name="Evil Twin",
    lvl=6,
    cost=8,
    effect = Evil_Twin_effect,
    target = Target(
        name ="Evil Twin Target",
        condition = lambda char: char.get_alignment()=='Good'
    )
)

def Fog_begin_combat_effect(source):
    for i in source.opponent.board.values():
        if i!= None and i.ranged:
            atk_mod = round(i.atk() / 2) * -1
            i.change_eob_atk_mod(atk_mod)

def Fog_effect(spell):
    effect=Triggered_Effect(
        name = 'Fog triggered effect',
        effect_func = Fog_begin_combat_effect,
        trigger = Trigger(
            name='Fog Effect trigger',
            type='start of combat'
        )
    )
    effect.apply_effect(spell.owner)

Fog = Spell(
    name = 'Fog',
    lvl=6,
    cost=2,
    effect = Fog_effect
)

def Gigantify_effect(spell):
    spell.selected_target.change_hlth_mod(10)

Gigantify = Spell(
    name = 'Gigantify',
    lvl=6,
    cost=5,
    effect = Gigantify_effect,
    target = Target(
        name ="Gigantify Target"
    )
)

def Hugeify_effect(spell):
    spell.selected_target.change_atk_mod(10)

Hugeify = Spell(
    name = 'Hugeify',
    lvl=6,
    cost=5,
    effect = Hugeify_effect,
    target = Target(
        name ="Hugeify Target"
    )
)

# It was all a dream

def Knighthood_effect(spell):
    spell.selected_target.upgraded = True

Knighthood = Spell(
    name = 'Knighthood',
    lvl = 6,
    cost =12,
    effect = Knighthood_effect,
    target = Target(
        name ="Knighthood Target",
        condition = lambda char: char.upgraded==False
    )
)

# Pigomorph
def Pigomorph_transform_effect(source):
    if any([i !=None for i in source.opponent.board.values()]):
        selected = random.choice([i for i in source.opponent.board.values() if i != None])
        token = Pigomorph_Pig.create_copy(source.opponent, 'Pigomorph attack effect')
        selected.transform(token, preserve_mods = False, temporary = True)

def Pigomorph_effect(spell):
    effect=Triggered_Effect(
        name = 'Pigomorph triggered effect',
        effect_func = Pigomorph_transform_effect,
        trigger = Trigger(
            name='Pigomorph Effect trigger',
            type='start of combat'
        )
    )
    effect.apply_effect(spell.owner)

Pigomorph = Spell(
    name='Pigomorph',
    lvl =6,
    cost=5,
    effect= Pigomorph_effect
)

def Smite_dmg_effect(source):
    if any([i !=None for i in source.opponent.board.values()]):
        selected = random.choice([i for i in source.opponent.board.values() if i != None])
        selected.take_damage(30, source=source)

def Smite_effect(spell):
    effect=Triggered_Effect(
        name = 'Smite triggered effect',
        effect_func = Smite_dmg_effect,
        trigger = Trigger(
            name='Smite Effect trigger',
            type='start of combat'
        )
    )
    effect.apply_effect(spell.owner)

Smite = Spell(
    name = 'Smite',
    lvl=6,
    cost=3,
    effect = Smite_effect
)

objs=deepcopy(list(locals().keys()))
master_spell_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Spell):
        master_spell_list.append(obj)
