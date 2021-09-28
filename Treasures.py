from c_Treasure import Treasure
from Effects import *
from copy import deepcopy
import random

Crown_of_Atlas_Modifier = Modifier(
    name= 'Crown of Atlas Modifier',
    atk_func = lambda char, atk, source: atk + 1,
    hlth_func = lambda char, hlth, source: hlth + 1,
    oth_func = lambda char: char.alignment_mod.append('Good'),
    oth_reverse_func = lambda char: char.alignment_mod.remove('Good')
)


Crown_of_Atlas = Treasure(
    name='Crown of Atlas',
    lvl = 2,
    abils=[
        Global_Static_Effect(
            name = 'Crown of Atlas Effect',
            effect_func = lambda char: char.add_modifier(Crown_of_Atlas_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Crown_of_Atlas_Modifier),
            condition = lambda char: 'Animal' in char.type
        )
    ]
)

Dancing_Sword_Modifier = Modifier(
    name= 'Dancing Sword Modifier',
    atk_func = lambda char, atk, source: atk + 1
)

Dancing_Sword = Treasure(
    name='Dancing Sword',
    lvl=2,
    abils=[
        Global_Static_Effect(
            name = 'Dancing Sword Effect',
            effect_func = lambda self: self.add_modifier(Dancing_Sword_Modifier),
            reverse_effect_func = lambda self: self.remove_modifier(Dancing_Sword_Modifier)
        )
    ]
)
Dark_Contract_Modifier = Modifier(
    name='Dark Contract Modifier',
    atk_func = lambda char, atk, source: atk + 5,
    hlth_func = lambda char, hlth, source: hlth + 5,
    eob = True
)

Dark_Contract = Treasure(
    name='Dark Contract',
    lvl=2,
    abils=[
        Purchase_Effect(
            name = 'Dark Contract Effect',
            effect_func = lambda char, eff: char.add_modifier(Dark_Contract_Modifier),
            condition = lambda char: char.get_alignment()=='Evil'
        )
    ]
)


Dragon_Nest_Modifier = Modifier(
    name= 'Dragon Nest Modifier',
    atk_func = lambda char, atk, source: atk + 5,
    hlth_func = lambda char, hlth, source: hlth + 5
)

Dragon_Nest = Treasure(
    name='Dragon Nest',
    lvl=2,
    abils=[
        Global_Static_Effect(
            name = 'Dragon Effect',
            effect_func = lambda char: char.add_modifier(Dragon_Nest_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Dragon_Nest_Modifier),
            condition = lambda char: 'Dragon' in char.type
        )
    ]
)

def Fairy_Tail_effect(char):
    char.atk_mod+=1
    char.hlth_mod+=1

def Fairy_Tail_reverse_effect(char):
    char.atk_mod-=1
    char.hlth_mod-=1


Fairy_Tail = Treasure(
    name='Fairy Tail',
    lvl=2,
    abils=[
        Shop_Effect(
            name='Fairy Tail Effect',
            char_effect_func = Fairy_Tail_effect,
            char_reverse_effect_func = Fairy_Tail_reverse_effect
        )
    ]
)

Fountain_of_Youth_Modifier = Modifier(
    name= 'Fountain of Youth Modifier',
    hlth_func = lambda char, hlth, source: hlth + 1
)

Fountain_of_Youth = Treasure(
    name='Fountain of Youth',
    lvl=2,
    abils=[
        Global_Static_Effect(
            name = 'Fountain of Youth Effect',
            effect_func = lambda self: self.add_modifier(Fountain_of_Youth_Modifier),
            reverse_effect_func = lambda self: self.remove_modifier(Fountain_of_Youth_Modifier)
        )
    ]
)

Hermes_Boots = Treasure(
    name="Hermes' Boots",
    lvl=2,
    abils=[]
    # ability hard coded into combat first player selection
)

Jacks_Jumping_Beans_Modifier = Modifier(
    name="Jack's Jumping Beans",
    atk_func = lambda char, atk, source: atk + 4,
    hlth_func = lambda char, hlth, source: hlth + 4,
    eob = True
)
def Jacks_Jumping_Beans_effect(source):
    if len([i for i in source.owner.board.values() if i!=None])>0:
        selected = random.choice([i for i in source.owner.board.values() if i!=None])
        selected.add_modifier(Jacks_Jumping_Beans_Modifier)

Jacks_Jumping_Beans = Treasure(
    name="Jack's Jumping Beans",
    lvl=2,
    abils = [
        Triggered_Effect(
            name = "Jack's Jumping Beans triggered ability",
            trigger = Trigger(
                name= "Jack's Jumping Beans trigger",
                type= "start of combat"
            ),
            effect_func = Jacks_Jumping_Beans_effect
        )
    ]
)

def Locked_Chest_effect(source):
    source.abils[0].counter = source.abils[0].counter - 1
    assert source.abils[0].counter >= 0
    if source.abils[0].counter == 0:
        plyr = source.owner
        source.owner.discard_treasure(source)
        plyr.select_treasure(lvl=3)

Locked_Chest = Treasure(
    name = "Locked Chest",
    lvl = 2,
    abils = [
        Triggered_Effect(
            name ='Locked Chest Counter',
            trigger = Trigger(
                name = 'Locked Chest Trigger',
                type = 'end of turn'
            ),
            effect_func = Locked_Chest_effect,
            counter = 3
        )
    ]
)

Monster_Manual = Treasure(
    name = 'Monster Manual',
    lvl = 2,
    abils = None
)

Ancient_Sarcophagus= Treasure(
    name='Ancient Sarcophagus',
    lvl=3,
    abils=None
)

Bad_Moon= Treasure(
    name='Bad Moon',
    lvl=3,
    abils=None
)

Cloak_of_the_Assassin= Treasure(
    name='Cloak of the Assassin',
    lvl=3,
    abils=None
)

Crystal_Ball= Treasure(
    name='Crystal Ball',
    lvl=3,
    abils=None
)

Deepstone_Mine= Treasure(
    name='Deepstone Mine',
    lvl=3,
    abils=None
)

Eye_of_Ares= Treasure(
    name='Eye of Ares',
    lvl=3,
    abils=None
)

Coin_of_Charron= Treasure(
    name='Coin of Charron',
    lvl=4,
    abils=None
)

Deck_of_Many_Things= Treasure(
    name='Deck of Many Things',
    lvl=4,
    abils=None
)

Dwarven_Forge= Treasure(
    name='Dwarven Forge',
    lvl=4,
    abils=None
)

Fools_Gold= Treasure(
    name="Fool's Gold",
    lvl=4,
    abils=None
)

Forking_Rod= Treasure(
    name='Forking Rod',
    lvl=4,
    abils=None
)

Gloves_of_Thieving= Treasure(
    name='Gloves of Thieving',
    lvl=4,
    abils=None
)

Ambrosia= Treasure(
    name='Ambrosia',
    lvl=5,
    abils=None
)

Draculas_Saber= Treasure(
    name="Dracula's Saber",
    lvl=5,
    abils=None
)

Exploding_Mittens= Treasure(
    name='Exploding Mittens',
    lvl=5,
    abils=None
)

Hand_of_Midas= Treasure(
    name='Hand of Midas',
    lvl=5,
    abils=None
)

Harvest_Moon= Treasure(
    name='Harvest Moon',
    lvl=5,
    abils=None
)

Helm_of_the_Ugly_Gosling= Treasure(
    name='Helm of the Ugly Gosling',
    lvl=5,
    abils=None
)


objs=deepcopy(list(locals().keys()))
master_treasure_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Treasure):
        master_treasure_list.append(obj)
