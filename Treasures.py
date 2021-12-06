from c_Treasure import Treasure
from Effects import *
from copy import deepcopy
import random
import pandas as pd

# Book of Heroes
def Book_of_Heroes_triggered_effect(source, slain, slayer):
    slayer.change_atk_mod(1)
    slayer.change_hlth_mod(2)

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
                    triggered_obj != None and
                    condition_obj != None and
                    condition_obj.check_alignment('Good') and
                    triggered_obj.check_alignment('Evil')
            )
        )
    ]
)

# Bounty Board
def Bounty_Board_triggered_effect(source, slain, slayer):
    slayer.get_owner().next_turn_addl_gold += 1

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

def Dark_Contract_effect(char, eff):
    char.change_eob_atk_mod(5)
    char.change_eob_hlth_mod(5)

Dark_Contract = Treasure(
    name='Dark Contract',
    lvl=2,
    abils=[
        Purchase_Effect(
            name = 'Dark Contract Effect',
            effect_func = Dark_Contract_effect,
            condition = lambda char: char.check_alignment('Evil')
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

def Jacks_Jumping_Beans_effect(source):
    if len([i for i in source.get_owner().board.values() if i!=None])>0:
        selected = random.choice([i for i in source.get_owner().board.values() if i!=None])
        selected.change_eob_atk_mod(4)
        selected.change_eob_hlth_mod

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
    plyr = source.owner
    plyr.select_treasure(lvl=3, max_lim= 4)

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

def Monster_Manual_triggered_effect(source, dead_char):
    dead_char.change_atk_mod(2)

Monster_Manual = Treasure(
    name = 'Monster Manual',
    lvl = 2,
    abils = [
        Triggered_Effect(
            name = 'Monster Manual Death Effect',
            effect_func = Monster_Manual_triggered_effect,
            trigger = Trigger(
                name='Monster Manual Death Effect trigger',
                type='die',
                condition = lambda self, char: 'Monster' in char.type
            )
        )
    ]
)

#Needle Nose Daggers
Needle_Nose_Daggers_Modifier = Modifier(
    name= 'Needle Nose Daggers Modifier',
    atk_func = lambda char, atk, source: atk + 2
)

def Needle_Nose_Daggers_trigger_effect(source):
    if source.get_owner().last_combat == 'lost':
        source.get_owner().discard_treasure(source)

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
                type = 'end of combat',

            ),
            multi_ignore = True
        )
    ]
)

Noble_Steed_Modifier = Modifier(
    name= "Noble Steed Modifier",
    atk_func = lambda char, atk, source: atk + 1,
    hlth_func = lambda char, hlth, source: hlth + 1
)


Noble_Steed = Treasure(
    name= 'Noble Steed',
    lvl = 2,
    abils=[
        # treasure boosting effect is hardcoded into quest resolution
        Global_Static_Effect(
            name = "Noble Steed Pump Effect",
            effect_func = lambda char: char.add_modifier(Noble_Steed_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Noble_Steed_Modifier),
            condition = lambda char: any([i.type == 'Quest' for i in char.abils])
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
    for i in source.get_owner().board.values():
        if i != None:
            i.take_damage(1, source=source)

    for i in source.get_owner().opponent.board.values():
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
            effect_func = lambda source: source.get_owner().life_gain(1)
        )
    ]
)

# Rune Stones
def Rune_Stones_trigger_effect(source):
    if source.owner != None:
        source.get_owner().discard_treasure(source)

Rune_Stones = Treasure(
    name = 'Rune Stones',
    lvl = 2,
    abils = [
        Treasure_Level_Mod(
            name='Rune Stones treasure level effect',
            effect_func= lambda base_lvl: base_lvl + 1
        ),
        Triggered_Effect(
            name = 'Rune Stones destroy effect',
            effect_func = Rune_Stones_trigger_effect,
            trigger = Trigger(
                name = 'Rune Stones trigger',
                type = 'gain treasure'
            )
        )
    ]
)

# Secret Stash
def Secret_Stash_trigger_effect(source):
    # doing this because owner could be None if trigger effect is multiplied
    if source.owner != None:
        owner = source.owner
    else:
        owner = source.last_owner

    if owner.last_combat == 'lost':
        owner.next_turn_addl_gold += 3
        owner.life_gain(3)
        if source.owner != None:
            source.get_owner().discard_treasure(source)

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
    source.get_owner().next_turn_addl_gold += 1

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

def Ancient_Sarcophagus_triggered_effect(source, dead_char):
    opp_chars = [i for i in source.get_owner().opponent.board.values() if i != None]
    if opp_chars != []:
        selected = random.choice(opp_chars)
        selected.take_damage(3, source=source)

Ancient_Sarcophagus= Treasure(
    name='Ancient Sarcophagus',
    lvl=3,
    abils=[
        Triggered_Effect(
            name = 'Ancient Sarcophagus Death Effect',
            effect_func = Ancient_Sarcophagus_triggered_effect,
            trigger = Trigger(
                name='Ancient Sarcophagus Death Effect trigger',
                type='die',
                condition = lambda self, char: char.check_alignment('Evil')
            )
        )
    ]
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

def Crystal_Ball_func(source, targeted):
    elig_spell_pool = [i for i in source.game.spells if i.lvl <= source.get_owner().lvl]
    selected = random.choice(list(elig_spell_pool))
    if len(source.get_owner().shop) < 7:
        source.get_owner().shop.append(selected)
        for eff in source.get_owner().effects:
            if isinstance(eff, Shop_Effect):
                eff.apply_effect(selected)

Crystal_Ball= Treasure(
    name='Crystal Ball',
    lvl=3,
    abils=[
        Triggered_Effect(
            name='Crystal Ball Target Effect',
            effect_func = Crystal_Ball_func,
            trigger = Trigger(
                name = 'Crystal Ball Target trigger',
                type = 'target'
            ),
        )
    ]
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

Eye_of_Ares_Modifier = Modifier(
    name= 'Eye of Ares Modifier',
    atk_func = lambda char, atk, source: atk + 5
)

def Eye_of_Ares_opp_effect(source):
    opp_effect = Global_Static_Effect(
        name = 'Eye of Ares Opponent Effect',
        effect_func = lambda self: self.add_modifier(Eye_of_Ares_Modifier),
        reverse_effect_func = lambda self: self.remove_modifier(Eye_of_Ares_Modifier),
        eob=True
    )
    source.get_owner().opponent.effects.append(opp_effect)

Eye_of_Ares= Treasure(
    name='Eye of Ares',
    lvl=3,
    abils=[
        Global_Static_Effect(
            name = 'Eye of Ares Effect',
            effect_func = lambda self: self.add_modifier(Eye_of_Ares_Modifier),
            reverse_effect_func = lambda self: self.remove_modifier(Eye_of_Ares_Modifier)
        ),
        Triggered_Effect(
            name = 'Eye of Ares give opponent effect',
            effect_func = Eye_of_Ares_opp_effect,
            trigger = Trigger(
                name='Eye of Ares give opponent trigger',
                type='start of combat'
            )
        )
    ]
)

# Fancy Pants
def Fancy_Pants_effect(char, eff):
    char.change_atk_mod(2)
    char.change_hlth_mod(2)

Fancy_Pants = Treasure(
    name='Fancy Pants',
    lvl=3,
    abils=[
        Purchase_Effect(
            name = 'Fancy Pants Effect',
            effect_func = Fancy_Pants_effect,
            once_per_turn = True,
        )
    ]
)


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
            name="Merlin's Hat shop effect",
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
            if source.get_owner().board[i] != None:
                source.get_owner().board[i].change_eob_atk_mod(1)
                source.get_owner().board[i].change_eob_hlth_mod(1)
                if dead_char.game.verbose_lvl>=4:
                    print(source.get_owner().board[i],'pumped by', source)

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

# Treasure Map
def Treasure_Map_trigger_effect(source):
    if source.owner != None:
        source.get_owner().discard_treasure(source)

Treasure_Map = Treasure(
    name = 'Treasure Map',
    lvl = 2,
    abils = [
        Treasure_Level_Mod(
            name='Treasure Map treasure level effect',
            effect_func= lambda base_lvl: base_lvl + 2
        ),
        Triggered_Effect(
            name = 'Treasure Map destroy effect',
            effect_func = Treasure_Map_trigger_effect,
            trigger = Trigger(
                name = 'Treasure Map trigger',
                type = 'gain treasure'
            )
        )
    ]
)

def Coin_of_Charron_triggered_effect(source, dead_char):
    if len(source.get_owner().chars_dead) <= 1:
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
                type='die',
                condition = lambda self, char: char.lvl > 1
            )
        )
    ]
)

def Deck_of_Many_Things_effect(source):
    Deck_spells = ['Falling Stars','Earthquake', 'Fireball', 'Lightning Bolt', 'Ride of the Valkyries',
        'Blessing of Athena', 'Poison Apple', 'Shrivel', 'Smite','Pigomorph']
    elig_spells = [i for i in source.get_owner().game.spells if i.name in Deck_spells
        and i.lvl <= source.get_owner().lvl]
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
    abils=[
        Upgrade_Reduce_Effect(
            name = 'Dwarven Forge upgrade reduce effect',
            condition = lambda char: 'Dwarf' in char.type
        )
    ]
)

def Fools_Gold_effect(source):
    source.get_owner().next_turn_addl_gold += 4

def Fools_Gold_spell_effect(eff, player):
    player.spells_in_shop.append(False)

def Fools_Gold_spell_reverse_effect(eff, player):
    player.spells_in_shop.remove(False)

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
    abils=[
        Spell_Multiplier(
            name = 'Forking Rod Spell Multiplier',
            condition = lambda spell: spell.current_cost <= 2
        )
    ]
)



def Gloves_of_Thieving_trigger_effect(source):
    dead_chars = [i for i in source.get_owner().last_opponent.chars_dead if i.lvl > 1]
    if dead_chars  != []:
        copy = dead_chars[0].create_copy(source.owner, 'Gloves of Thieving spell effect')
        copy.current_cost = 0
        copy.add_to_hand(source.owner, store_in_shop=True)
        if source.get_owner().game.verbose_lvl >=3:
            print('Gloves of Thieving creates', copy,'for',source.owner)

Gloves_of_Thieving= Treasure(
    name='Gloves of Thieving',
    lvl=4,
    abils=[
        Triggered_Effect(
            name = 'Gloves of Thieving effect',
            effect_func = Gloves_of_Thieving_trigger_effect,
            trigger = Trigger(
                name = 'Gloves of Thieving trigger',
                type = 'end of combat'
            )
        )
    ]
)

# Hidden Cache
def Hidden_Cache_trigger_effect(source):
    if any([i != None for i in source.get_owner().board.values()]):
        selected = random.choice([i for i in source.get_owner().board.values() if i != None])
        selected.change_atk_mod(3)
        selected.change_hlth_mod(3)
    else:
        source.get_owner().next_turn_addl_gold += 3

Hidden_Cache= Treasure(
    name='Hidden Cache',
    lvl=4,
    abils=[
        Triggered_Effect(
            name = 'Hidden Cache effect',
            effect_func = Hidden_Cache_trigger_effect,
            trigger = Trigger(
                name = 'Hidden Cache trigger',
                type = 'end of combat'
            )
        )
    ]
)

Moonsong_Horn_Modifier = Modifier(
    name= 'Moonsong Horn Modifier',
    atk_func = lambda char, atk, source: atk + 1,
    hlth_func = lambda char, hlth, source: hlth + 1,
)

def Moonsong_Horn_effect(spell):
    spell.current_cost = max(0, spell.current_cost - 1)

def Moonsong_Horn_reverse_effect(spell):
    spell.current_cost = spell.base_cost


Moonsong_Horn = Treasure(
    name = 'Moonsong Horn',
    lvl = 4,
    abils=[
        Global_Static_Effect(
            name = 'Moonsong Horn Pump Effect',
            effect_func = lambda char: char.add_modifier(Moonsong_Horn_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Moonsong_Horn_Modifier)
        ),
        Shop_Effect(
            name="Moonsong Horn shop effect",
            spell_effect_func = Moonsong_Horn_effect,
            spell_reverse_effect_func = Moonsong_Horn_reverse_effect
        )
    ]
)

def Other_Hand_of_Vekna_triggered_effect(source, dead_char):
    pos_map = {1:[1,2,3,4],
        2:[1,2,3,4],
        3:[1,2,3,4],
        4:[1,2,3,4],
        5:[5,6,7],
        6:[5,6,7],
        7:[5,6,7]}
    if dead_char.position == None:
        position = dead_char.last_position
    else:
        position = dead_char.position
    assert position != None
    if position in pos_map.keys():
        pump_pos = pos_map[position]
        for i in pump_pos:
            if source.get_owner().board[i] != None:
                source.get_owner().board[i].change_eob_atk_mod(1)
                source.get_owner().board[i].change_eob_hlth_mod(1)
                if dead_char.game.verbose_lvl>=4:
                    print(source.get_owner().board[i],'pumped by', source)

Other_Hand_of_Vekna= Treasure(
    name='Other Hand of Vekna',
    lvl=5,
    abils=[
        Triggered_Effect(
            name = 'Other Hand of Vekna Death Effect',
            effect_func = Other_Hand_of_Vekna_triggered_effect,
            trigger = Trigger(
                name='Other Hand of Vekna Death Effect trigger',
                type='die'
            )
        )
    ]
)

# Reduplicator
def Reduplicator_summon_effect(source, summoned):
    if hasattr(source, 'Reduplicator_used_this_turn') == False:
        source.Reduplicator_used_this_turn = False
    if source.Reduplicator_used_this_turn == False:
        source.Reduplicator_used_this_turn = True
        copy = summoned.create_copy(source.owner, 'Reduplicator copy')
        copy.token = True
        copy.summon(source.owner, position = summoned.position)

def Reduplicator_reset_effect(source):
    source.Reduplicator_used_this_turn = False

Reduplicator = Treasure(
    name = "Reduplicator",
    lvl = 4,
    abils = [
        Triggered_Effect(
            name = "Reduplicator reset triggered ability",
            trigger = Trigger(
                name= "Reduplicator reset trigger",
                type= "start of combat"
            ),
            effect_func = Reduplicator_reset_effect
        ),
        Triggered_Effect(
            name = "Reduplicator summon triggered ability",
            trigger = Trigger(
                name= "Reduplicator reset trigger",
                type= "summon"
            ),
            effect_func = Reduplicator_summon_effect
        )
    ]
)

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
            reverse_effect_func = lambda char: char.remove_modifier(Ring_of_Rage_Modifier)
        )
    ]
)

Six_of_Shields_Modifier = Modifier(
    name= 'Six of Shields Modifier',
    hlth_func = lambda char, hlth, source: hlth + 3
)

Six_of_Shields= Treasure(
    name = 'Six of Shields',
    lvl = 4,
    abils= [
        Global_Static_Effect(
            name = 'Six of Shields Effect',
            effect_func = lambda char: char.add_modifier(Six_of_Shields_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Six_of_Shields_Modifier)
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


def Summoning_Portal_reset_effect(source):
    source.Summoning_Portal_counter = 0

def Summoning_Portal_count_effect(source, summoned):
    source.Summoning_Portal_counter += 1

def Summoning_Portal_summon_effect(source, summoned):
    summoned.change_eob_atk_mod(source.Summoning_Portal_counter)
    summoned.change_eob_hlth_mod(source.Summoning_Portal_counter)

Summoning_Portal = Treasure(
    name = 'Summoning Portal',
    lvl=4,
    abils=[
        Triggered_Effect(
            name = "Summoning Portal reset triggered ability",
            trigger = Trigger(
                name= "Summoning Portal reset trigger",
                type= "start of combat"
            ),
            effect_func = Summoning_Portal_reset_effect
        ),
        Triggered_Effect(
            name = "Summoning Portal summon counting ability",
            trigger = Trigger(
                name= "Summoning Portal counting trigger",
                type= "summon"
            ),
            effect_func = Summoning_Portal_count_effect,
            multi_ignore = True
        ),
        Triggered_Effect(
            name = "Summoning Portal summon triggered ability",
            trigger = Trigger(
                name= "Summoning Portal summon trigger",
                type= "summon"
            ),
            effect_func = Summoning_Portal_summon_effect
        )
    ]
)


def Ambrosia_reverse_effect(char):
    char.upgraded = False

def Ambrosia_effect(source):
    char = source.get_owner().board[7]
    if char != None and char.upgraded == False:
        source.upgraded = True
        copy = Effect(
            name="Ambrosia reverse effect",
            reverse_effect_func = Ambrosia_reverse_effect
        )
        char.eob_reverse_effects.append(copy)

Ambrosia= Treasure(
    name='Ambrosia',
    lvl=5,
    abils= [
            Triggered_Effect(
                name = 'Ambrosia triggered effect',
                effect_func = Ambrosia_effect,
                trigger = Trigger(
                    name='Ambrosia Effect trigger',
                    type='start of combat'
                )
            )
        ]
)

def Draculas_Saber_effect(source, dead_char):
    for i in source.get_owner().board.values():
        if i != None:
            i.change_eob_atk_mod(2)
            i.change_eob_hlth_mod(1)

Draculas_Saber= Treasure(
    name="Dracula's Saber",
    lvl=5,
    abils=[
        Triggered_Effect(
            name = 'Dracula Saber triggered effect',
            effect_func = Draculas_Saber_effect,
            trigger = Trigger(
                name='Dracula Saber Effect trigger',
                type='opponent die'
            )
        )
    ]
)

def Exploding_Mittens_triggered_effect(source, dead_char):
    opp_chars = [i for i in source.get_owner().opponent.board.values() if i != None]
    for char in opp_chars:
        char.take_damage(1, source=source)

Exploding_Mittens= Treasure(
    name='Exploding Mittens',
    lvl=5,
    abils=[
        Triggered_Effect(
            name = 'Exploding Mittens Death Effect',
            effect_func = Exploding_Mittens_triggered_effect,
            trigger = Trigger(
                name='Exploding Mittens Death Effect trigger',
                type='die'
            )
        )
    ]
)

def Hand_of_Midas_effect(char, source):
    upgrade_chars = char.get_owner().check_for_upgrades()[0]
    if char.name not in upgrade_chars:
        char.upgraded = True
        source.source.get_owner().discard_treasure(source.source)

Hand_of_Midas= Treasure(
    name='Hand of Midas',
    lvl=5,
    abils=[
        Purchase_Effect(
            name = 'Hand of Midas Effect',
            effect_func = Hand_of_Midas_effect,
            multi_ignore = True
        )
    ]
)

# Harvest_Moon= Treasure(
#     name='Harvest Moon',
#     lvl=5,
#     abils=[]
#     # ability hardcoded into attacks
# )

def Helm_of_the_Ugly_Gosling_effect(source):
    chars = [i for i in source.get_owner().board.values() if i != None]
    if chars != []:
        lowest_atk = min([i.atk() for i in chars])
        lowest_atk_char = [i for i in chars if i.atk()==lowest_atk][0]
        lowest_atk_char.change_eob_atk_mod(15)
        lowest_atk_char.change_eob_hlth_mod(15)

Helm_of_the_Ugly_Gosling= Treasure(
    name='Helm of the Ugly Gosling',
    lvl=5,
    abils=[
        Triggered_Effect(
            name = 'Helm of the Ugly Gosling triggered effect',
            effect_func = Helm_of_the_Ugly_Gosling_effect,
            trigger = Trigger(
                name='Helm of the Ugly Gosling Effect trigger',
                type='start of combat'
            )
        )
    ]
)

# Horn of Olympus
Horn_of_Olympus = Treasure(
    name = 'Horn of Olympus',
    lvl =5,
    abils = []
    # abil hardcoded into support effects
)

Mimic = Treasure(
    name = 'Mimic',
    lvl=5,
    abils = [
        Treasure_Effect_Multiplier(
            name = 'Mimic Treasure Effect Multiplier'
        )
    ]
)

Monkeys_Paw_Modifier = Modifier(
    name = "Monkey's Paw Modifier",
    atk_func = lambda char, atk, source: atk + 6,
    hlth_func = lambda char, hlth, source: hlth + 6,
)

def Monkeys_Paw_begin_combat_check(source):
    if any([i==None for i in source.get_owner().board.values()]):
        source.Monkeys_Paw_toggle = True
    else:
        source.Monkeys_Paw_toggle = False

def Monkeys_Paw_cond(char):
    result = any([i.Monkeys_Paw_toggle for i in char.get_owner().treasures if i.name == "Monkey's Paw"
        and hasattr(i,"Monkeys_Paw_toggle")])
    return result

Monkeys_Paw = Treasure(
    name = "Monkey's Paw",
    lvl = 5,
    abils = [
        Triggered_Effect(
            name = "Monkey's triggered ability",
            trigger = Trigger(
                name= "Monkey's Paw trigger",
                type= "start of combat"
            ),
            effect_func = Monkeys_Paw_begin_combat_check
        ),
        Global_Static_Effect(
            name = "Monkey's Paw",
            effect_func = lambda char: char.add_modifier(Monkeys_Paw_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Monkeys_Paw_Modifier),
            condition = Monkeys_Paw_cond
        )
    ]
)

Staff_of_the_Old_Toad = Treasure(
    name="Staff of the Old Toad",
    lvl=5,
    abils=[]
    # ability hard coded into shop generation
)




Sword_of_Fire_and_Ice_Atk_Modifier = Modifier(
    name= 'Sword of Fire and Ice Attack Modifier',
    atk_func = lambda char, atk, source: atk + 6
)

Sword_of_Fire_and_Ice_Health_Modifier = Modifier(
    name= 'Sword of Fire and Ice Health Modifier',
    hlth_func = lambda char, hlth, source: hlth + 6
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
    lvl = 5,
    abils = [
        Global_Static_Effect(
            name = 'Sword of Fire and Ice Effect',
            effect_func = Sword_of_Fire_and_Ice_effect,
            reverse_effect_func = Sword_of_Fire_and_Ice_reverse_effect
        )
    ]
)

# The 9th Book of Merlin
def Merlin_9th_Book_Last_Breath_Effect(mage):
    Deck_spells = ['Falling Stars','Earthquake', 'Fireball', 'Lightning Bolt', 'Ride of the Valkyries',
    'Blessing of Athena', 'Poison Apple', 'Shrivel', 'Smite','Pigomorph']
    elig_spells = [i for i in mage.get_owner().game.spells if i.name in Deck_spells
    and i.lvl <= mage.get_owner().lvl]
    if elig_spells != []:
        selected = random.choice(elig_spells)
        selected.cast(mage.owner, in_combat = True)

def The_Ninth_Book_of_Merlin_effect(char):
    abil = Last_Breath_Effect(
        name='The 9th Book of Merlin Last Breath Effect',
        effect_func = Merlin_9th_Book_Last_Breath_Effect
    )
    char.abils.append(abil)
    abil.add_to_obj(char)

def The_Ninth_Book_of_Merlin_reverse_effect(char):
    rm_eff = [i for i in char.abils if i.name=='The 9th Book of Merlin Last Breath Effect']
    char.abils.remove(rm_eff[0])

The_Ninth_Book_of_Merlin = Treasure(
    name = 'The 9th Book of Merlin',
    lvl = 5,
    abils = [
        Global_Static_Effect(
            name = 'The 9th Book of Merlin Effect',
            effect_func = The_Ninth_Book_of_Merlin_effect,
            reverse_effect_func = The_Ninth_Book_of_Merlin_reverse_effect,
            condition = lambda char: 'Mage' in char.type
        )
    ]
)

def Tree_of_Life_triggered_effect(source, dead_char):
    for i in source.get_owner().board.values():
        if i != None:
            i.change_eob_hlth_mod(i.dmg_taken)

Tree_of_Life= Treasure(
    name='Tree of Life',
    lvl=5,
    abils=[
        Triggered_Effect(
            name = 'Tree of Life Death Effect',
            effect_func = Tree_of_Life_triggered_effect,
            trigger = Trigger(
                name='Tree of Life Death Effect trigger',
                type='die'
            )
        )
    ]
)


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

def Evil_Eye_effect(eff, player):
    player.support_effects_multiplier += 1

def Evil_Eye_reverse_effect(eff, player):
    player.support_effects_multiplier -= 1

Evil_Eye= Treasure(
    name='Evil Eye',
    lvl=6,
    abils=[
        Player_Effect(
            name = 'Evil Eye Support Effect Multiplier',
            effect_func = Evil_Eye_effect,
            reverse_effect_func = Evil_Eye_reverse_effect
        )
    ]
)

def Ivory_Owl_effect(source):
    for i in source.get_owner().board.values():
        if i != None:
            i.change_atk_mod(2)
            i.change_hlth_mod(2)

Ivory_Owl= Treasure(
    name='Ivory Owl',
    lvl=6,
    abils=[
        Triggered_Effect(
            name = "Ivory Owl triggered ability",
            trigger = Trigger(
                name= "Ivory Owl trigger",
                type= "start of combat"
            ),
            effect_func = Ivory_Owl_effect
        )
    ]
)

def Pandoras_Box_effect(source):
    plyr = source.get_owner()
    treasures = [i for i in source.get_owner().game.treasures if i.lvl == 7 and i not in
        source.get_owner().treasures and i not in source.get_owner().obtained_treasures]
    selected = random.choice(treasures)
    if source.get_owner().game.verbose_lvl>=2:
        print(source.get_owner(), 'gains', selected)
    plyr.gain_treasure(selected)

    if len(source.get_owner().treasures) > 4:
        remove_choice = source.get_owner().input_choose(source.get_owner().treasures, label='treasure remove')
        if source.get_owner().game.verbose_lvl>=2:
            print(source.get_owner(), 'discards', remove_choice)
        source.get_owner().discard_treasure(remove_choice)



Pandoras_Box = Treasure(
    name = "Pandora's Box",
    lvl = 6,
    abils = [
        Triggered_Effect(
            name ='Pandoras Box Counter',
            trigger = Trigger(
                name = 'Pandoras Box Trigger',
                type = 'end of turn'
            ),
            effect_func = Pandoras_Box_effect,
            counter = 1,
            multi_ignore = True
        )
    ]
)


def Phoenix_Feather_resummon_effect(source, dead_char):
    # check if current position has a token with origin from phoenix feather
    # if so, that means it's the second trigger of phoenix feather (from mimic) and
    # we need to find a new position for the second token
    if source.get_owner().board[dead_char.position] != None and \
        source.get_owner().board[dead_char.position].origin == 'Phoenix Feather summon':
        spawn_pos = source.get_owner().find_next_spawn_position(dead_char.position)
    else:
        spawn_pos = dead_char.position

    # only create a copy if there's space
    if spawn_pos != None:
        copy = dead_char.create_copy(source.owner, 'Phoenix Feather summon')
        copy.token = True
        copy.summon(source.owner, spawn_pos)

def Phoenix_Feather_resummon_condition(source, condition_obj):
    chars = [i for i in source.source.source.get_owner().board.values() if i != None and i != condition_obj]
    if chars != []:
        highest_atk = max([i.atk() for i in chars])
    else:
        highest_atk = -1
    return condition_obj.atk()>= highest_atk


Phoenix_Feather= Treasure(
    name='Phoenix Feather',
    lvl=6,
    abils=[
        Triggered_Effect(
            name = "Phoenix Feather resummon ability",
            trigger = Trigger(
                name= "Phoenix Feather resummon trigger",
                type= "die",
                condition = Phoenix_Feather_resummon_condition
            ),
            effect_func = Phoenix_Feather_resummon_effect,
            once_per_turn= True
        ),
    ]
)

def Spear_of_Achilles_effect(source, attacker):
    attacker.change_eob_atk_mod(7)
    attacker.change_eob_hlth_mod(7)

Spear_of_Achilles= Treasure(
    name='Spear of Achilles',
    lvl=6,
    abils=[
        Triggered_Effect(
            name = 'Spear of Achilles attack effect',
            effect_func = Spear_of_Achilles_effect,
            trigger = Trigger(
                name='Spear of Achilles attack effect trigger',
                type='attack'
            )
        )
    ]
)


def The_Ark_effect(source):
    lvls = [i.lvl for i in source.get_owner().board.values() if i !=None]
    if all([i in lvls for i in range(2,7)]):
        for i in source.get_owner().board.values():
            if i != None:
                i.change_eob_atk_mod(12)
                i.change_eob_hlth_mod(12)

The_Ark = Treasure(
    name = 'The Ark',
    lvl=6,
    abils = [
        Triggered_Effect(
            name = "The Ark triggered ability",
            trigger = Trigger(
                name= "The Ark trigger",
                type= "start of combat"
            ),
            effect_func = The_Ark_effect
        )
    ]
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
Wand_of_Weirding = Treasure(
    name= 'Wand of Weirding',
    lvl=6,
    abils = [
        Spell_Multiplier(
            name = 'Wand of Weirding Spell Multiplier'
        )
    ]
)

# Black Prism
Black_Prism = Treasure(
    name= 'Black Prism',
    lvl =7,
    # Black Prism abil is a hardcoded check when casting a spell
    abils = []
)

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

Magic_Sword_100_Modifier = Modifier(
    name= 'Magic Sword +100 Modifier',
    atk_func = lambda char, atk, source: atk + 100,
)

Magic_Sword_100= Treasure(
    name='Magic Sword +100',
    lvl=7,
    abils=[
        Global_Static_Effect(
            name = 'Magic Sword +100 Effect',
            effect_func = lambda char: char.add_modifier(Magic_Sword_100_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Magic_Sword_100_Modifier),
            condition = lambda char: char.position==1
        )
    ]
)

def Mirror_Mirror_assign_respawn(source):
    for n in range(1,5):
        char = source.get_owner().board[n]
        if char != None:
            char.trackers = char.trackers.copy()
            char.trackers['Mirror_Mirror_respawn'] += 1

def Mirror_Mirror_reset_respawn(source):
    for char in source.get_owner().hand:
        char.trackers = char.trackers.copy()
        char.trackers['Mirror_Mirror_respawn'] = 0

def Mirror_Mirror_triggered_effect(source, dead_char):
    spawn_pos = dead_char.position

    # only create a copy if there's space
    if spawn_pos != None:
        copy = dead_char.create_copy(source.owner, 'Mirror Mirror summon', plain_copy = True)
        copy.token = True
        copy.base_atk = 1
        copy.base_hlth = 1
        copy.trackers = copy.trackers.copy()
        copy.trackers['Mirror_Mirror_respawn'] = dead_char.trackers['Mirror_Mirror_respawn'] - 1
        copy.summon(source.owner, spawn_pos)

Mirror_Mirror= Treasure(
    name='Mirror Mirror',
    lvl=7,
    abils=[
        Triggered_Effect(
            name = "Mirror Mirror assign respawn ability",
            trigger = Trigger(
                name= "Mirror Mirror trigger",
                type= "start of combat"
            ),
            effect_func = Mirror_Mirror_assign_respawn
        ),
        Triggered_Effect(
            name = 'Mirror Mirror Death Effect',
            effect_func = Mirror_Mirror_triggered_effect,
            trigger = Trigger(
                name='Mirror Mirror Death Effect trigger',
                type='die',
                condition = lambda source, condition_obj: condition_obj.trackers
                    ['Mirror_Mirror_respawn'] > 0
            ),
            multi_ignore = True
        ),
        Triggered_Effect(
            name = "Mirror Mirror reset respawn ability",
            trigger = Trigger(
                name= "Mirror Mirror trigger",
                type= "end of turn"
            ),
            effect_func = Mirror_Mirror_reset_respawn
        ),
    ]
)

# approximating the limitation of time to roll here
def The_Holy_Grail_effect(source):
    source.get_owner().next_turn_addl_gold += 50
    if source.owner != None:
        source.get_owner().discard_treasure(source)

The_Holy_Grail= Treasure(
    name='The Holy Grail',
    lvl=7,
    abils=[
        Triggered_Effect(
            name = "The Holy Grail triggered ability",
            trigger = Trigger(
                name= "The Holy Grail trigger",
                type= "end of turn"
            ),
            effect_func = The_Holy_Grail_effect,
            multi_ignore = True
        )
    ]
)

def The_Round_Table_effect(source):
    for i in source.get_owner().board.values():
        if i != None:
            if i.atk() > i.hlth():
                i.change_eob_hlth_mod(i.atk() - i.hlth())
            else:
                i.change_eob_atk_mod(i.hlth() - i.atk())

The_Round_Table= Treasure(
    name='The Round Table',
    lvl=7,
    abils=[
        Triggered_Effect(
            name = "The Round Table triggered ability",
            trigger = Trigger(
                name= "The Round Table trigger",
                type= "start of combat"
            ),
            effect_func = The_Round_Table_effect
        )
    ]
)

objs=deepcopy(list(locals().keys()))
master_treasure_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Treasure):
        master_treasure_list.append(obj)

if __name__ == "__main__":
    import pandas as pd
    df = pd.DataFrame([i.__dict__ for i in master_treasure_list])
    df.to_csv('output/treasure_list.csv')
