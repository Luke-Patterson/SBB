from c_Character import Character
from copy import deepcopy
from Effects import *

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
    char.hlth_mod += 3 * (1+ source.upgraded)

def Baby_Root_reverse_effect(char, source):
    char.hlth_mod -= 3 * (1+ source.upgraded)

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
    name = '1/1 Cat',
    atk=1,
    hlth=1,
    alignment='Evil',
    lvl=2,
    type=['Animal'],
    token = True
)

def Black_Cat_Death_Effect(char):
    token = Cat_1_1.create_token(char.owner)
    if char.upgraded:
        token.base_atk = 2
        token.base_hlth = 2
    char.owner.board[char.position] = token
    token.position = char.position

Black_Cat = Character(
    name = 'Black Cat',
    atk=1,
    hlth=1,
    alignment='Evil',
    lvl=2,
    type=['Animal'],
    abils=[
        Death_Effect(
            name='Black Cat Death Effect',
            effect_func = Black_Cat_Death_Effect
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
    char.atk_mod += 2 * (1+ source.upgraded)
    char.hlth_mod += 2 * (1+ source.upgraded)

def Fanny_reverse_effect(char, source):
    char.atk_mod -= 2 * (1+ source.upgraded)
    char.hlth_mod -= 2 * (1+ source.upgraded)

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
            effect_func = lambda source: source.increase_hlth_mod( 2 * (1+source.upgraded)),
            trigger = Trigger(
                name='Happy Little Tree Trigger',
                type='end of turn'
            )
        )
    ]
)

def Humpty_Dumpty_death_effect(self):
    self.remove_from_hand()

Humpty_Dumpty = Character(
    name='Humpty Dumpty',
    atk=6,
    hlth=6,
    alignment='Good',
    lvl=2,
    type=['Egg'],
    abils = [
        Death_Effect(
            name = 'Humpty Dumpty',
            effect_func = Humpty_Dumpty_death_effect
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
            effect_func = lambda source: source.owner.gain_gold_next_turn(1 * (1 + source.upgraded)),
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
    atk=5,
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

def Mad_Mim_support_effect(char, source):
    char.hlth_mod += 3 * (1+ source.upgraded)

def Mad_Mim_reverse_effect(char, source):
    char.hlth_mod -= 3 * (1+ source.upgraded)


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
    eff.source.permanent_transform(deepcopy(Frog_Prince))

Lonely_Prince_Transform = Purchase_Effect(
    name='Lonely Prince Purchase Effect',
    effect_func = Lonely_Prince_Transform_func,
    condition = lambda char: 'Princess' in char.type
)

# def Lonely_Prince_effect(eff, player):
#     copy = deepcopy(Lonely_Prince_Transform)
#     copy.source = eff.source
#     player.effects.append(copy)
#
#
# def Lonely_Prince_reverse_effect(eff, player):
#     rm_eff = [i for i in player.effects if i.source==eff.source]
#     assert len(rm_eff)>0
#     player.effects.remove(rm_eff[0])
#
# Lonely_Prince = Character(
#     name = 'Lonely Prince',
#     lvl =2,
#     alignment='Good',
#     atk=1,
#     hlth=1,
#     type=['Prince'],
#     abils=[
#         Player_Effect(
#             name='Lonely Prince Effect',
#             effect_func= Lonely_Prince_effect,
#             reverse_effect_func = Lonely_Prince_reverse_effect
#         )
#     ]
# )

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

Rainbow_Unicorn_Modifier = Modifier(
    name= 'Rainbow Unicorn Modifier',
    hlth_func = lambda char, hlth, source: hlth + 1 * (1 + source.upgraded)
)


Rainbow_Unicorn = Character(
    name='Rainbow Unicorn',
    atk=1,
    hlth=5,
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
    keyword_abils = ['Ranged'],
    type=['Princess']
)

def Wizards_Familiar_effect(source):
    source.increase_atk_mod(1 * (1+source.upgraded))
    source.increase_hlth_mod(1 * (1+source.upgraded))

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

Adventurer = Character(
    name = "Adventurer",
    atk=1,
    hlth=1,
    alignment='Good',
    lvl=3,
    type=['Princess'],
    abils=[
        Triggered_Effect(
            name='Adventurer Slay effect',
            effect_func = lambda source: source.owner.gain_xp(1 * (1 + source.upgraded)),
            trigger = Trigger(
                name = 'Adventurer Slay trigger',
                type = 'slay'
            )
        )
    ]
)

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

# Darkwood Creeper

# Dubly

# Good Witch of the North
def Good_Witch_support_effect(char, source):
    char.atk_mod += 2 * (1+ source.upgraded)
    char.hlth_mod += 3 * (1 + source.upgraded)

def Good_Witch_reverse_effect(char, source):
    char.atk_mod -= 2 * (1+ source.upgraded)
    char.hlth_mod -= 3 * (1+ source.upgraded)

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

# Princess Peep

# Princess Wight

# Prized Pig

# Queen of Hearts

# Romeo

# Shadow Assassin

# Sleeping Princess

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
            effect_func = lambda source: source.increase_atk_mod(1 * (1+source.upgraded)),
            trigger = Trigger(
                name='Spell Weaver Trigger',
                type='cast'
            )
        )
    ]
)

# The White Stag
# Trojan Donkey

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

def Tweedle_Dee_Death_Effect(char):
    token = Tweedle_Dum.create_token(char.owner)
    if char.upgraded:
        token.base_atk = 2
        token.base_hlth = 8
    char.owner.board[char.position] = token
    token.position = char.position

Tweedle_Dee = Character(
    name = 'Tweedle Dee',
    atk=4,
    hlth=1,
    alignment='Neutral',
    lvl=3,
    type=['Dwarf'],
    abils=[
        Death_Effect(
            name='Tweedle Dee Death Effect',
            effect_func = Tweedle_Dee_Death_Effect
        )
    ]
)

def Vainpire_effect(source):
    source.increase_atk_mod(1 * (1+source.upgraded))
    source.increase_hlth_mod(1 * (1+source.upgraded))

# Vain-Pire
Vainpire = Character(
    name='Vain-pire',
    atk=3,
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
    char.atk_mod += 3 * (1+ source.upgraded)
    char.hlth_mod += 2 * (1 + source.upgraded)

def Wicked_Witch_reverse_effect(char, source):
    char.atk_mod -= 3 * (1+ source.upgraded)
    char.hlth_mod -= 2 * (1+ source.upgraded)

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
# Bossy
# Broc Lee
# Copycat
# Court Wizard
# Fairy Godmother
# Friendly Spirit
# Greedy
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
# Prince Arthur
# Princess Pea
# Puff Puff
# Riverwish Mermaid

# Sheep in Wolf's clothing
Sheep = Character(
    name = 'Sheep',
    atk=5,
    hlth=5,
    alignment='Evil',
    lvl=2,
    type=['Animal'],
    token = True
)

def Sheep_in_Wolfs_Clothing_Death_Effect(char):
    token = Sheep.create_token(char.owner)
    token.base_atk = token.base_atk * (1+ char.upgraded)
    token.base_hlth = token.base_hlth * (1+ char.upgraded)
    char.owner.board[char.position] = token
    token.position = char.position

Sheep_in_Wolfs_Clothing = Character(
    name = "Sheep in Wolf's Clothing",
    atk=1,
    hlth=1,
    alignment='Evil',
    lvl=4,
    type=['Animal'],
    abils=[
        Death_Effect(
            name="Sheep in Wolf's Clothing Death Effect",
            effect_func = Sheep_in_Wolfs_Clothing_Death_Effect
        )
    ]
)

# Sporko
def Sporko_support_effect(char, source):
    char.atk_mod += 5 * (1+ source.upgraded)

def Sporko_reverse_effect(char, source):
    char.atk_mod -= 5 * (1+ source.upgraded)

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
# The Nutcracker
# Angry
# Aon
# Baba Yaga
# Baby Bear
# Cupid
# Lancelot
# Lancelot = Character(
#     name='Lancelot',
#     atk=7,
#     hlth=7,
#     alignment='Good',
#     lvl=2,
#     type=['Princess','Mage'],
#     abils = [
#         Quest(
#             name= 'Cinder-ella Quest',
#             trigger = Trigger(
#                 name='Cinder-ella Quest Trigger',
#                 type='cast'
#             ),
#             counter = 1
#         )
#     ]
# )
# Monster Book
# Nian, Sea Terror
# Rotten Appletree
# Soltak Ancient
# Southern Siren
# Wombats in Disguise
# Wretched Mummy
# Ashwood Elm
# Bearstein
# Doombreath
# Echowood
# Good Boy
# Great Pumpkin King
# Grumblegore
def Grumblegore_support_effect(char, source):
    char.atk_mod += 10 * (1+ source.upgraded)

def Grumblegore_reverse_effect(char, source):
    char.atk_mod -= 10 * (1+ source.upgraded)

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
# Lordy
# Robin Wood
# Shoulder Faeries
# The Green Knight
def Green_Knight_support_effect(char, source):
    char.hlth_mod += 10 * (1+ source.upgraded)

def Green_Knight_reverse_effect(char, source):
    char.hlth_mod -= 10 * (1+ source.upgraded)

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

# The Oni King
# The Storm King
# Three Big Pigs

objs=deepcopy(list(locals().keys()))
master_char_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Character) and obj.token==False and obj.inshop:
        master_char_list.append(obj)
