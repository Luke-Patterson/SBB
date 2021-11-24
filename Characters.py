from c_Character import Character
from copy import deepcopy
from Effects import *
from datetime import datetime

# general condition for battle only triggered effects from characters
# requires the character be on the board to trigger
def battle_trigger_cond(source, triggering_obj):
    return triggering_obj.source in triggering_obj.source.owner.board.values()

# general condition for cast triggers
def char_cast_cond(source, condition_obj, in_combat):
    if in_combat == False:
        return True
    elif condition_obj.source in condition_obj.source.owner.board.values():
        return True
    else:
        return False

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
    char.change_eob_hlth_mod(3 * (1+ source.upgraded))

def Baby_Root_reverse_effect(char, source):
    char.change_eob_hlth_mod(-3 * (1+ source.upgraded))

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
    if char.position == None:
        position = char.last_position
    else:
        position = char.position
    token.summon(plyr = char.owner, position = position)

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
    name='Cinder-Ella',
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
            name = 'Crafty Static Effect',
            effect_func = lambda self: self.add_modifier(Crafty_Modifier),
            reverse_effect_func = lambda self: self.remove_modifier(Crafty_Modifier),
            modifier = Crafty_Modifier
        )
    ]
)

def Fanny_support_effect(char, source):
    char.change_eob_atk_mod(2 * (1+ source.upgraded))
    char.change_eob_hlth_mod(2 * (1+ source.upgraded))

def Fanny_reverse_effect(char, source):
    char.change_eob_atk_mod(-2 * (1+ source.upgraded))
    char.change_eob_hlth_mod(-2 * (1+ source.upgraded))

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

def Humpty_Dumpty_condition(source, obj):
    return obj.source in obj.source.owner.chars_dead

Humpty_Dumpty = Character(
    name='Humpty Dumpty',
    atk=7,
    hlth=7,
    alignment='Good',
    lvl=2,
    type=['Egg'],
    abils = [
        Triggered_Effect(
            name='Humpty Dumpty Effect',
            effect_func = Humpty_Dumpty_Last_Breath_Effect,
            trigger = Trigger(
                name='Humpty Dumpty Trigger',
                type='end of turn',
                condition = Humpty_Dumpty_condition
            )
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
            condition = lambda char: char.check_alignment('Evil'),
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
    char.change_eob_atk_mod(3 * (1+ source.upgraded))

def Mad_Mim_reverse_effect(char, source):
    char.change_eob_atk_mod(-3 * (1+ source.upgraded))

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
            condition = lambda char: char.check_alignment('Good'),
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

def Wizards_Familiar_effect(source, in_combat):
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
                type='cast',
                condition = char_cast_cond
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
    if source not in source.owner.board.values():
        import pdb; pdb.set_trace()

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
                type = 'survive damage',
                condition = lambda self, condition_obj: self.source.source in self.source.source.owner.board.values()
            )
        )
    ]
)

# Dubly
Dubly = Character(
    name = 'Dubly',
    atk=1,
    hlth=1,
    lvl=3,
    type=['Dwarf']
    # Dubly ability hardcoded into change_XXX_mod functions
)


# Good Witch of the North
def Good_Witch_support_effect(char, source):
    char.change_eob_atk_mod(2 * (1+ source.upgraded))
    char.change_eob_hlth_mod(3 * (1 + source.upgraded))

def Good_Witch_reverse_effect(char, source):
    char.change_eob_atk_mod(2 * (1+ source.upgraded))
    char.change_eob_hlth_mod(-3 * (1+ source.upgraded))

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
            condition = lambda char: char.check_alignment('Good')
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


def Ogre_Princess_effect(source, slain, slain_attribs):
    if source.upgraded:
        chars = [i for i in source.owner.game.char_pool if i.lvl==source.owner.lvl]
    else:
        chars = [i for i in source.owner.game.char_pool if i.lvl<=source.owner.lvl]
    selected = random.choice(chars)
    source.owner.game.char_pool.remove(selected)
    selected.owner = source.owner
    selected.add_to_hand(source.owner, store_in_shop=True)
    if source.owner.game.verbose_lvl>=3:
        print(source.owner,'gains',selected)

Ogre_Princess = Character(
    name = 'Ogre Princess',
    atk = 3,
    hlth = 2,
    alignment = 'Good',
    lvl=3,
    type=['Princess','Monster'],
    abils=[
        Triggered_Effect(
            name='Ogre Princess Slay effect',
            effect_func = Ogre_Princess_effect,
            trigger = Trigger(
                name = 'Ogre Princess Slay trigger',
                type = 'slay'
            )
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
    type=['Princess'],
    abils=[
        Last_Breath_Effect(
            name='Princess Peep Death Effect',
            effect_func = Princess_Peep_Last_Breath_Effect
        )
    ]
)

# def Princess_Wight_triggered_effect(source, dead_char):
#     source.change_atk_mod(1 * (1 + source.upgraded))
#     source.change_hlth_mod(1 * (1 + source.upgraded))

Princess_Wight_Modifier = Modifier(
    name = 'Princess Wight Modifier',
    atk_func = lambda char, atk, source: atk + char.owner.dwarves_bought * (char.upgraded + 1),
    hlth_func = lambda char, hlth, source: hlth + char.owner.dwarves_bought * (char.upgraded + 1)
)

# Princess Wight
Princess_Wight = Character(
    name = 'Princess Wight',
    atk=1,
    hlth=3,
    alignment='Evil',
    lvl=3,
    type=['Princess'],
    abils = [
        Local_Static_Effect(
            name = 'Princess Wight Static Effect',
            effect_func = lambda self: self.add_modifier(Princess_Wight_Modifier),
            reverse_effect_func = lambda self: self.remove_modifier(Princess_Wight_Modifier),
            modifier = Princess_Wight_Modifier
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
                condition = lambda self, char: char.check_alignment('Evil')
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
    if char.position == None:
        position = char.last_position
    else:
        position = char.position
    copy.summon(char.owner, position)

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

def Shadow_Assassin_trigger_cond(self, condition_obj, triggered_obj):
    result = any([i.trigger.type == 'slay' for i in condition_obj.abils
        if isinstance(i, Triggered_Effect)]) & (self.source.source in \
        self.source.source.owner.board.values())
    return result

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
                condition = Shadow_Assassin_trigger_cond
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

def Sleeping_Princess_Transform_func(char, targeted):
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
            effect_func = lambda source, in_combat: source.change_atk_mod(1 * (1+source.upgraded)),
            trigger = Trigger(
                name='Spell Weaver Trigger',
                type='cast',
                condition = char_cast_cond
            )
        )
    ]
)

# The White Stag
def The_White_Stag_effect(source, attacker):
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
        copy = selected.create_copy(source.owner, 'Trojan Donkey summon')
        copy.token = True
        copy.summon(source.owner, source.position)

# Trojan Donkey
Trojan_Donkey = Character(
    name = 'Trojan Donkey',
    atk=2,
    hlth=6,
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
    atk=2,
    hlth=3,
    alignment='Neutral',
    lvl=2,
    type=['Dwarf'],
    token = True
)

def Tweedle_Dee_Last_Breath_Effect(char):
    token = Tweedle_Dum.create_copy(char.owner, 'Tweedle Dee Death Effect')
    if char.upgraded:
        token.base_atk = 4
        token.base_hlth = 6
    if char.position == None:
        position = char.last_position
    else:
        position = char.position
    token.summon(char.owner, position)

Tweedle_Dee = Character(
    name = 'Tweedle Dee',
    atk=3,
    hlth=2,
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
    name='Vain-Pire',
    atk=4,
    hlth=4,
    alignment='Evil',
    lvl=3,
    type=['Monster'],
    abils=[
        Triggered_Effect(
            name='Vain-Pire Slay effect',
            effect_func = Vainpire_effect,
            trigger = Trigger(
                name = 'Vain-Pire Slay trigger',
                type = 'slay'
            )
        )
    ]
)


def Wicked_Witch_support_effect(char, source):
    char.change_eob_atk_mod(3 * (1+ source.upgraded))
    char.change_eob_hlth_mod(2 * (1 + source.upgraded))

def Wicked_Witch_reverse_effect(char, source):
    char.change_eob_atk_mod(-3 * (1+ source.upgraded))
    char.change_eob_hlth_mod(-2 * (1+ source.upgraded))

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
            condition = lambda char: char.check_alignment('Evil')
        )
    ]
)

# Wretched Mummy
def Wretched_Mummy_Last_Breath_Effect(char):
    chars = [i for i in char.owner.opponent.board.values() if i != None]
    if chars != [] and char.last_atk > 0:
        selected = random.choice(chars)
        selected.take_damage(char.last_atk, source=char)

Wretched_Mummy = Character(
    name = 'Wretched Mummy',
    atk=2,
    hlth=1,
    alignment='Evil',
    lvl=3,
    type=['Monster'],
    abils=[
        Last_Breath_Effect(
            name='Wretched Mummy Death Effect',
            effect_func = Wretched_Mummy_Last_Breath_Effect
        )
    ]
)

# Bearded Vulture
def Bearded_Vulture_triggered_effect(source, dead_char):
    source.change_eob_atk_mod(3 * (1 + source.upgraded))
    source.change_eob_hlth_mod(3 * (1 + source.upgraded))

Bearded_Vulture = Character(
    name = 'Bearded Vulture',
    atk=3,
    hlth=3,
    lvl=4,
    alignment='Evil',
    type=['Animal'],
    abils = [
        Triggered_Effect(
            name = 'Bearded Vulture Death Effect',
            effect_func = Bearded_Vulture_triggered_effect,
            trigger = Trigger(
                name='Bearded Vulture Death Effect trigger',
                type='die',
                condition = lambda self, char: 'Animal' in char.type
            )
        )
    ]
)

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
def Copycat_effect(source, attacker):
    back_targets = {1:[5], 2:(5,6), 3:(6,7), 4:[7]}
    if source.position in back_targets.keys():
        for i in back_targets[source.position]:
            if source.owner.board[i] != None:
                for abil in source.owner.board[i].abils:
                    if isinstance(abil, Last_Breath_Effect):
                        # trigger last breath effects once or twice, depending on
                        # whether copycat is upgraded. Also check for whether
                        # last breath multiplier comes into play.
                        for n in range(1+ source.upgraded + (source.owner.last_breath_multiplier- 1)
                            *(source.owner.last_breath_multiplier_used_this_turn==False)):
                            abil.apply_effect(source.owner.board[i])
                            if n != 0:
                                source.owner.last_breath_multiplier_used_this_turn = True

Copycat = Character(
    name = 'Copycat',
    atk=2,
    hlth=12,
    lvl=4,
    type=['Animal'],
    abils=[
        Triggered_Effect(
            name = 'Copycat attack effect',
            effect_func = Copycat_effect,
            trigger = Trigger(
                name='Copycat attack effect trigger',
                type='attack',
                condition = lambda self, char: self.source.source == char
            )
        )
    ]
)

# Court Wizard
def Court_Wizard_triggered_effect(source, dead_char):
    if dead_char.death_from_attacking:
        source.make_attack()

def Court_Wizard_cond(self, char):
    result = ('Prince' in char.type or 'Princess' in char.type) & \
        (self.source.source in self.source.source.owner.board.values())
    return result

Court_Wizard = Character(
    name = 'Court Wizard',
    atk = 4,
    hlth = 2,
    alignment = 'Good',
    lvl = 4,
    type = ['Mage'],
    keyword_abils=['ranged'],
    abils = [
        Triggered_Effect(
            name = 'Court Wizard Death Effect',
            effect_func = Court_Wizard_triggered_effect,
            trigger = Trigger(
                name='Court Wizard Death Effect trigger',
                type='die',
                condition = Court_Wizard_cond
            )
        )
    ]
)


# Fairy Godmother
def Fairy_Godmother_triggered_effect(source, dead_char):
    for i in source.owner.board.values():
        if i != None and i.check_alignment('Good'):
            source.change_eob_hlth_mod(2 * (1 + source.upgraded))

Fairy_Godmother = Character(
    name = 'Fairy Godmother',
    atk=4,
    hlth=4,
    alignment='Good',
    lvl=4,
    type=['Fairy'],
    abils = [
        Triggered_Effect(
            name = 'Fairy Godmother Death Effect',
            effect_func = Fairy_Godmother_triggered_effect,
            trigger = Trigger(
                name='Fairy Godmother Death Effect trigger',
                type='die',
                condition = lambda self, char: char.check_alignment('Good')
                    and self.source.source in self.source.source.owner.board.values()
            )
        )
    ]
)

# Friendly Spirit
def Friendly_Spirit_effect(char):
    chars = [i for i in char.owner.board.values() if i != None]
    if chars != []:
        selected = random.choice(chars)
        selected.change_eob_atk_mod(char.atk() * (1+ char.upgraded))
        selected.change_eob_hlth_mod(char.hlth() * (1+ char.upgraded))


Friendly_Spirit = Character(
    name = 'Friendly Spirit',
    atk = 3,
    hlth = 3,
    alignment = 'Good',
    lvl = 4,
    type=['Monster'],
    abils = [
        Last_Breath_Effect(
            name = 'Friendly Spirit Death Effect',
            effect_func = Friendly_Spirit_effect
        )
    ]
)

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
#
# def Grim_Soul_effect(char):
#     slay_abils = []
#     for i in char.owner.board.values():
#         if i != None:
#             for abil in i.abils:
#                 if isinstance(abil, Triggered_Effect) and abil.trigger.type=='slay' and \
#                     abil.name != 'Southern Siren Slay effect':
#                     slay_abils.append(abil)
#
#     if slay_abils != []:
#         selected = random.choice(slay_abils)
#         selected.trigger_effect(effect_kwargs={'slain':None,'slain_attribs':None})
#
# Grim_Soul = Character(
#     name = 'Grim Soul',
#     lvl=4,
#     atk=5,
#     hlth=1,
#     type = ['Monster'],
#     abils = [
#         Last_Breath_Effect(
#             name = 'Grim Soul Effect',
#             effect_func = Grim_Soul_effect
#         )
#     ]
# )

# Heartwood Elder
def Heartwood_Elder_support_effect(char, source):

    buff = 2 * (1 + source.upgraded)

    def Heartwood_Elder_effect(source):
        source.change_eob_atk_mod(buff)
        source.change_eob_hlth_mod(buff)

    Heartwood_Elder_buff_effect = Triggered_Effect(
        name = 'Heartwood Elder Buff Effect',
        effect_func = Heartwood_Elder_effect,
        trigger = Trigger(
            name='Heartwood Elder Buff trigger',
            type='start of combat',
            condition = battle_trigger_cond
        ),
    )

    char.abils.append(Heartwood_Elder_buff_effect)
    char.owner.triggers.append(Heartwood_Elder_buff_effect.trigger)
    Heartwood_Elder_buff_effect.add_to_obj(char)

def Heartwood_Elder_reverse_effect(char, source):
    rm_eff = [i for i in char.abils if i.name=='Heartwood Elder Buff Effect']
    if rm_eff != []:
        char.abils.remove(rm_eff[0])
        if rm_eff[0].trigger in source.get_owner().triggers:
            source.get_owner().triggers.remove(rm_eff[0].trigger)

Heartwood_Elder = Character(
    name = 'Heartwood Elder',
    atk = 5,
    hlth = 7,
    lvl= 4,
    type = ['Treant'],
    abils = [
        Support_Effect(
            name = 'Heartwood Elder support effect',
            effect_func = Heartwood_Elder_support_effect,
            reverse_effect_func = Heartwood_Elder_reverse_effect,
            condition = lambda char: 'Treant' in char.type
        )
    ]
)

# Hungry Hungry Hippocampus
def Hungry_Hungry_Hippocampus_summon_effect(source, summoned):
    source.change_hlth_mod(2 * (1+source.upgraded))

def Hungry_Hungry_Hippocampus_hlth_effect(char, eff):
    if eff.source != char:
        eff.source.change_hlth_mod(2 * (1+ eff.source.upgraded))

Hungry_Hungry_Hippocampus_purchase_effect = Purchase_Effect(
    name = 'Hungry Hungry Hippocampus Purchase Effect',
    effect_func = Hungry_Hungry_Hippocampus_hlth_effect,
    condition = lambda char: 'Animal' in char.type
)

def Hungry_Hungry_Hippocampus_effect(eff, player):
    copy = deepcopy(Hungry_Hungry_Hippocampus_purchase_effect)
    copy.source = eff.source
    player.effects.append(copy)


def Hungry_Hungry_Hippocampus_reverse_effect(eff, player):
    rm_eff = [i for i in player.effects if i.source==eff.source
        and i.name=='Hungry Hungry Hippocampus Purchase Effect']
    player.effects.remove(rm_eff[0])

Hungry_Hungry_Hippocampus = Character(
    name = 'Hungry Hungry Hippocampus',
    atk = 10,
    hlth = 1,
    alignment= 'Good',
    lvl=4,
    type=['Animal'],
    abils = [
        Triggered_Effect(
            name = 'Hungry Hungry Hippocampus Summon Effect',
            effect_func = Hungry_Hungry_Hippocampus_summon_effect,
            trigger = Trigger(
                name='Hungry Hungry Hippocampus Summon Effect trigger',
                type='summon',
                condition = lambda self, char: 'Animal' in char.type and
                    self.source.source in self.source.source.owner.board.values()
            )
        ),
        Player_Effect(
            name='Hungry Hungry Hippocampus Player Effect',
            effect_func= Hungry_Hungry_Hippocampus_effect,
            reverse_effect_func = Hungry_Hungry_Hippocampus_reverse_effect
        )
    ]
)



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
    char.change_eob_hlth_mod(5 * (1+ source.upgraded))

def Lady_of_the_Lake_reverse_effect(char, source):
    char.change_eob_hlth_mod(-5 * (1+ source.upgraded))

Lady_of_the_Lake = Character(
    name='Lady of the Lake',
    atk=3,
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
def Lightning_Dragon_effect(source):
    if any([i!= None for i in source.owner.opponent.board.values()]):
        source.make_attack()

Lightning_Dragon = Character(
    name = 'Lightning Dragon',
    atk = 10,
    hlth = 1,
    lvl=4,
    type=['Dragon'],
    keyword_abils = ['flying'],
    abils = [
         Triggered_Effect(
            name = 'Lightning Dragon triggered effect',
            effect_func = Lightning_Dragon_effect,
            trigger = Trigger(
                name='Lightning Dragon trigger',
                type='start of combat',
                condition = battle_trigger_cond
            ),
        )
    ]
)

# Medusa
Statue = Character(
    name = 'Statue',
    atk=0,
    hlth=6,
    lvl=1,
    type=['Statue'],
    token = True
)

def Medusa_effect(source, attacker):
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

#Prince Arthur
def Prince_Arthur_effect(source):
    for char in source.owner.board.values():
        if char != None and ('Prince' in char.type or 'Princess' in char.type) and char.upgraded:
            char.change_atk_mod(2 * (1 + source.upgraded))
            char.change_hlth_mod(2 * (1 + source.upgraded))


Prince_Arthur = Character(
    name = 'Prince Arthur',
    atk = 5,
    hlth = 5,
    alignment = 'Good',
    lvl = 4,
    type=['Prince'],
    abils = [
        Triggered_Effect(
            name = 'Prince Arthur triggered effect',
            effect_func = Prince_Arthur_effect,
            trigger = Trigger(
                name='Prince Arthur trigger',
                type='start of combat',
                condition = battle_trigger_cond
            ),
        )
    ]
)

# # Princess Pea
# def Princess_Pea_atk_func(char, atk, source):
#     support_effs = [i for i in char.eob_reverse_effects if isinstance(i, Support_Effect)]
#     chars = list(set([i.source for i in support_effs]))
#     return atk + 4 * len(chars) * (1 + char.upgraded)
#
# def Princess_Pea_hlth_func(char, hlth, source):
#     support_effs = [i for i in char.eob_reverse_effects if isinstance(i, Support_Effect)]
#     chars = list(set([i.source for i in support_effs]))
#     return hlth + 4 * len(chars) * (1 + char.upgraded)
#
# Princess_Pea_Modifier = Modifier(
#     name = 'Princess Pea Modifier',
#     atk_func = Princess_Pea_atk_func,
#     hlth_func = Princess_Pea_hlth_func
# )
# Princess_Pea = Character(
#     name = 'Princess Pea',
#     atk = 4,
#     hlth = 4,
#     alignment='Good',
#     lvl=4,
#     type=['Princess'],
#     abils = [
#         Local_Static_Effect(
#             name = 'Princess Pea Static Effect',
#             effect_func = lambda self: self.add_modifier(Princess_Pea_Modifier),
#             reverse_effect_func = lambda self: self.remove_modifier(Princess_Pea_Modifier),
#             modifier = Princess_Pea_Modifier
#         )
#     ]
# )


# Puff Puff
def Puff_Puff_effect(char):
    for i in char.owner.hand:
        if i.name == 'Puff Puff':
            i.change_atk_mod(1 * (1+char.upgraded))
            i.change_hlth_mod(1 * (1+char.upgraded))

Puff_Puff = Character(
    name = 'Puff Puff',
    atk=7,
    hlth =7,
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
def Riverwish_Mermaid_support_effect(char, source):

    buff = 1 * (1 + source.upgraded)

    def Riverwish_Mermaid_effect(source, slain, slain_attribs):
        source.change_atk_mod(buff)
        source.change_hlth_mod(buff)

    Riverwish_Mermaid_buff_effect = Triggered_Effect(
        name = 'Riverwish Mermaid Buff Effect',
        effect_func = Riverwish_Mermaid_effect,
        trigger = Trigger(
            name='Riverwish Mermaid Buff trigger',
            type='slay'
        ),
    )

    char.abils.append(Riverwish_Mermaid_buff_effect)
    char.owner.triggers.append(Riverwish_Mermaid_buff_effect.trigger)
    Riverwish_Mermaid_buff_effect.add_to_obj(char)

def Riverwish_Mermaid_reverse_effect(char, source):
    rm_eff = [i for i in char.abils if i.name=='Riverwish Mermaid Buff Effect']
    if rm_eff != []:
        char.abils.remove(rm_eff[0])
        if rm_eff[0].trigger in source.get_owner().triggers:
            source.get_owner().triggers.remove(rm_eff[0].trigger)

Riverwish_Mermaid = Character(
    name = 'Riverwish Mermaid',
    atk = 4,
    hlth = 4,
    lvl= 4,
    type = ['Princess'],
    abils = [
        Support_Effect(
            name = 'Riverwish Mermaid support effect',
            effect_func = Riverwish_Mermaid_support_effect,
            reverse_effect_func = Riverwish_Mermaid_reverse_effect
        )
    ]
)

# Sheep in Wolf's clothing
Bad_Sheep = Character(
    name = 'Sheep',
    atk=6,
    hlth=6,
    lvl=1,
    alignment='Evil',
    type=['Animal'],
    token = True
)

def Sheep_in_Wolfs_Clothing_Last_Breath_Effect(char):
    token = Bad_Sheep.create_copy(char.owner, 'Sheep in Wolfs Clothing death effect')
    token.base_atk = token.base_atk * (1+ char.upgraded)
    token.base_hlth = token.base_hlth * (1+ char.upgraded)
    if char.position == None:
        position = char.last_position
    else:
        position = char.position
    token.summon(char.owner, position)

Sheep_in_Wolfs_Clothing = Character(
    name = "Sheep in Wolf's Clothing",
    atk=2,
    hlth=2,
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

Soltak_Ancient = Character(
    name = 'Soltak Ancient',
    atk = 0,
    hlth = 20,
    alignment = 'Good',
    lvl=4,
    type=['Treant']
    # Soltak Ancient ability hardcoded into damage dealing
)

# Sporko
def Sporko_support_effect(char, source):
    char.change_eob_atk_mod(5 * (1+ source.upgraded))

def Sporko_reverse_effect(char, source):
    char.change_eob_atk_mod(-5 * (1+ source.upgraded))

Sporko = Character(
    name='Sporko',
    atk=3,
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
    name='The Nutcracker',
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
def Aon_trigger_effect(source, in_combat):
    if in_combat:
        effect_chars = [i for i in source.owner.board.values() if i!= None and
            'Mage' in i.type]
    else:
        effect_chars = [i for i in source.owner.hand if i!= None and
            'Mage' in i.type]
    for i in effect_chars:
        i.change_atk_mod(1 * (1+source.upgraded))


def Aon_slay_effect(source, slain, slain_attribs):
    reduce_val = 1 * (1 + source.upgraded)
    spell_reduce_effect = Shop_Effect(
                name="Aon shop effect",
                spell_effect_func = lambda spell: spell.change_cost(-1 * reduce_val),
                spell_reverse_effect_func = lambda spell: spell.reset_cost(),
                eob = True
            )

    source.owner.effects.append(spell_reduce_effect)
    for i in source.owner.shop:
        spell_reduce_effect.apply_effect(i)

Aon = Character(
    name = 'Aon',
    atk = 6,
    hlth = 12,
    alignment = 'Evil',
    lvl = 5,
    type = ['Mage'],
    abils = [
        Triggered_Effect(
            name='Aon triggered effect',
            effect_func = Aon_trigger_effect,
            trigger = Trigger(
                name='Aon Trigger',
                type='cast',
                condition = char_cast_cond
            )
        ),
        Triggered_Effect(
            name='Aon Slay effect',
            effect_func = Aon_slay_effect,
            trigger = Trigger(
                name = 'Aon Slay trigger',
                type = 'slay'
            )
        )

    ]
)

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
    if char.position == None:
        position = char.last_position
    else:
        position = char.position
    token.summon(plyr = char.owner, position = position)


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
    if char.position == None:
        position = char.last_position
    else:
        position = char.position
    token.summon(plyr = char.owner, position = position)

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
    if char.position == None:
        position = char.last_position
    else:
        position = char.position
    token.summon(plyr = char.owner, position = position)

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

def Cupid_effect(source, damage_dealt, damaged_char, attacking):
    # check to make sure the cupid attack hasn't killed the damaged character and its attacking
    if damaged_char.dmg_taken < damaged_char.hlth() and attacking and damaged_char.owner != None:
        damaged_char.make_attack(player = damaged_char.owner)


Cupid = Character(
    name = 'Cupid',
    atk = 1,
    hlth = 10,
    alignment = 'Good',
    lvl =5,
    keyword_abils = ['ranged', 'flying'],
    type = ['Fairy'],
    abils = [
        Triggered_Effect(
            name = 'Cupid damage effect',
            effect_func = Cupid_effect,
            trigger = Trigger(
                name = 'Cupid damage trigger',
                type = 'deal damage',
                condition = lambda self, condition_obj: self.source.source == condition_obj
            )
        )
    ]
)


# Lancelot
def Lancelot_slay_effect(source, slain, slain_attribs):
    source.change_atk_mod(2 * (1+ source.upgraded))
    source.change_hlth_mod(2 * (1+ source.upgraded))

def Lancelot_condition(source, abil):
    return abil.source.atk() >= 25 or abil.source.hlth() - abil.source.dmg_taken >=25

Lancelot = Character(
    name='Lancelot',
    atk=7,
    hlth=7,
    alignment='Good',
    lvl=5,
    type=['Prince','Mage'],
    abils = [
        Triggered_Effect(
            name='Lancelot Slay effect',
            effect_func = Lancelot_slay_effect,
            trigger = Trigger(
                name = 'Lancelot Slay trigger',
                type = 'slay'
            )
        ),
        Quest(
            name= 'Lancelot Quest',
            trigger = Trigger(
                name='Lancelot Quest Trigger',
                type='atk/hlth >25',
                condition = Lancelot_condition
            ),
            counter = 1
        )
    ]
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
)


# Rotten Appletree
def Rotten_Appletree_effect(source, attacker):
    attacker.dmg_taken = 0
    hlth_mod = (attacker.hlth() - 1) * -1
    attacker.change_eob_hlth_mod(hlth_mod)

Rotten_Appletree = Character(
    name = 'Rotten Appletree',
    atk = 0,
    hlth = 18,
    alignment = 'Evil',
    lvl = 5,
    type = ['Treant'],
    abils = [
        Triggered_Effect(
            name = 'Rotten Appletree attack effect',
            effect_func = Rotten_Appletree_effect,
            trigger = Trigger(
                name='Rotten Appletree attacked effect trigger',
                type='attacked',
                condition = lambda self, char: self.source.source == char
            )
        )
    ]
)

# Shoulder Fairy
def Shoulder_Faeries_effect(source):
    good_chars = [i for i in source.owner.board.values() if i != None and i.check_alignment('Good')]
    evil_chars = [i for i in source.owner.board.values() if i != None and i.check_alignment('Evil')]
    if good_chars != []:
        hlth_pump = max([i.hlth() for i in good_chars] + [0])
        source.change_eob_hlth_mod(hlth_pump * (1+source.upgraded))
    if evil_chars != []:
        atk_pump = max([i.atk() for i in evil_chars] + [0])
        source.change_eob_atk_mod(atk_pump * (1+source.upgraded))

Shoulder_Faeries = Character(
    name = 'Shoulder Faeries',
    atk = 1,
    hlth = 1,
    alignment = 'Neutral',
    lvl =5,
    type = ['Fairy'],
    abils = [
        Triggered_Effect(
            name = 'Shoulder Faeries triggered effect',
            effect_func = Shoulder_Faeries_effect,
            trigger = Trigger(
                name='Shoulder Faeries trigger',
                type='start of combat',
                condition = battle_trigger_cond
            ),
        )
    ]
)


# Southern Siren
def Southern_Siren_effect(source, slain, slain_attribs):
    for _ in range(1 * (1+source.upgraded)):
        if source.position==None:
            start_pos = source.last_position
        else:
            start_pos = source.position
        copy = slain.create_copy(source.owner, 'Southern Siren summon', plain_copy=False)
        copy.token = True

        # reattach the original slain char's attributes to the char
        for i in slain_attribs.keys():
            copy.__dict__[i] = slain_attribs[i]

        copy.summon(plyr = source.owner, position = start_pos)

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
    if char.position == None:
        position = char.last_position
    else:
        position = char.position
    copy.summon(plyr = char.owner, position = position)

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



# Ashwood Elm
def Ashwood_Elm_effect(source):
    for char in source.owner.board.values():
        if char != None and ('Treant' in char.type):
            char.change_atk_mod(source.hlth() * (1 + source.upgraded))
            char.change_hlth_mod(source.hlth() * (1 + source.upgraded))


Ashwood_Elm = Character(
    name = 'Ashwood Elm',
    atk = 0,
    hlth = 20,
    alignment = 'Evil',
    lvl = 6,
    type=['Treant'],
    abils = [
        Triggered_Effect(
            name = 'Ashwood Elm triggered effect',
            effect_func = Ashwood_Elm_effect,
            trigger = Trigger(
                name='Ashwood Elm trigger',
                type='start of combat',
                condition = battle_trigger_cond
            ),
        )
    ]
)

# Bearstein
Bearstein_Modifier = Modifier(
    name= 'Bearstein Modifier',
    atk_func = lambda char, atk, source: atk + 2 * (1 + source.upgraded),
    hlth_func = lambda char, hlth, source: hlth + 2 * (1 + source.upgraded)
)

def Bearstein_summon_effect(source, summoned):
    summoned.change_eob_atk_mod(summoned.atk() * (1 + source.upgraded))
    summoned.change_eob_hlth_mod(summoned.hlth() * (1 + source.upgraded))

Bearstein = Character(
    name = 'Bearstein',
    atk = 5,
    hlth = 8,
    alignment = 'Good',
    lvl = 6,
    type = ['Animal'],
    abils = [
        Global_Static_Effect(
            name = 'Bearstein effect',
            effect_func = lambda char: char.add_modifier(Bearstein_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Bearstein_Modifier),
            condition = lambda char: 'Animal' in char.type,
            modifier = Bearstein_Modifier
        ),
        Triggered_Effect(
            name = 'Bearstein Summon Effect',
            effect_func = Bearstein_summon_effect,
            trigger = Trigger(
                name='Bearstein Summon Effect trigger',
                type='summon',
                condition = lambda self, char: 'Animal' in char.type and
                    self.source.source in self.source.source.owner.board.values()
            )
        )
    ]
)

# Doombreath
def Doombreath_effect(source, damage_dealt, damaged_char, attacking):
    # check to make sure the cupid attack hasn't killed the damaged character and its attacking
    back_targets = {1:[5], 2:(5,6), 3:(6,7), 4:[7]}
    if damaged_char.position in back_targets.keys() and attacking:
        for i in back_targets[damaged_char.position]:
            if source.owner.board[i] != None:
                source.owner.board[i].take_damage(amt = damage_dealt, source = source,
                    attacking = True)

Doombreath = Character(
    name = 'Doombreath',
    atk = 10,
    hlth = 6,
    alignment = 'Evil',
    lvl =6,
    type = ['Dragon'],
    abils = [
        Triggered_Effect(
            name = 'Doombreath damage effect',
            effect_func = Doombreath_effect,
            trigger = Trigger(
                name = 'Doombreath damage trigger',
                type = 'deal damage',
                condition = lambda self, condition_obj: self.source.source == condition_obj
            )
        )
    ]
)

# Echowood
def Echowood_effect(source, amt, type):
    if type == 'atk' and amt > 0 and source.position != None:
        source.change_eob_atk_mod(amt * (1 + source.upgraded))
    if type == 'hlth' and amt > 0 and source.position != None:
        source.change_eob_hlth_mod(amt * (1 + source.upgraded))

Echowood = Character(
    name = 'Echowood',
    atk=1,
    hlth=1,
    lvl=6,
    type=['Treant'],
    abils = [
        Triggered_Effect(
            name = 'Echowood attack effect',
            effect_func = Echowood_effect,
            trigger = Trigger(
                name='Echowood effect trigger',
                type='change_mod',
                # condition is to make sure it only pumps while in combat
                condition = lambda self, condition_obj: condition_obj.source.owner.opponent != None
            )
        )
    ]
)

# Good Boy
def Good_Boy_Last_Breath_Effect(char):
    for i in char.owner.board.values():
        if i != None and i.check_alignment('Good'):
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
    if char.position == None:
        start_pos = char.last_position
    else:
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
    evil_dead_chars = [i for i in char.owner.chars_dead if i.check_alignment('Evil')]
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
            elig_pool = [i for i in char.game.char_pool if i.check_alignment('Evil') and
                i.lvl == get_lvl]
            selected = random.choice(elig_pool)
            copy = selected.create_copy(char.owner, 'Great Pumpkin King summon')
            copy.token = True
            if char.upgraded:
                copy.upgraded = True
            copy.summon(char.owner, pos)

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
    char.change_eob_atk_mod(10 * (1+ source.upgraded))

def Grumblegore_reverse_effect(char, source):
    char.change_eob_atk_mod(-10 * (1+ source.upgraded))

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
Hercules = Character(
    name = 'Hercules',
    atk = 20,
    hlth = 20,
    alignment='Good',
    lvl=6,
    type=['Prince'],
    abils=[
        Quest(
            name= 'Hercules Quest',
            trigger = Trigger(
                name='Hercules Quest Trigger',
                type='deal damage',
                condition = lambda self, condition_obj: self.source.source == condition_obj
            ),
            counter = 100
        )
    ]
)

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
def Lordy_effect(source):
    affected = [i for i in source.owner.board.values() if i != None and
        ('Dwarf' in i.type or i.name =='Princess Wight')]
    for i in affected:
        i.change_eob_atk_mod(2 * len(affected) * (1+ source.upgraded))
        i.change_eob_hlth_mod(2 * len(affected) * (1+ source.upgraded))

Lordy = Character(
    name = 'Lordy',
    atk = 7,
    hlth = 7,
    alignment = 'Neutral',
    lvl =6,
    type = ['Dwarf'],
    abils = [
        Triggered_Effect(
            name = 'Lordy triggered effect',
            effect_func = Lordy_effect,
            trigger = Trigger(
                name='Lordy trigger',
                type='start of combat',
                condition = battle_trigger_cond
            ),
        )
    ]
)

# Robin Wood
def Robin_Wood_effect(source):
    chars = [i for i in source.owner.board.values() if i != None]
    opp_chars = [i for i in source.owner.opponent.board.values() if i != None]
    if chars != [] and opp_chars != []:
        highest_atk = max([i.atk() for i in opp_chars])
        highest_atk_opp_char = [i for i in opp_chars if i.atk()==highest_atk][0]
        lowest_atk = min([i.atk() for i in chars])
        lowest_atk_char = [i for i in chars if i.atk()==lowest_atk][0]
        highest_atk_opp_char.change_eob_atk_mod(-15 * (1 + source.upgraded))
        lowest_atk_char.change_eob_atk_mod(15 * (1 + source.upgraded))

Robin_Wood = Character(
    name = 'Robin Wood',
    atk = 7,
    hlth = 10,
    alignment = 'Good',
    lvl =6,
    type = ['Treant'],
    abils = [
        Triggered_Effect(
            name = 'Robin Wood triggered effect',
            effect_func = Robin_Wood_effect,
            trigger = Trigger(
                name='Robin Wood trigger',
                type='start of combat',
                condition = battle_trigger_cond
            ),
        )
    ]
)

# The Green Knight
def Green_Knight_support_effect(char, source):
    char.change_eob_hlth_mod(10 * (1+ source.upgraded))

def Green_Knight_reverse_effect(char, source):
    char.change_eob_hlth_mod(-10 * (1+ source.upgraded))

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

def The_Oni_King_effect(source, attacker):
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
                condition = lambda self, char: 'Monster' in char.type and
                    self.source.source in self.source.source.owner.board.values()
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

def Captain_Croc_last_breath_effect(char):
    token = char.trackers['Croc_Bait_char'].create_copy(char.owner, 'Captain Croc Last Breath')
    if char.position == None:
        position = char.last_position
    else:
        position = char.position
    token.summon(plyr = char.owner, position = position)

Captain_Croc = Character(
    name = 'Captain Croc',
    atk = 10,
    hlth = 10,
    lvl = 6,
    alignment = 'Evil',
    type = ['Animal'],
    inshop = False,
    abils = [
        Last_Breath_Effect(
            name = 'Captain Croc Last Breath Effect',
            effect_func = Captain_Croc_last_breath_effect
        )
    ]
)

objs=deepcopy(list(locals().keys()))
master_char_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Character):
        master_char_list.append(obj)
