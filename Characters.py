from c_Character import Character
from copy import deepcopy
from Effects import *
import random
from datetime import datetime


Baby_Dragon = Character(
    name='Baby Dragon',
    atk=3,
    hlth=2,
    alignment='Neutral',
    lvl=2,
    type=['Dragon'],
    keyword_abils = ['flying']
)

def Baby_Root_support_effect(char, source):
    char.change_hlth_mod(3 * (1+ source.upgraded))

def Baby_Root_reverse_effect(char, source):
    char.change_hlth_mod(-3 * (1+ source.upgraded))

Baby_Root = Character(
    name='Baby Root',
    atk=0,
    hlth=3,
    alignment='Good',
    lvl=2,
    type=['Treant'],
    abils=[
        Support_Effect(
            name='Baby Root support effect',
            effect_func = Baby_Root_support_effect,
            reverse_effect_func = Baby_Root_reverse_effect
        )
    ]
)

Cat_1_1 = Character(
    name = 'Cat',
    atk=1,
    hlth=1,
    alignment='Evil',
    lvl=2,
    type=['Animal'],
    token = True
)

def Black_Cat_Last_Breath_Effect(char):
    token = Cat_1_1.create_copy(char.owner, 'Black Cat Death Effect')
    if char.upgraded:
        token.base_atk = 2
        token.base_hlth = 2
    token.add_to_board(plyr = char.owner, position = char.position)

Black_Cat = Character(
    name = 'Black Cat',
    atk=1,
    hlth=1,
    alignment='Evil',
    lvl=2,
    type=['Animal'],
    abils=[
        Last_Breath_Effect(
            name='Black Cat Death Effect',
            effect_func = Black_Cat_Last_Breath_Effect
        )
    ]
)


Baad_Billy_Gruff = Character(
    name='B-a-a-d Billy Gruff',
    atk=2,
    hlth=3,
    alignment='Evil',
    lvl=2,
    type=['Animal']
)

Blind_Mouse = Character(
    name='Blind Mouse',
    atk=2,
    hlth=2,
    alignment='Neutral',
    lvl=2,
    type=['Animal']
)

Cinderella = Character(
    name='Cinder-ella',
    atk=2,
    hlth=2,
    alignment='Neutral',
    lvl=2,
    type=['Princess','Mage'],
    abils = [
        Quest(
            name= 'Cinder-ella Quest',
            trigger = Trigger(
                name='Cinder-ella Quest Trigger',
                type='cast'
            ),
            counter = 4
        )
    ]
)

Crafty_Modifier = Modifier(
    name = 'Crafty Modifier',
    atk_func = lambda char, atk, source: atk + len(char.owner.treasures)*3 * (char.upgraded + 1),
    hlth_func = lambda char, hlth, source: hlth + len(char.owner.treasures)*3 * (char.upgraded + 1)
)

Crafty = Character(
    name='Crafty',
    atk=1,
    hlth=1,
    alignment='Neutral',
    lvl=2,
    type=['Dwarf'],
    abils=[
        Local_Static_Effect(
            name = 'Craft Static Effect',
            effect_func = lambda self: self.add_modifier(Crafty_Modifier),
            reverse_effect_func = lambda self: self.remove_modifier(Crafty_Modifier),
            modifier = Crafty_Modifier
        )
    ]
)

def Fanny_support_effect(char, source):
    char.change_atk_mod(2 * (1+ source.upgraded))
    char.change_hlth_mod(2 * (1+ source.upgraded))

def Fanny_reverse_effect(char, source):
    char.change_atk_mod(-2 * (1+ source.upgraded))
    char.change_hlth_mod(-2 * (1+ source.upgraded))

Fanny = Character(
    name='Fanny',
    atk=2,
    hlth=2,
    alignment='Neutral',
    lvl=2,
    type=['Dwarf'],
    abils=[
        Support_Effect(
            name='Fanny support effect',
            effect_func = Fanny_support_effect,
            reverse_effect_func = Fanny_reverse_effect,
            condition = lambda char: 'Dwarf' in char.type
        )
    ]
)

# ability to sell chicken for 2 is hardcoded in selling
Golden_Chicken = Character(
    name='Golden Chicken',
    atk=2,
    hlth=2,
    alignment='Neutral',
    lvl=2,
    type=['Animal']
)

Happy_Little_Tree= Character(
    name='Happy Little Tree',
    atk=1,
    hlth=1,
    alignment='Good',
    lvl=2,
    type=['Treant'],
    abils=[
        Triggered_Effect(
            name='Happy Little Tree Effect',
            effect_func = lambda source: source.change_hlth_mod( 2 * (1+source.upgraded)),
            trigger = Trigger(
                name='Happy Little Tree Trigger',
                type='end of turn'
            )
        )
    ]
)

def Humpty_Dumpty_Last_Breath_Effect(self):
    if self.token == False:
        self.remove_from_hand()

Humpty_Dumpty = Character(
    name='Humpty Dumpty',
    atk=6,
    hlth=6,
    alignment='Good',
    lvl=2,
    type=['Egg'],
    abils = [
        Last_Breath_Effect(
            name = 'Humpty Dumpty',
            effect_func = Humpty_Dumpty_Last_Breath_Effect
        )
    ]
)

Kitty_Cutpurse = Character(
    name='Kitty Cutpurse',
    atk=1,
    hlth=1,
    alignment='Evil',
    lvl=2,
    type=['Animal'],
    abils=[
        Triggered_Effect(
            name='Kitty Cutpurse Slay effect',
            effect_func = lambda source, slain, slain_attribs: source.owner.gain_gold_next_turn(1 * (1 + source.upgraded)),
            trigger = Trigger(
                name = 'Kitty Cutpurse Slay trigger',
                type = 'slay'
            )
        )
    ]
)

Labyrinth_Minotaur_Modifier = Modifier(
    name= 'Labyrinth Minotaur Modifier',
    atk_func = lambda char, atk, source: atk + 1 * (1 + source.upgraded)
)


Labyrinth_Minotaur = Character(
    name='Labyrinth Minotaur',
    atk=4,
    hlth=1,
    alignment='Evil',
    lvl=2,
    type=['Monster'],
    abils = [
        Global_Static_Effect(
            name = 'Labyrinth Minotaur effect',
            effect_func = lambda char: char.add_modifier(Labyrinth_Minotaur_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Labyrinth_Minotaur_Modifier),
            condition = lambda char: char.get_alignment()=='Evil',
            modifier= Labyrinth_Minotaur_Modifier
        )
    ]
)


Frog_Prince = Character(
    name = 'Frog Prince',
    lvl=2,
    alignment='Good',
    atk=5,
    hlth=5,
    type=['Prince','Animal'],
    inshop=False
)

def Lonely_Prince_Transform_func(char, eff):
    copy = Frog_Prince.create_copy(char.owner, 'Frog Prince Transform Effect')
    eff.source.transform(copy)

Lonely_Prince_Transform = Purchase_Effect(
    name='Lonely Prince Purchase Effect',
    effect_func = Lonely_Prince_Transform_func,
    condition = lambda char: 'Princess' in char.type
)

def Lonely_Prince_effect(eff, player):
    copy = deepcopy(Lonely_Prince_Transform)
    copy.source = eff.source
    player.effects.append(copy)


def Lonely_Prince_reverse_effect(eff, player):
    rm_eff = [i for i in player.effects if i.source==eff.source
        and i.name=='Lonely Prince Purchase Effect']
    assert len(rm_eff)>0
    player.effects.remove(rm_eff[0])

Lonely_Prince = Character(
    name = 'Lonely Prince',
    lvl =2,
    alignment='Good',
    atk=1,
    hlth=1,
    type=['Prince'],
    abils=[
        Player_Effect(
            name='Lonely Prince Effect',
            effect_func= Lonely_Prince_effect,
            reverse_effect_func = Lonely_Prince_reverse_effect
        )
    ]
)


def Mad_Mim_support_effect(char, source):
    char.hlth_mod += 3 * (1+ source.upgraded)

def Mad_Mim_reverse_effect(char, source):
    char.hlth_mod -= 3 * (1+ source.upgraded)

Mad_Mim = Character(
    name='Mad Mim',
    atk=0,
    hlth=3,
    alignment='Evil',
    lvl=2,
    type=['Mage'],
    abils=[
        Support_Effect(
            name='Mad Mim support effect',
            effect_func = Mad_Mim_support_effect,
            reverse_effect_func = Mad_Mim_reverse_effect
        )
    ]
)

# Polywoggle
def Polywoggle_effect(source, slain, slain_attribs):
    elig_pool = [i for i in source.game.char_pool if i.lvl==min(source.owner.lvl+1,6)]
    selected = random.choice(elig_pool)
    if source.token:
        selected.token = True
        source.transform(selected)
    else:
        source.transform(selected)

Polywoggle = Character(
    name='Polywoggle',
    atk=1,
    hlth=1,
    alignment='Neutral',
    lvl=2,
    type=['Animal'],
    abils=[
        Triggered_Effect(
            name='Polywoggle Slay effect',
            effect_func = Polywoggle_effect,
            trigger = Trigger(
                name = 'Polywoggle Slay trigger',
                type = 'slay'
            )
        )
    ]
)

Rainbow_Unicorn_Modifier = Modifier(
    name= 'Rainbow Unicorn Modifier',
    hlth_func = lambda char, hlth, source: hlth + 1 * (1 + source.upgraded)
)


Rainbow_Unicorn = Character(
    name='Rainbow Unicorn',
    atk=1,
    hlth=4,
    alignment='Good',
    lvl=2,
    type=['Animal'],
    abils = [
        Global_Static_Effect(
            name = 'Rainbow Unicorn effect',
            effect_func = lambda char: char.add_modifier(Rainbow_Unicorn_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Rainbow_Unicorn_Modifier),
            condition = lambda char: char.get_alignment()=='Good',
            modifier = Rainbow_Unicorn_Modifier
        )
    ]
)

Tiny = Character(
    name='Tiny',
    atk=6,
    hlth=1,
    alignment='Neutral',
    lvl=2,
    type=['Dwarf']
)

Sherwood_Sureshot = Character(
    name='Sherwood Sureshot',
    atk=2,
    hlth=1,
    alignment='Good',
    lvl=2,
    keyword_abils = ['ranged'],
    type=['Princess']
)

def Wizards_Familiar_effect(source):
    source.change_atk_mod(1 * (1+source.upgraded))
    source.change_hlth_mod(1 * (1+source.upgraded))

Wizards_Familiar = Character(
    name = "Wizard's Familiar",
    atk=1,
    hlth=1,
    alignment='Neutral',
    lvl=2,
    type=['Animal','Mage'],
    abils=[
        Triggered_Effect(
            name='Wizards Familiar Effect',
            effect_func = Wizards_Familiar_effect,
            trigger = Trigger(
                name='Wizards Familiar Trigger',
                type='cast'
            )
        )
    ]
)

# Adventurer = Character(
#     name = "Adventurer",
#     atk=1,
#     hlth=1,
#     alignment='Good',
#     lvl=3,
#     type=['Princess'],
#     abils=[
#         Triggered_Effect(
#             name='Adventurer Slay effect',
#             effect_func = lambda source: source.owner.gain_exp(1 * (1 + source.upgraded)),
#             trigger = Trigger(
#                 name = 'Adventurer Slay trigger',
#                 type = 'slay'
#             )
#         )
#     ]
# )

Brave_Princess = Character(
    name = "Brave Princess",
    atk=4,
    hlth=3,
    alignment='Good',
    lvl=3,
    type=['Princess'],
    abils=[
        Quest(
            name= 'Brave Princess Quest',
            trigger = Trigger(
                name='Brave Princess Quest Trigger',
                type='slay'
            ),
            counter = 3
        )
    ]
)

def Darkwood_Creeper_effect(source, damaged_char):
    damaged_char.change_atk_mod(1 * (1 + source.upgraded))

# Darkwood Creeper
Darkwood_Creeper = Character(
    name='Darkwood Creeper',
    atk=0,
    hlth=3,
    alignment='Evil',
    lvl=3,
    type=['Treant'],
    abils=[
        Triggered_Effect(
            name = 'Darkwood Creeper survive effect',
            effect_func = Darkwood_Creeper_effect,
            trigger = Trigger(
                name = 'Darkwood Creeper survive effect trigger',
                type = 'survive damage'
            )
        )
    ]
)

# Dubly
# Dubly = Character(
#     name = 'Dubly',
#     atk=1,
#     hlth=1,
#     lvl=3,
#     type=['Dwarf']
# )


# Good Witch of the North
def Good_Witch_support_effect(char, source):
    char.change_atk_mod(2 * (1+ source.upgraded))
    char.change_hlth_mod(3 * (1 + source.upgraded))

def Good_Witch_reverse_effect(char, source):
    char.change_atk_mod(2 * (1+ source.upgraded))
    char.change_hlth_mod(-3 * (1+ source.upgraded))

Good_Witch_of_the_North = Character(
    name='Good Witch of the North',
    atk=2,
    hlth=3,
    alignment='Good',
    lvl=3,
    type=['Mage'],
    abils=[
        Support_Effect(
            name='Good Witch support effect',
            effect_func = Good_Witch_support_effect,
            reverse_effect_func = Good_Witch_reverse_effect,
            condition = lambda char: char.get_alignment()=='Good'
        )
    ]
)

# Lucky
def Lucky_triggered_effect(source):
    selected = random.choice([i for i in source.shop if isinstance(i,Character)])
    selected.current_cost = max(0, selected.current_cost - 2)

def Lucky_upgr_triggered_effect(source):
    selected = random.choice([i for i in source.shop if isinstance(i,Character)])
    selected.current_cost = max(0, selected.current_cost - 4)


def Lucky_effect(char):
    if char.upgraded:
        effect = Triggered_Effect(
            name = 'Lucky Triggered Effect',
            effect_func = Lucky_upgr_triggered_effect,
            trigger = Trigger(
                name='Lucky Effect trigger',
                type='start of turn'
            ),
            eob = True
        )
    else:
        effect = Triggered_Effect(
            name = 'Lucky Triggered Effect',
            effect_func = Lucky_triggered_effect,
            trigger = Trigger(
                name='Lucky Effect trigger',
                type='start of turn'
            ),
            eob = True
        )
    effect.apply_effect(char.owner)

Lucky = Character(
    name = 'Lucky',
    atk=3,
    hlth=2,
    lvl=3,
    type=['Dwarf'],
    abils = [
        Last_Breath_Effect(
            name = 'Lucky Death Effect',
            effect_func = Lucky_effect
        )
    ]
)
# Princess Peep
Good_Sheep = Character(
    name = 'Sheep',
    atk=1,
    hlth=1,
    alignment='Good',
    lvl=2,
    type=['Animal'],
    token = True
)

Good_Sheep_upgr = Character(
    name = 'Sheep from upgraded',
    atk=2,
    hlth=2,
    alignment='Good',
    lvl=2,
    type=['Animal'],
    token = True
)

def Princess_Peep_Last_Breath_Effect(char):
    if char.upgraded:
        char.owner.multi_spawn(Good_Sheep_upgr, 3, char.position, char.upgraded)
    else:
        char.owner.multi_spawn(Good_Sheep, 3, char.position, char.upgraded)

Princess_Peep = Character(
    name = 'Princess Peep',
    atk=1,
    hlth=1,
    alignment='Good',
    lvl=3,
    type=['Animal'],
    abils=[
        Last_Breath_Effect(
            name='Princess Peep Death Effect',
            effect_func = Princess_Peep_Last_Breath_Effect
        )
    ]
)

def Princess_Wight_triggered_effect(source, dead_char):
    source.change_atk_mod(1 * (1 + source.upgraded))
    source.change_hlth_mod(1 * (1 + source.upgraded))

# Princess Wight
Princess_Wight = Character(
    name = 'Princess Wight',
    atk=1,
    hlth=3,
    alignment='Evil',
    lvl=3,
    type=['Princess'],
    abils = [
        Triggered_Effect(
            name = 'Princess Wight Dwarf Death Effect',
            effect_func = Princess_Wight_triggered_effect,
            trigger = Trigger(
                name='Princess Wight Dwarf Death Effect trigger',
                type='die',
                condition = lambda self, char: 'Dwarf' in char.type
            )
        ),
        Quest(
            name= 'Princess Wight Quest',
            trigger = Trigger(
                name='Princess Wight Quest Trigger',
                type='purchase',
                condition = lambda self, char: 'Dwarf' in char.type
            ),
            counter = 7
        )
    ]
)

# Prized Pig
def Prized_Pig_Last_Breath_Effect(char):
    char.owner.opponent.next_turn_addl_gold += 1 * (1 + char.upgraded)

def Prized_Pig_end_of_combat_effect(source):
    source.owner.next_turn_addl_gold += 2 * (1+ source.upgraded)

def Prized_Pig_end_of_combat_condition(self, source):
    return source.source.position != None and source.source in source.source.owner.board.values()

Prized_Pig = Character(
    name = 'Prized Pig',
    atk=3,
    hlth=6,
    lvl=3,
    type=['Animal'],
    abils = [
        Last_Breath_Effect(
            name = 'Prized Pig Last Breath Effect',
            effect_func = Prized_Pig_Last_Breath_Effect
        ),
        Triggered_Effect(
            name = 'Prized Pig End of Combat effect',
            effect_func = Prized_Pig_end_of_combat_effect,
            trigger = Trigger(
                name = 'Prized Pig End of Combat trigger',
                type = 'end of combat',
                condition = Prized_Pig_end_of_combat_condition
            )
        )
    ]
)

def Queen_of_Hearts_triggered_effect(source, dead_char):
    source.change_eob_atk_mod(2 * (1 + source.upgraded))
    source.change_eob_hlth_mod(2 * (1 + source.upgraded))

# Queen of Hearts
Queen_of_Hearts = Character(
    name = 'Queen of Hearts',
    atk=1,
    hlth=3,
    alignment='Evil',
    lvl=3,
    type=['Queen'],
    abils = [
        Triggered_Effect(
            name = 'Queen of Hearts Death Effect',
            effect_func = Queen_of_Hearts_triggered_effect,
            trigger = Trigger(
                name='Queen of Hearts Death Effect trigger',
                type='die',
                condition = lambda self, char: char.get_alignment() == 'Evil'
            )
        )
    ]
)

# Romeo
def Romeo_effect(char):
    Juliets = [i for i in char.owner.chars_dead if i.name == 'Juliet']
    upgr_Juliets = [i for i in Juliets if i.upgraded]
    if upgr_Juliets != []:
        selected = upgr_Juliets[0]
    elif Juliets != []:
        selected = Juliets[0]
    else:
        return

    copy = selected.create_copy(char.owner, 'Romeo summon')
    # making the copy a token so it won't end up on the chars_dead list
    copy.token = True
    copy.atk_mod += 7 * (1+ char.upgraded)
    copy.hlth_mod += 7 * (1+ char.upgraded)
    copy.add_to_board(char.owner, char.position)

Romeo = Character(
    name = 'Romeo',
    lvl=3,
    alignment='Good',
    atk=5,
    hlth=3,
    type=['Prince'],
    abils = [
        Last_Breath_Effect(
            name = 'Romeo Death Effect',
            effect_func = Romeo_effect
        )
    ]
)

# Shadow Assassin
def Shadow_Assassin_triggered_effect(source, slain, slayer):
    source.change_atk_mod(1 * (1 + source.upgraded))

Shadow_Assassin = Character(
    name = 'Shadow Assassin',
    lvl=3,
    alignment='Evil',
    atk=2,
    hlth=1,
    keyword_abils=['ranged'],
    type=['Monster'],
    abils = [
        Triggered_Effect(
            name = 'Shadow Assassin Global Slay Effect',
            effect_func = Shadow_Assassin_triggered_effect,
            trigger = Trigger(
                name='Shadow Assassin Global Slay Effect trigger',
                type='global slay',
                condition = lambda self, condition_obj, triggered_obj:
                    any([i.trigger.type == 'slay' for i in condition_obj.abils
                    if isinstance(i, Triggered_Effect)])
            )
        )
    ]
)

# Sleeping Princess
Awakened_Princess = Character(
    name = 'Awakened Princess',
    lvl=3,
    alignment='Good',
    atk=8,
    hlth=8,
    type=['Princess'],
    inshop=False
)

def Sleeping_Princess_Transform_func(char):
    copy = Awakened_Princess.create_copy(char.owner, 'Sleeping Princess Transform Effect')
    char.transform(copy)

def Sleeping_Princess_Transform_condition (self, char):
    return self.source.source == char

Sleeping_Princess_Transform = Triggered_Effect(
    name='Sleeping Princess Target Effect',
    effect_func = Sleeping_Princess_Transform_func,
    trigger = Trigger(
        name = 'Sleeping Princess Target trigger',
        type = 'target',
        condition = Sleeping_Princess_Transform_condition
    )
)

def Sleeping_Princess_effect(eff, player):
    copy = deepcopy(Sleeping_Princess_Transform)
    copy.source = eff.source
    player.effects.append(copy)
    player.triggers.append(copy.trigger)


def Sleeping_Princess_reverse_effect(eff, player):
    rm_eff = [i for i in player.effects if i.source==eff.source
        and i.name=='Sleeping Princess Target Effect']
    assert len(rm_eff)>0
    player.effects.remove(rm_eff[0])
    player.triggers.remove(rm_eff[0].trigger)

Sleeping_Princess = Character(
    name = 'Sleeping Princess',
    lvl =3,
    alignment='Good',
    atk=0,
    hlth=8,
    type=['Princess'],
    abils=[
        Player_Effect(
            name='Sleeping Princess Effect',
            effect_func= Sleeping_Princess_effect,
            reverse_effect_func = Sleeping_Princess_reverse_effect
        )
    ]
)

# Spell Weaver
Spell_Weaver = Character(
    name = "Spell Weaver",
    atk=1,
    hlth=3,
    alignment='Evil',
    lvl=3,
    type=['Mage'],
    abils=[
        Triggered_Effect(
            name='Spell Weaver Effect',
            effect_func = lambda source: source.change_atk_mod(1 * (1+source.upgraded)),
            trigger = Trigger(
                name='Spell Weaver Trigger',
                type='cast'
            )
        )
    ]
)

# The White Stag
def The_White_Stag_effect(source):
    if source.position == 1:
        effect_pos = [5]
    elif source.position == 2:
        effect_pos = [5,6]
    elif source.position == 3:
        effect_pos = [6,7]
    elif source.position == 4:
        effect_pos = [7]
    else:
        return

    for n in effect_pos:
        if source.owner.board[n] != None:
            source.owner.board[n].change_eob_atk_mod(3 * (1 + source.upgraded))
            source.owner.board[n].change_eob_hlth_mod(3 * (1 + source.upgraded))

The_White_Stag = Character(
    name= 'The White Stag',
    atk=3,
    hlth=3,
    alignment = 'Good',
    lvl=3,
    type=['Animal'],
    abils = [
        Triggered_Effect(
            name = 'White Stag attack effect',
            effect_func = The_White_Stag_effect,
            trigger = Trigger(
                name='White Stag attack effect trigger',
                type='attack',
                condition = lambda self, char: self.source.source == char
            )
        )
    ]
)

def Trojan_Donkey_effect(source, damaged_char):
    empty_pos = [source.owner.board[i] == None for i in source.owner.board.keys()]
    if any(empty_pos):
        if source.upgraded:
            elig_pool = [i for i in source.game.char_pool if i.lvl==source.owner.lvl]
        else:
            elig_pool = [i for i in source.game.char_pool if i.lvl<=source.owner.lvl]

        selected = random.choice(elig_pool)
        spawn_pos = source.owner.find_next_spawn_position(source.position)
        assert spawn_pos != None
        copy = selected.create_copy(source.owner, 'Trojan Donkey summon')
        copy.token = True
        copy.add_to_board(source.owner, spawn_pos)
        if source.owner.game.verbose_lvl>=3:
            print(source, 'summons', copy)


# Trojan Donkey
Trojan_Donkey = Character(
    name = 'Trojan Donkey',
    atk=1,
    hlth=5,
    alignment='Good',
    lvl=3,
    type=['Animal'],
    abils = [
        Triggered_Effect(
            name = 'Trojan Donkey survive effect',
            effect_func = Trojan_Donkey_effect,
            trigger = Trigger(
                name = 'Trojan Donkey survive effect trigger',
                type = 'survive damage',
                condition = lambda self, char: self.source.source == char
            )
        )
    ]
)
# Tweedle Dee
Tweedle_Dum = Character(
    name = 'Tweedle Dum',
    atk=1,
    hlth=4,
    alignment='Neutral',
    lvl=2,
    type=['Dwarf'],
    token = True
)

def Tweedle_Dee_Last_Breath_Effect(char):
    token = Tweedle_Dum.create_copy(char.owner, 'Tweedle Dee Death Effect')
    if char.upgraded:
        token.base_atk = 2
        token.base_hlth = 8
    token.add_to_board(char.owner, char.position)

Tweedle_Dee = Character(
    name = 'Tweedle Dee',
    atk=4,
    hlth=1,
    alignment='Neutral',
    lvl=3,
    type=['Dwarf'],
    abils=[
        Last_Breath_Effect(
            name='Tweedle Dee Death Effect',
            effect_func = Tweedle_Dee_Last_Breath_Effect
        )
    ]
)

def Vainpire_effect(source, slain, slain_attribs):
    source.change_atk_mod(1 * (1+source.upgraded))
    source.change_hlth_mod(1 * (1+source.upgraded))

# Vain-Pire
Vainpire = Character(
    name='Vain-pire',
    atk=4,
    hlth=4,
    alignment='Evil',
    lvl=3,
    type=['Monster'],
    abils=[
        Triggered_Effect(
            name='Vain-pire Slay effect',
            effect_func = Vainpire_effect,
            trigger = Trigger(
                name = 'Vain-pire Slay trigger',
                type = 'slay'
            )
        )
    ]
)


def Wicked_Witch_support_effect(char, source):
    char.change_atk_mod(3 * (1+ source.upgraded))
    char.change_hlth_mod(2 * (1 + source.upgraded))

def Wicked_Witch_reverse_effect(char, source):
    char.change_atk_mod(-3 * (1+ source.upgraded))
    char.change_hlth_mod(-2 * (1+ source.upgraded))

Wicked_Witch_of_the_West = Character(
    name='Wicked Witch of the West',
    atk=3,
    hlth=2,
    alignment='Evil',
    lvl=3,
    type=['Mage'],
    abils=[
        Support_Effect(
            name='Wicked Witch support effect',
            effect_func = Wicked_Witch_support_effect,
            reverse_effect_func = Wicked_Witch_reverse_effect,
            condition = lambda char: char.get_alignment()=='Evil'
        )
    ]
)

# Bearded Vulture
#Bearded_Vulture =

# Bossy
Bossy_Modifier = Modifier(
    name= 'Bossy Modifier',
    atk_func = lambda char, atk, source: atk + 2 * (1 + source.upgraded),
    hlth_func = lambda char, hlth, source: hlth + 2 * (1 + source.upgraded)
)


Bossy = Character(
    name='Bossy',
    atk=2,
    hlth=2,
    lvl=4,
    type=['Dwarf'],
    abils = [
        Global_Static_Effect(
            name = 'Bossy effect',
            effect_func = lambda char: char.add_modifier(Bossy_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Bossy_Modifier),
            condition = lambda char: 'Dwarf' in char.type,
            modifier = Bossy_Modifier
        )
    ]
)

# Broc Lee
def Broc_Lee_effect(source, damaged_char):
    source.change_eob_atk_mod(10 * (1 + source.upgraded))

Broc_Lee = Character(
    name = 'Broc Lee',
    atk = 0,
    hlth = 15,
    lvl = 4,
    type = ['Treant'],
    abils = [
        Triggered_Effect(
            name = 'Broc Lee survive effect',
            effect_func = Broc_Lee_effect,
            trigger = Trigger(
                name = 'Broc Lee survive effect trigger',
                type = 'survive damage',
                condition = lambda self, char: self.source.source == char
            )
        )
    ]
)

# Copycat
# Court Wizard
# Fairy Godmother
# Friendly Spirit
# Greedy
def Greedy_effect(source, damaged_char):
    source.owner.next_turn_addl_gold += 1 * (1 + source.upgraded)

Greedy = Character(
    name = 'Greedy',
    atk = 4,
    hlth = 8,
    lvl = 4,
    type = ['Dwarf'],
    abils = [
        Triggered_Effect(
            name = 'Greedy survive effect',
            effect_func = Greedy_effect,
            trigger = Trigger(
                name = 'Greedy survive effect trigger',
                type = 'survive damage',
                condition = lambda self, char: self.source.source == char
            )
        )
    ]
)

# Grim Soul
# Heartwood Elder
# Hungry Hungry Hippocampus
# Juliet
Juliet = Character(
    name='Juliet',
    atk=7,
    hlth=7,
    alignment='Good',
    lvl=4,
    type=['Princess']
)

# Lady of the Lake
def Lady_of_the_Lake_support_effect(char, source):
    char.hlth_mod += 5 * (1+ source.upgraded)

def Lady_of_the_Lake_reverse_effect(char, source):
    char.hlth_mod -= 5 * (1+ source.upgraded)

Lady_of_the_Lake = Character(
    name='Lady of the Lake',
    atk=1,
    hlth=3,
    alignment='Good',
    lvl=4,
    type=['Mage'],
    abils=[
        Support_Effect(
            name='Lady of the Lake support effect',
            effect_func = Lady_of_the_Lake_support_effect,
            reverse_effect_func = Lady_of_the_Lake_reverse_effect
        )
    ]
)


# Lightning Dragon

# Medusa
Statue = Character(
    name = 'Statue',
    atk=0,
    hlth=6,
    lvl=1,
    type=['Statue'],
    token = True
)

def Medusa_effect(source):
    orig = source.atk_target
    if source.atk_target.name != "Statue":
        token = Statue.create_copy(source.owner.opponent, 'Medusa attack effect')
        source.atk_target.transform(token, preserve_mods = False, temporary = True)
        source.atk_target = token


Medusa = Character(
    name = 'Medusa',
    atk = 3,
    hlth = 3,
    alignment = 'Evil',
    lvl = 4,
    type = ['Monster'],
    abils = [
        Triggered_Effect(
            name = 'Medusa attack effect',
            effect_func = Medusa_effect,
            trigger = Trigger(
                name='Medusa attack effect trigger',
                type='attack',
                condition = lambda self, char: self.source.source == char
            )
        )
    ]
)

# Prince Arthur
# def Prince_Arthur_effect(source):
#     for char in source.owner.board.values():
#         if char != None and ('Prince' in char.type or 'Princess' in char.type) and char.upgraded:
#             char.change_atk_mod(2 * (1 + source.upgraded))
#             char.change_hlth_mod(2 * (1 + source.upgraded))
#
#     import pdb; pdb.set_trace()
#
# Prince_Arthur = Character(
#     name = 'Prince Arthur',
#     atk = 5,
#     hlth = 5,
#     alignment = 'Good',
#     lvl = 4,
#     type=['Prince'],
#     abils = [
#         Triggered_Effect(
#             name = 'Prince Arthur triggered effect',
#             effect_func = Prince_Arthur_effect,
#             trigger = Trigger(
#                 name='Earthquake Effect trigger',
#                 type='start of combat',
#                 battle_trigger = True
#             ),
#         )
#     ]
# )

# Princess Pea
# Puff Puff
def Puff_Puff_effect(char):
    for i in char.owner.hand:
        if i.name == 'Puff Puff':
            i.change_atk_mod(1 * (1+char.upgraded))
            i.change_hlth_mod(1 * (1+char.upgraded))

Puff_Puff = Character(
    name = 'Puff Puff',
    atk=6,
    hlth =6,
    lvl=4,
    alignment='Good',
    type=['Puff Puff'],
    abils=[
        Last_Breath_Effect(
            name = 'Puff Puff Death Effect',
            effect_func = Puff_Puff_effect
        )
    ]
)

# Riverwish Mermaid

# Sheep in Wolf's clothing
Bad_Sheep = Character(
    name = 'Sheep',
    atk=5,
    hlth=5,
    alignment='Evil',
    lvl=2,
    type=['Animal'],
    token = True
)

def Sheep_in_Wolfs_Clothing_Last_Breath_Effect(char):
    token = Bad_Sheep.create_copy(char.owner, 'Sheep in Wolfs Clothing death effect')
    token.base_atk = token.base_atk * (1+ char.upgraded)
    token.base_hlth = token.base_hlth * (1+ char.upgraded)
    token.add_to_board(char.owner, char.position)

Sheep_in_Wolfs_Clothing = Character(
    name = "Sheep in Wolf's Clothing",
    atk=1,
    hlth=1,
    alignment='Evil',
    lvl=4,
    type=['Animal'],
    abils=[
        Last_Breath_Effect(
            name="Sheep in Wolf's Clothing Death Effect",
            effect_func = Sheep_in_Wolfs_Clothing_Last_Breath_Effect
        )
    ]
)

# Sporko
def Sporko_support_effect(char, source):
    char.change_atk_mod(5 * (1+ source.upgraded))

def Sporko_reverse_effect(char, source):
    char.change_atk_mod(-5 * (1+ source.upgraded))

Sporko = Character(
    name='Sporko',
    atk=1,
    hlth=3,
    alignment='Evil',
    lvl=4,
    type=['Mage'],
    abils=[
        Support_Effect(
            name='Sporko support effect',
            effect_func = Sporko_support_effect,
            reverse_effect_func = Sporko_reverse_effect
        )
    ]
)

# The Chupacabra
def Chupacabra_effect(source, slain, slain_attribs):
    source.change_atk_mod(1 * (1+source.upgraded))
    source.change_hlth_mod(1 * (1+source.upgraded))
    back_targets = {1:[5], 2:(5,6), 3:(6,7), 4:[7]}
    if source.position in back_targets.keys():
        for i in back_targets[source.position]:
            if source.owner.board[i] != None:
                source.owner.board[i].change_atk_mod(1 * (1+source.upgraded))
                source.owner.board[i].change_hlth_mod(1 * (1+source.upgraded))

Chupacabra = Character(
    name='The Chupacabra',
    atk=7,
    hlth=5,
    alignment='Evil',
    lvl=4,
    type=['Monster'],
    abils=[
        Triggered_Effect(
            name='The Chupacabra Slay effect',
            effect_func = Chupacabra_effect,
            trigger = Trigger(
                name = 'The Chupacabra Slay trigger',
                type = 'slay'
            )
        )
    ]
)

# The Nutcracker
The_Nutcracker = Character(
    name='Cinder-ella',
    atk=4,
    hlth=10,
    alignment='Good',
    lvl=4,
    type=['Prince','Treant'],
    abils = [
        Quest(
            name= 'The Nutcracker Quest',
            trigger = Trigger(
                name = 'The Nutcracker survive effect trigger',
                type = 'survive damage',
                condition = lambda self, char: self.source.source == char
            ),
            counter = 4
        )
    ]
)

# Angry
def Angry_effect(source, damaged_char):
    for i in source.owner.board.values():
        if i != None and 'Dwarf' in i.type:
            i.change_eob_atk_mod(2 * (1+source.upgraded))
            i.change_eob_hlth_mod(2 * (1+source.upgraded))

Angry = Character(
    name = 'Angry',
    atk = 4,
    hlth = 10,
    lvl = 5,
    type = ['Dwarf'],
    abils = [
        Triggered_Effect(
            name = 'Angry survive effect',
            effect_func = Angry_effect,
            trigger = Trigger(
                name = 'Angry survive effect trigger',
                type = 'survive damage',
                condition = lambda self, char: self.source.source == char
            )
        )
    ]
)

# Aon
# Baba Yaga

# Baby Bear
Papa_Bear = Character(
    name = 'Papa Bear',
    atk=4,
    hlth=4,
    alignment='Good',
    lvl=1,
    type=['Animal'],
    token = True
)

Papa_Bear_upgr = Character(
    name = 'Papa Bear from upgraded',
    atk=8,
    hlth=8,
    alignment='Good',
    lvl=1,
    type=['Animal'],
    token = True
)

def Mama_Bear_Last_Breath_Effect(char):
    token = Papa_Bear.create_copy(char.owner, 'Mama Bear Death Effect')
    token.add_to_board(plyr = char.owner, position = char.position)


Mama_Bear = Character(
    name = 'Mama Bear',
    atk=2,
    hlth=2,
    alignment='Good',
    lvl=1,
    type=['Animal'],
    token = True,
    abils=[
        Last_Breath_Effect(
            name='Mama Bear Death Effect',
            effect_func = Mama_Bear_Last_Breath_Effect
        )
    ]
)

def Mama_Bear_upgr_Last_Breath_Effect(char):
    token = Papa_Bear_upgr.create_copy(char.owner, 'Mama Bear Death Effect')
    token.add_to_board(plyr = char.owner, position = char.position)

Mama_Bear_upgr = Character(
    name = 'Mama Bear from upgraded',
    atk=4,
    hlth=4,
    alignment='Good',
    lvl=1,
    type=['Animal'],
    token = True,
    abils=[
        Last_Breath_Effect(
            name='Mama Bear from upgraded Death Effect',
            effect_func = Mama_Bear_upgr_Last_Breath_Effect
        )
    ]
)


def Baby_Bear_Last_Breath_Effect(char):
    if char.upgraded:
        token = Mama_Bear_upgr.create_copy(char.owner, 'Baby Bear Death Effect')
    else:
        token = Mama_Bear.create_copy(char.owner, 'Baby Bear Death Effect')
    token.add_to_board(plyr = char.owner, position = char.position)

Baby_Bear = Character(
    name = 'Baby Bear',
    atk=1,
    hlth=1,
    alignment='Good',
    lvl=5,
    type=['Animal'],
    abils=[
        Last_Breath_Effect(
            name='Baby Bear Death Effect',
            effect_func = Baby_Bear_Last_Breath_Effect
        )
    ]
)

# Cupid
# Lancelot - placeholder for a lvl 5 char
Lancelot = Character(
    name='Lancelot',
    atk=7,
    hlth=7,
    alignment='Good',
    lvl=5,
    type=['Prince','Mage'],
    # abils = [
    #     Quest(
    #         name= 'Cinder-ella Quest',
    #         trigger = Trigger(
    #             name='Cinder-ella Quest Trigger',
    #             type='cast'
    #         ),
    #         counter = 1
    #     )
    # ]
)
# Monster Book
def Monster_Book_Last_Breath_Effect(char):
    Deck_spells = ['Falling Stars','Earthquake', 'Fireball', 'Lightning Bolt', 'Ride of the Valkyries',
        'Blessing of Athena', 'Poison Apple', 'Shrivel', 'Smite','Pigomorph']
    elig_spells = [i for i in char.owner.game.spells if i.name in Deck_spells
        and i.lvl <= char.owner.lvl]
    if elig_spells != []:
        for _ in range(1 * (1 + char.upgraded)):
            selected = random.choice(elig_spells)
            selected.cast(char.owner, in_combat = True)

Monster_Book = Character(
    name='Monster Book',
    atk=10,
    hlth=4,
    alignment='Evil',
    lvl=5,
    type=['Monster'],
    abils =[
        Last_Breath_Effect(
            name='Monster Book Death Effect',
            effect_func = Monster_Book_Last_Breath_Effect
        )
    ]
)
# Nian, Sea Terror
Nian_Sea_Terror = Character(
    name='Nian, Sea Terror',
    atk=10,
    hlth=10,
    alignment='Evil',
    lvl=5,
    type=['Monster'],
    # abils = [
    #     Quest(
    #         name= 'Cinder-ella Quest',
    #         trigger = Trigger(
    #             name='Cinder-ella Quest Trigger',
    #             type='cast'
    #         ),
    #         counter = 1
    #     )
    # ]
)
# Rotten Appletree
# Soltak Ancient

# Southern Siren
def Southern_Siren_effect(source, slain, slain_attribs):
    for _ in range(1 * (1+source.upgraded)):
        if source.position==None:
            start_pos = source.last_position
        else:
            start_pos = source.position
        pos = source.owner.find_next_spawn_position(start_pos)
        if pos != None:
            copy = slain.create_copy(source.owner, 'Southern Siren summon', plain_copy=False)
            copy.token = True

            # reattach the original slain char's attributes to the char
            for i in slain_attribs.keys():
                copy.__dict__[i] = slain_attribs[i]

            copy.add_to_board(plyr = source.owner, position = pos)

Southern_Siren = Character(
    name='Southern Siren',
    atk=10,
    hlth=10,
    alignment='Evil',
    lvl=5,
    type=['Monster'],
    abils=[
        Triggered_Effect(
            name='Southern Siren Slay effect',
            effect_func = Southern_Siren_effect,
            trigger = Trigger(
                name = 'Southern Siren Slay trigger',
                type = 'slay'
            )
        )
    ]
)

# Wombats in Disguise
def Wombats_in_Disguise_Last_Breath_Effect(char):
    elig_pool = [i for i in char.game.char_pool]
    selected = random.choice(elig_pool)
    copy = selected.create_copy(char.owner, 'Wombats in Disguise summon')
    copy.token = True
    copy.change_atk_mod(char.atk() * (1 + char.upgraded))
    copy.change_hlth_mod(char.hlth() * (1 + char.upgraded))
    copy.add_to_board(plyr = char.owner, position = char.position)

Wombats_in_Disguise = Character(
    name = 'Wombats in Disguise',
    atk=4,
    hlth=4,
    alignment='Neutral',
    lvl=5,
    type=['Animal'],
    abils=[
        Last_Breath_Effect(
            name='Wombats in Disguise Death Effect',
            effect_func = Wombats_in_Disguise_Last_Breath_Effect
        )
    ]
)

# Wretched Mummy
def Wretched_Mummy_Last_Breath_Effect(char):
    for i in char.owner.opponent.board.values():
        if i != None:
            i.take_damage(4, source=char)

Wretched_Mummy = Character(
    name = 'Wretched Mummy',
    atk=4,
    hlth=1,
    alignment='Evil',
    lvl=5,
    type=['Monster'],
    abils=[
        Last_Breath_Effect(
            name='Wretched Mummy Death Effect',
            effect_func = Wretched_Mummy_Last_Breath_Effect
        )
    ]
)

# Ashwood Elm
# Bearstein
# Doombreath

# Echowood
# Good Boy
def Good_Boy_Last_Breath_Effect(char):
    for i in char.owner.board.values():
        if i != None and i.get_alignment() == 'Good':
            i.change_eob_atk_mod(char.atk() * (1 + char.upgraded))
            i.change_eob_hlth_mod(char.hlth() * (1 + char.upgraded))

Good_Boy = Character(
    name = 'Good Boy',
    atk=2,
    hlth=2,
    alignment='Good',
    lvl=6,
    type=['Animal'],
    abils=[
        Last_Breath_Effect(
            name='Good Boy Death Effect',
            effect_func = Good_Boy_Last_Breath_Effect
        )
    ]
)

# Great Pumpkin King
def Great_Pumpkin_King_Last_Breath_Effect(char):
    # figure out order chars will spawn based on pumpkin position
    start_pos = char.position
    if start_pos == 1:
        order = [2,3,4,5,6,7,1]
    if start_pos == 2:
        order = [3,1,4,5,6,7,2]
    if start_pos == 3:
        order = [4,2,1,6,7,5,3]
    if start_pos == 4:
        order = [3,2,1,7,6,5,4]
    if start_pos == 5:
        order = [6,7,1,2,3,4,5]
    if start_pos == 6:
        order = [5,7,2,3,4,1,6]
    if start_pos == 7:
        order = [5,6,4,3,2,1,7]

    # note dead evil chars and their levels
    evil_dead_chars = [i for i in char.owner.chars_dead if i.get_alignment()=='Evil']
    lvls = [i.lvl-1 for i in evil_dead_chars if i.lvl>=3]
    lvls.sort()

    # note spaces that are empty
    empty_spaces = [i for i in char.owner.board.keys() if char.owner.board[i] == None]
    empty_spaces.append(char.position)
    summon_order = []
    for i in order:
        if i in empty_spaces:
            summon_order.append(i)

    # pick a random character to summon for every dead char
    for pos in summon_order:
        if lvls != []:
            get_lvl = lvls.pop(-1)
            elig_pool = [i for i in char.game.char_pool if i.get_alignment()=='Evil' and
                i.lvl == get_lvl]
            selected = random.choice(elig_pool)
            copy = selected.create_copy(char.owner, 'Great Pumpkin King summon')
            copy.token = True
            if char.upgraded:
                copy.upgraded = True
            copy.add_to_board(char.owner, pos)
            if char.owner.game.verbose_lvl>=3:
                print(char.owner, 'summons', copy)

Great_Pumpkin_King = Character(
    name = 'Great Pumpkin King',
    atk=5,
    hlth=5,
    alignment='Evil',
    lvl=6,
    type=['Monster'],
    abils=[
        Last_Breath_Effect(
            name='Great Pumpkin King Death Effect',
            effect_func = Great_Pumpkin_King_Last_Breath_Effect
        )
    ]
)

# Grumblegore
def Grumblegore_support_effect(char, source):
    char.change_atk_mod(10 * (1+ source.upgraded))

def Grumblegore_reverse_effect(char, source):
    char.change_atk_mod(-10 * (1+ source.upgraded))

Grumblegore = Character(
    name='Grumblegore',
    atk=10,
    hlth=5,
    alignment='Evil',
    lvl=6,
    type=['Monster'],
    keyword_abils=['ranged'],
    abils=[
        Support_Effect(
            name='Grumblegore support effect',
            effect_func = Grumblegore_support_effect,
            reverse_effect_func = Grumblegore_reverse_effect
        )
    ]
)

# Hercules
# Jormungand
def Jormungand_effect(source, slain, slain_attribs):
    source.change_eob_atk_mod(20 * (1+source.upgraded))
    source.change_eob_hlth_mod(20 * (1+source.upgraded))

Jormungand = Character(
    name='Jormungand',
    atk=20,
    hlth=20,
    lvl=6,
    type=['Monster'],
    abils=[
        Triggered_Effect(
            name='Jormungand Slay effect',
            effect_func = Jormungand_effect,
            trigger = Trigger(
                name = 'Jormungand Slay trigger',
                type = 'slay'
            )
        )
    ]
)

# Lordy
# Robin Wood
# Shoulder Faeries
# The Green Knight
def Green_Knight_support_effect(char, source):
    char.change_hlth_mod(10 * (1+ source.upgraded))

def Green_Knight_reverse_effect(char, source):
    char.change_hlth_mod(-10 * (1+ source.upgraded))

Green_Knight = Character(
    name='The Green Knight',
    atk=10,
    hlth=30,
    alignment='Good',
    lvl=6,
    type=['Treant'],
    abils=[
        Support_Effect(
            name='The Green Knight support effect',
            effect_func = Green_Knight_support_effect,
            reverse_effect_func = Green_Knight_reverse_effect
        )
    ]
)

def The_Oni_King_effect(source):
    source.change_eob_atk_mod(10 * (1+source.upgraded))
    source.change_eob_hlth_mod(10 * (1+source.upgraded))

# The Oni King
The_Oni_King = Character(
    name = 'The Oni King',
    atk = 13,
    hlth = 13,
    alignment = 'Evil',
    lvl = 6,
    type = ['Monster'],
    abils = [
        Triggered_Effect(
            name = 'The Oni King attack effect',
            effect_func = The_Oni_King_effect,
            trigger = Trigger(
                name='The Oni King attack effect trigger',
                type='attack',
                condition = lambda self, char: 'Monster' in char.type
            )
        )
    ]
)

# The Storm King
The_Storm_King_Modifier = Modifier(
    name = 'The Storm King Modifier',
    atk_func = lambda char, atk, source: atk + char.owner.spells_cast_this_game*2 * (char.upgraded + 1),
    hlth_func = lambda char, hlth, source: hlth + char.owner.spells_cast_this_game*2 * (char.upgraded + 1)
)

The_Storm_King = Character(
    name='The Storm King',
    atk=2,
    hlth=2,
    alignment='Neutral',
    lvl=6,
    type=['Mage'],
    abils=[
        Local_Static_Effect(
            name = 'The Storm King Static Effect',
            effect_func = lambda self: self.add_modifier(The_Storm_King_Modifier),
            reverse_effect_func = lambda self: self.remove_modifier(The_Storm_King_Modifier),
            modifier = The_Storm_King_Modifier
        )
    ]
)


# Three Big Pigs
Evil_Pig = Character(
    name = 'Evil Pig',
    atk=5,
    hlth=5,
    alignment='Evil',
    lvl=1,
    type=['Animal'],
    token = True
)

Evil_Pig_upgr = Character(
    name = 'Evil Pig from upgraded',
    atk=10,
    hlth=10,
    lvl=1,
    alignment='Evil',
    type=['Animal'],
    token = True
)

def Three_Big_Pigs_Last_Breath_Effect(char):
    if char.upgraded:
        char.owner.multi_spawn(Evil_Pig_upgr, 3, char.position, char.upgraded)
    else:
        char.owner.multi_spawn(Evil_Pig, 3, char.position, char.upgraded)


Three_Big_Pigs = Character(
    name = 'Three Big Pigs',
    atk=15,
    hlth=15,
    alignment='Evil',
    lvl=6,
    type=['Animal'],
    abils=[
        Last_Breath_Effect(
            name='Three Big Pigs Death Effect',
            effect_func = Three_Big_Pigs_Last_Breath_Effect
        )
    ]
)

Pigomorph_Pig = Character(
        name = 'Pigomorph Pig',
        atk=10,
        hlth=10,
        lvl=1,
        type=['Animal'],
        token = True
)

objs=deepcopy(list(locals().keys()))
master_char_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Character):
        master_char_list.append(obj)
