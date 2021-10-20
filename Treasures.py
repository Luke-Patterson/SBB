from c_Treasure import Treasure
from Effects import *
from copy import deepcopy
import random

# Book of Heroes
def Book_of_Heroes_triggered_effect(source, slain, slayer):
    slayer.change_atk_mod(1)
    slayer.change_hlth_mod(1)

Book_of_Heroes = Treasure(
    name = 'Book of Heroes',
    lvl = 2,
    abils = [
        Triggered_Effect(
            name = 'Book of Heroes Global Slay Effect',
            effect_func = Book_of_Heroes_triggered_effect,
            trigger = Trigger(
                name='Book of Heroes Global Slay Effect trigger',
                type='global slay',
                condition = lambda self, condition_obj, triggered_obj:
                    condition_obj.get_alignment() == 'Good' and
                    triggered_obj.get_alignment() == 'Evil'
            )
        )
    ]
)

# Bounty Board
def Bounty_Board_triggered_effect(source, slain, slayer):
    slayer.owner.next_turn_addl_gold += 1

Bounty_Board = Treasure(
    name = 'Bounty Board',
    lvl=2,
    abils = [
        Triggered_Effect(
            name = 'Bounty Board Global Slay Effect',
            effect_func = Bounty_Board_triggered_effect,
            trigger = Trigger(
                name='Bounty Board Global Slay Effect trigger',
                type='global slay',
                condition = lambda self, condition_obj, triggered_obj:
                    any([i.trigger.type == 'slay' for i in condition_obj.abils
                    if isinstance(i, Triggered_Effect)])
            )
        )
    ]
)

#Corrupted Heartwood
Corrupted_Heartwood_Modifier = Modifier(
    name= 'Corrupted Heartwood Modifier',
    atk_func = lambda char, atk, source: atk + 1,
    oth_func = lambda char: char.alignment_mod.append('Evil'),
    oth_reverse_func = lambda char: char.alignment_mod.remove('Evil')
)

Corrupted_Heartwood = Treasure(
    name='Corrupted Heartwood',
    lvl = 2,
    abils=[
        Global_Static_Effect(
            name = 'Corrupted Heartwood Effect',
            effect_func = lambda char: char.add_modifier(Corrupted_Heartwood_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Corrupted_Heartwood_Modifier),
            condition = lambda char: 'Animal' in char.type or 'Treefolk' in char.type
        )
    ]
)

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
    char.change_atk_mod(1)
    char.change_hlth_mod(1)

def Fairy_Tail_reverse_effect(char):
    char.change_atk_mod(-1)
    char.change_hlth_mod(-1)


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

#Needle Nose Daggers
Needle_Nose_Daggers_Modifier = Modifier(
    name= 'Needle Nose Daggers Modifier',
    atk_func = lambda char, atk, source: atk + 1
)

def Needle_Nose_Daggers_trigger_effect(source):
    if source.owner.last_combat == 'lost':
        source.owner.discard_treasure(source)

Needle_Nose_Daggers = Treasure(
    name='Needle Nose Daggers',
    lvl=2,
    abils=[
        Global_Static_Effect(
            name = 'Needle Nose Daggers Effect',
            effect_func = lambda self: self.add_modifier(Needle_Nose_Daggers_Modifier),
            reverse_effect_func = lambda self: self.remove_modifier(Needle_Nose_Daggers_Modifier)
        ),
        Triggered_Effect(
            name = 'Needle Nose Daggers destroy effect',
            effect_func = Needle_Nose_Daggers_trigger_effect,
            trigger = Trigger(
                name = 'Needle Nose Daggers trigger',
                type = 'end of combat'
            )
        )
    ]
)

Piggie_Bank = Treasure(
    name='Piggie Bank',
    lvl=2,
    # Piggie Bank ability is hardcoded into gold generation
    abils=[]
)

#Ring of Meteors
def Ring_of_Meteors_dmg_effect(source):
    for i in source.owner.board.values():
        if i != None:
            i.take_damage(1, source=source)

    for i in source.owner.opponent.board.values():
        if i != None:
            i.take_damage(1, source=source)

Ring_of_Meteors = Treasure(
    name = 'Ring of Meteors',
    lvl=2,
    abils = [
        Triggered_Effect(
            name = 'Ring of Meteors triggered effect',
            effect_func = Ring_of_Meteors_dmg_effect,
            trigger = Trigger(
                name='Ring of Meteors Effect trigger',
                type='start of combat'
            )
        )
    ]
)

#Ring of Regeneration
Ring_of_Regeneration = Treasure(
    name='Ring of Regeneration',
    lvl=2,
    abils=[
        Triggered_Effect(
            name ='Ring of Regeneration',
            trigger = Trigger(
                name = 'Ring of Regeneration Trigger',
                type = 'end of turn'
            ),
            effect_func = lambda source: source.owner.life_gain(1)
        )
    ]
)

# Rune Stones

# Secret Stash
def Secret_Stash_trigger_effect(source):
    if source.owner.last_combat == 'lost':
        source.owner.next_turn_addl_gold += 3
        source.owner.life_gain(3)
        source.owner.discard_treasure(source)

Secret_Stash = Treasure(
    name = 'Secret Stash',
    lvl=2,
    abils = [
        Triggered_Effect(
            name = 'Secret Stash destroy effect',
            effect_func = Secret_Stash_trigger_effect,
            trigger = Trigger(
                name = 'Secret Stash trigger',
                type = 'end of combat'
            )
        )
    ]
)

#Shepherd's Sling

Shepherds_Sling_Modifier = Modifier(
    name= "Shepherd's Sling Modifier",
    atk_func = lambda char, atk, source: atk + 1,
    hlth_func = lambda char, hlth, source: hlth + 1
)


Shepherds_Sling = Treasure(
    name="Shepherd's Sling",
    lvl = 2,
    abils=[
        Global_Static_Effect(
            name = "Shepherd's Sling Effect",
            effect_func = lambda char: char.add_modifier(Shepherds_Sling_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Shepherds_Sling_Modifier),
            condition = lambda char: char.lvl<=3
        )
    ]
)

#Spinning Wheel
def Spinning_Wheel_effect(source):
    source.owner.next_turn_addl_gold += 1

Spinning_Wheel = Treasure(
    name="Spinning Wheel",
    lvl=2,
    abils = [
        Triggered_Effect(
            name = "Spinning Wheel triggered ability",
            trigger = Trigger(
                name= "Spinning Wheel trigger",
                type= "start of turn"
            ),
            effect_func = Spinning_Wheel_effect
        )
    ]
)

Ancient_Sarcophagus= Treasure(
    name='Ancient Sarcophagus',
    lvl=3,
    abils=None
)

def Bad_Moon_triggered_effect(source, slain, slayer):
    slayer.change_atk_mod(1)
    slayer.change_hlth_mod(2)

Bad_Moon= Treasure(
    name='Bad Moon',
    lvl=3,
    abils=[Triggered_Effect(
        name = 'Bad Moon Global Slay Effect',
        effect_func = Bad_Moon_triggered_effect,
        trigger = Trigger(
            name='Bad Moon Global Slay Effect trigger',
            type='global slay',
            condition = lambda self, condition_obj, triggered_obj:
                any([i.trigger.type == 'slay' for i in condition_obj.abils
                if isinstance(i, Triggered_Effect)])
        )
    )]
)

Cloak_of_the_Assassin_Modifier = Modifier(
    name= 'Cloak of the Assassin Modifier',
    atk_func = lambda char, atk, source: atk + 3,
    hlth_func = lambda char, hlth, source: hlth + 3,
)


Cloak_of_the_Assassin= Treasure(
    name='Cloak of the Assassin',
    lvl=3,
    abils=[
        Global_Static_Effect(
            name = 'Cloak of the Assassin Effect',
            effect_func = lambda char: char.add_modifier(Cloak_of_the_Assassin_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Cloak_of_the_Assassin_Modifier),
            condition = lambda char: any([i.trigger.type=='slay' for i in char.abils if isinstance(i, Triggered_Effect)])
        )
    ]
)

Crystal_Ball= Treasure(
    name='Crystal Ball',
    lvl=3,
    abils=None
)


Deepstone_Mine_Modifier = Modifier(
    name= 'Deepstone Mine Modifier',
    atk_func = lambda char, atk, source: atk + 2,
    hlth_func = lambda char, hlth, source: hlth + 2,
)

Deepstone_Mine= Treasure(
    name='Deepstone Mine',
    lvl=3,
    abils=[
        Global_Static_Effect(
            name = 'Deepstone Mine Effect',
            effect_func = lambda char: char.add_modifier(Deepstone_Mine_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Deepstone_Mine_Modifier),
            condition = lambda char: 'Dwarf' in char.type
        )
    ]
)

Eye_of_Ares= Treasure(
    name='Eye of Ares',
    lvl=3,
    abils=None
)

# Fancy Pants

# Haunted Helm
Haunted_Helm_Modifier = Modifier(
    name= 'Haunted Helm Modifier',
    hlth_func = lambda char, hlth, source: hlth + 10,
)

Haunted_Helm = Treasure(
    name='Haunted Helm',
    lvl=3,
    abils=[
        Global_Static_Effect(
            name = 'Haunted Helm Effect',
            effect_func = lambda char: char.add_modifier(Haunted_Helm_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Haunted_Helm_Modifier),
            condition = lambda char: char.position==1
        )
    ]
)

def Merlins_Hat_effect(spell):
    spell.current_cost = max(0, spell.current_cost - 2)

def Merlins_Hat_reverse_effect(spell):
    spell.current_cost = spell.base_cost


# Merlin's Hat
Merlins_Hat = Treasure(
    name="Merlin's Hat",
    lvl=3,
    abils=[
        Shop_Effect(
            name="Merlin's Hat",
            spell_effect_func = Merlins_Hat_effect,
            spell_reverse_effect_func = Merlins_Hat_reverse_effect
        )
    ]
)

Power_Orb_Modifier = Modifier(
    name= 'Power Orb Modifier',
    atk_func = lambda char, atk, source: atk + 1,
    hlth_func = lambda char, hlth, source: hlth + 1,
)

Power_Orb = Treasure(
    name='Power Orb',
    lvl=3,
    abils=[
        Global_Static_Effect(
            name = 'Power Orb Effect',
            effect_func = lambda char: char.add_modifier(Power_Orb_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Power_Orb_Modifier)
        )
    ]
)

# Ring of Revenge
def Ring_of_Revenge_triggered_effect(source, dead_char):
    pos_map = {1:[5],2:[5,6],3:[6,7],4:[7]}
    if dead_char.position == None:
        position = dead_char.last_position
    else:
        position = dead_char.position
    assert position != None
    if position in pos_map.keys():
        pump_pos = pos_map[position]
        for i in pump_pos:
            if source.owner.board[i] != None:
                source.owner.board[i].change_eob_atk_mod(1)
                source.owner.board[i].change_eob_hlth_mod(1)
                if dead_char.game.verbose_lvl>=4:
                    print(source.owner.board[i],'pumped by', source)

Ring_of_Revenge = Treasure(
    name = 'Ring of Revenge',
    lvl=3,
    abils = [
        Triggered_Effect(
            name = 'Ring of Revenge Death Effect',
            effect_func = Ring_of_Revenge_triggered_effect,
            trigger = Trigger(
                name='Ring of Revenge Death Effect trigger',
                type='die'
            )
        )
    ]
)

# Sting
Sting_Modifier = Modifier(
    name= 'Sting Modifier',
    atk_func = lambda char, atk, source: atk + 10,
)
Sting = Treasure(
    name='Sting',
    lvl=3,
    abils=[
        Global_Static_Effect(
            name = 'Sting Effect',
            effect_func = lambda char: char.add_modifier(Sting_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Sting_Modifier),
            condition = lambda char: char.position==1
        )
    ]
)


Tell_Tale_Quiver_Modifier = Modifier(
    name= 'Tell Tale Quiver Modifier',
    atk_func = lambda char, atk, source: atk + 3,
    hlth_func = lambda char, hlth, source: hlth + 3,
)

# Telltale Quiver
Tell_Tale_Quiver= Treasure(
    name = 'Tell Tale Quiver',
    lvl = 3,
    abils= [
        Global_Static_Effect(
            name = 'Tell Tale Quiver Effect',
            effect_func = lambda char: char.add_modifier(Tell_Tale_Quiver_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Tell_Tale_Quiver_Modifier),
            condition = lambda char: 'ranged' in char.keyword_abils and (
                char.position==5 or char.position==6 or char.position==7)
        )
    ]
)

def Coin_of_Charron_triggered_effect(source, dead_char):
    if len(source.owner.chars_dead) <= 1:
        dead_char.change_atk_mod(4)
        dead_char.change_hlth_mod(4)

Coin_of_Charron= Treasure(
    name='Coin of Charron',
    lvl=4,
    abils = [
        Triggered_Effect(
            name = 'Coin of Charron Death Effect',
            effect_func = Coin_of_Charron_triggered_effect,
            trigger = Trigger(
                name='Coin of Charon Death Effect trigger',
                type='die'
            )
        )
    ]
)

def Deck_of_Many_Things_effect(source):
    Deck_spells = ['Falling Stars','Earthquake', 'Fireball', 'Lightning Bolt', 'Ride of the Valkyries',
        'Blessing of Athena', 'Poison Apple', 'Shrivel', 'Smite','Pigomorph']
    elig_spells = [i for i in source.owner.game.spells if i.name in Deck_spells
        and i.lvl <= source.owner.lvl]
    if elig_spells != []:
        selected = random.choice(elig_spells)
        selected.cast(source.owner, in_combat = True)

Deck_of_Many_Things= Treasure(
    name='Deck of Many Things',
    lvl=4,
    abils=[
        Triggered_Effect(
            name = "Deck of Many Things triggered ability",
            trigger = Trigger(
                name= "Deck of Many Things trigger",
                type= "start of combat"
            ),
            effect_func = Deck_of_Many_Things_effect
        )
    ]
)

Dwarven_Forge= Treasure(
    name='Dwarven Forge',
    lvl=4,
    abils=None
)

def Fools_Gold_effect(source):
    source.owner.next_turn_addl_gold += 4

def Fools_Gold_spell_effect(eff, player):
    player.spells_in_shop.append(False)

def Fools_Gold_spell_reverse_effect(eff, player):
    player.spells_in_shop.remove(False)
    import pdb; pdb.set_trace()

Fools_Gold= Treasure(
    name="Fool's Gold",
    lvl=4,
    abils=[
        Triggered_Effect(
            name = "Fool's Gold triggered ability",
            trigger = Trigger(
                name= "Fool's Gold trigger",
                type= "start of turn"
            ),
            effect_func = Fools_Gold_effect
        ),
        Player_Effect(
            name='Fools Gold Spell Effect',
            effect_func= Fools_Gold_spell_effect,
            reverse_effect_func = Fools_Gold_spell_reverse_effect
        )
    ]
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

# Hidden Cache
# Other Hand of Vekna
# Reduplicator

# Ring of Rage
Ring_of_Rage_Modifier = Modifier(
    name= 'Ring of Rage Modifier',
    atk_func = lambda char, atk, source: atk + 3
)

Ring_of_Rage= Treasure(
    name = 'Ring of Rage',
    lvl = 4,
    abils= [
        Global_Static_Effect(
            name = 'Ring of Rage Effect',
            effect_func = lambda char: char.add_modifier(Ring_of_Rage_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Ring_of_Rage_Modifier),
            condition = lambda char: (char.position==1 or char.position==2
                or char.position==3 or char.position==4)
        )
    ]
)

Sky_Castle_Modifier = Modifier(
    name= 'Sky Castle Modifier',
    atk_func = lambda char, atk, source: atk + 4,
    hlth_func = lambda char, hlth, source: hlth + 4
)

Sky_Castle = Treasure(
    name = 'Sky Castle',
    lvl = 4,
    abils = [
        Global_Static_Effect(
            name = 'Sky Castle Effect',
            effect_func = lambda char: char.add_modifier(Sky_Castle_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Sky_Castle_Modifier),
            condition = lambda char: 'Prince' in char.type or 'Princess' in char.type
        )
    ]
)

# Wild Growth

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

# Horn of Olympus
# Mimic

# Monkeys_Paw = Treasure(
#     lvl = 5,
#     abils = [
#         Global_Static_Effect(
#             name = "Monkey's Paw",
#             effect_func = lambda char: char.add_modifier(Monkeys_Paw_Modifier),
#             reverse_effect_func = lambda char: char.remove_modifier(Monkeys_Paw_Modifier),
#             condition = lambda char: any([i==None for i in char.owner.board.values()])
#         )
#     ]
# )

# Staff of the Old Toad
# Summoning Portal

Sword_of_Fire_and_Ice_Atk_Modifier = Modifier(
    name= 'Sword of Fire and Ice Attack Modifier',
    atk_func = lambda char, atk, source: atk + 5
)

Sword_of_Fire_and_Ice_Health_Modifier = Modifier(
    name= 'Sword of Fire and Ice Health Modifier',
    hlth_func = lambda char, hlth, source: hlth + 5
)

def Sword_of_Fire_and_Ice_effect(char):
    if char.position!= None and char.position>=1 and char.position<=4:
        char.add_modifier(Sword_of_Fire_and_Ice_Health_Modifier)

    if char.position!= None and char.position>=5 and char.position<=7:
        char.add_modifier(Sword_of_Fire_and_Ice_Atk_Modifier)

def Sword_of_Fire_and_Ice_reverse_effect(char):
    if Sword_of_Fire_and_Ice_Health_Modifier in char.modifiers:
        char.remove_modifier(Sword_of_Fire_and_Ice_Health_Modifier)

    if Sword_of_Fire_and_Ice_Atk_Modifier in char.modifiers:
        char.remove_modifier(Sword_of_Fire_and_Ice_Atk_Modifier)


Sword_of_Fire_and_Ice = Treasure(
    name = 'Sword of Fire and Ice',
    lvl = 2,
    abils = [
        Global_Static_Effect(
            name = 'Sword of Fire and Ice Effect',
            effect_func = Sword_of_Fire_and_Ice_effect,
            reverse_effect_func = Sword_of_Fire_and_Ice_reverse_effect
        )
    ]
)

# Tree of Life

def Embiggening_Stone_effect(char):
    char.change_atk_mod(15)
    char.change_hlth_mod(15)

def Embiggening_Stone_reverse_effect(char):
    char.change_atk_mod(-15)
    char.change_hlth_mod(-15)

Embiggening_Stone= Treasure(
    name='Embiggening Stone',
    lvl=6,
    abils=[
        Shop_Effect(
            name='Embiggening Stone Effect',
            char_effect_func = Embiggening_Stone_effect,
            char_reverse_effect_func = Embiggening_Stone_reverse_effect,
            condition = lambda char: char.lvl<=3
        )
    ]
)

Evil_Eye= Treasure(
    name='Evil Eye',
    lvl=6,
    abils=None
)

Ivory_Owl= Treasure(
    name='Ivory Owl',
    lvl=6,
    abils=None
)

Magic_Sword_100_Modifier = Modifier(
    name= 'Magic Sword +100 Modifier',
    atk_func = lambda char, atk, source: atk + 100,
)

Magic_Sword_100= Treasure(
    name='Magic Sword +100',
    lvl=6,
    abils=[
        Global_Static_Effect(
            name = 'Magic Sword +100 Effect',
            effect_func = lambda char: char.add_modifier(Magic_Sword_100_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Magic_Sword_100_Modifier),
            condition = lambda char: char.position==1
        )
    ]
)

Spear_of_Achilles= Treasure(
    name='Spear of Achilles',
    lvl=6,
    abils=None
)

The_Singing_Sword_Modifier = Modifier(
    name= 'The Singing Sword Modifier',
    atk_func = lambda char, atk, source: atk * 2
)

The_Singing_Sword= Treasure(
    name='The Singing Sword',
    lvl=6,
    abils= [
        Global_Static_Effect(
            name = 'The Singing Sword Effect',
            effect_func = lambda char: char.add_modifier(The_Singing_Sword_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(The_Singing_Sword_Modifier),
            condition = lambda char: (char.position==1 or char.position==2
                or char.position==3 or char.position==4)
        )
    ]
)

# Wand of Weirding



def Excalibur_effect(char):
    char.upgraded = True

def Excalibur_reverse_effect(char):
    char.upgraded = False

Excalibur= Treasure(
    name='Excalibur',
    lvl=7,
    abils=[
        Shop_Effect(
            name='Excalibur Effect',
            char_effect_func = Excalibur_effect,
            char_reverse_effect_func = Excalibur_reverse_effect
        )
    ]
)

Fairy_Queens_Wand_Modifier = Modifier(
    name= "Fairy Queen's Wand Modifier",
    atk_func = lambda char, atk, source: atk + 5,
    hlth_func = lambda char, hlth, source: hlth + 5,
)

Fairy_Queens_Wand= Treasure(
    name="Fairy Queen's Wand",
    lvl=7,
    abils=[
        Global_Static_Effect(
            name = "Fairy Queen's Wand Effect",
            effect_func = lambda char: char.add_modifier(Fairy_Queens_Wand_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Fairy_Queens_Wand_Modifier)
        )
    ]
)

Mirror_Mirror= Treasure(
    name='Mirror Mirror',
    lvl=7,
    abils=None
)

Phoenix_Feather= Treasure(
    name='Phoenix Feather',
    lvl=7,
    abils=None
)

The_Holy_Grail= Treasure(
    name='The Holy Grail',
    lvl=7,
    abils=None
)

The_Round_Table= Treasure(
    name='The Round Table',
    lvl=7,
    abils=None
)

objs=deepcopy(list(locals().keys()))
master_treasure_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Treasure):
        master_treasure_list.append(obj)
