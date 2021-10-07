from c_Spell import Spell
from Effects import Target
from Effects import Trigger
from Effects import Triggered_Effect
from Effects import Shop_Effect
from Characters import Character
from Characters import master_char_list
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
        selected.add_to_hand(spell.owner)
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
        selected.add_to_hand(source)

def For_Glory_effect(spell):
    effect=Triggered_Effect(
        name='For Glory triggered effect',
        effect_func = For_Glory_char_effect,
        trigger = Trigger(
            name='For Glory Effect trigger',
            type='end of turn'
        )
    )
    effect.source = spell.owner
    spell.owner.effects.append(effect)
    spell.owner.triggers.append(effect.trigger)

For_Glory = Spell(
    name = 'For Glory!',
    lvl=2,
    cost=1,
    effect = For_Glory_effect
)

def Genies_Wish_effect(spell):
    elig_spells = [i for i in spell.owner.game.spells if i.target==None and i.name!="Genie's Wish"]
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

Magic_Research_reverse_trig_effect = Triggered_Effect(
    name='Magic Research reverse effect',
    trigger=Trigger(
        name= 'Magic Research reverse effect trigger',
        type='end of turn'
    ),
    effect_func = Magic_Research_reverse_effect,
    eob=True
)

def Magic_Research_effect(spell):
    spell.selected_target.change_atk_mod(1)
    spell.selected_target.change_hlth_mod(1)
    copy = deepcopy(Magic_Research_reverse_trig_effect)
    copy.source = spell.selected_target
    spell.selected_target.owner.triggers.append(copy.trigger)

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
    spell.selected_target.permanent_transform(selected)

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

def Cats_Call_effect(spell):
    pass
# Cat's Call

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
    effect.source = spell.owner
    spell.owner.effects.append(effect)
    spell.owner.triggers.append(effect.trigger)

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
            name='Falling Starts Effect trigger',
            type='start of combat'
        )
    )
    effect.source = spell.owner
    spell.owner.effects.append(effect)
    spell.owner.triggers.append(effect.trigger)

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
    copy = source.last_opponent.first_char_dead.create_copy(source)
    copy.current_cost = 0
    copy.add_to_hand(source, store_in_shop=True)

def Kidnap_effect(spell):
    effect=Triggered_Effect(
        name='Kidnap triggered effect',
        effect_func = Kidnap_char_effect,
        trigger = Trigger(
            name='Kidnap Effect trigger',
            type='end of turn'
        )
    )
    effect.source = spell.owner
    spell.owner.effects.append(effect)
    spell.owner.triggers.append(effect.trigger)

# Kidnap
Kidnap = Spell(
    name='Kidnap',
    lvl=3,
    cost=2,
    effect = Kidnap_effect
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

objs=deepcopy(list(locals().keys()))
master_spell_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Spell):
        master_spell_list.append(obj)
