from c_Hero import Hero
from copy import deepcopy
from Effects import *
from Spells import Knighthood
#from Spells import It_Was_All_A_Dream
from Spells import Kidnap
import random

def Apocalypse_cond(source, condition_obj):
    plyr =condition_obj.source.owner
    return plyr.lvl == 6 and plyr.trackers['Apocalypse_abil_used'] == False

def Apocalypse_effect(source):
    handcopy = source.owner.hand.copy()
    for char in handcopy:
        char.remove_from_hand()

    elig_pool = [i for i in source.owner.game.char_pool if i.lvl == 6]
    selected_chars = random.sample(elig_pool, 7)
    for char in selected_chars:
        char.add_to_hand(source.owner)
        source.owner.game.char_pool.remove(char)


    source.owner.trackers['Apocalypse_abil_used'] = True

Apocalypse = Hero(name='Apocalypse',
    life=50,
    abils = [
        Triggered_Effect(
            name = "Apocalypse lvl 6 effect",
            effect_func = Apocalypse_effect,
            trigger = Trigger(
                name= "Apocalypse trigger",
                type= "start of turn",
                condition = Apocalypse_cond
            )
        )
    ]
)

def Celestial_Tiger_cond(effect):
    # small workaround for Treasure_Effect_Multiplier which feeds a treasure instead of
    # effect object for this condition.
    if isinstance(effect, Treasure) == False:
        treasure = effect.source
    else:
        treasure = effect

    return treasure.lvl <= 3

Celestial_Tiger = Hero(
    name='Celestial Tiger',
    abils = [
        Treasure_Effect_Multiplier(
            name = 'Celestial Tiger Treasure Effect Multiplier',
            condition = Celestial_Tiger_cond
        )
    ]
)


def Charon_effect(source, dead_char):
    dead_char.change_atk_mod(2)
    dead_char.change_hlth_mod(1)

Charon = Hero(
    name='Charon',
    abils = [
        Triggered_Effect(
            name = 'Charon effect',
            effect_func = Charon_effect,
            trigger = Trigger(
                name = 'Charon effect trigger',
                type = 'die',
                condition = lambda self, char: char.lvl > 1
            ),
            once_per_turn = True
        )
    ]
)

def Evella_dead_animal_counter_effect(source, dead_char):
    source.owner.trackers['Animals_dead_this_combat'] += 1

def Evella_reset_animal_counter(source):
    source.owner.trackers['Animals_dead_this_combat'] = 0


Evella_Modifier = Modifier(
    name= 'Evella Modifier',
    atk_func = lambda char, atk, source: atk + char.owner.trackers['Animals_dead_this_combat']
)

Evella = Hero(
    name='Evella',
    abils = [
        Triggered_Effect(
            name = 'Evella dead animal counter',
            effect_func = Evella_dead_animal_counter_effect,
            trigger = Trigger(
                name = 'Evella effect trigger',
                type = 'die',
                condition = lambda self, char: 'Animal' in char.type
            ),
        ),
        Global_Static_Effect(
            name = 'Evella dead animal pump',
            effect_func = lambda char: char.add_modifier(Evella_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Evella_Modifier),
            condition = lambda char: char.check_alignment('Evil'),
            modifier= Evella_Modifier
        ),

        Triggered_Effect(
            name = "Evella reset animal counter",
            effect_func = Evella_reset_animal_counter,
            trigger = Trigger(
                name= "Evella trigger",
                type= "end of turn"
            ),
        ),
    ]
)

def Fallen_Angel_atk_chk(source):
    evil_chars = len([i for i in source.owner.board.values() if i != None and
        i.check_alignment('Evil')])
    if evil_chars >=3:
        source.owner.trackers['Fallen_Angel_atk_chk'] = True
    else:
        source.owner.trackers['Fallen_Angel_atk_chk'] = False

def Fallen_Angel_hlth_chk(source):
    good_chars = len([i for i in source.owner.board.values() if i != None and
        i.check_alignment('Good')])
    if good_chars >=3:
        source.owner.trackers['Fallen_Angel_hlth_chk'] = True
    else:
        source.owner.trackers['Fallen_Angel_hlth_chk'] = False

Fallen_Angel_atk_Modifier = Modifier(
    name= 'Fallen Angel atk Modifier',
    atk_func = lambda char, atk, source: atk + 2
)

Fallen_Angel_hlth_Modifier = Modifier(
    name= 'Fallen Angel hlth Modifier',
    hlth_func = lambda char, hlth, source: hlth + 2
)

Fallen_Angel = Hero(
    name='Fallen Angel',
    abils = [
        Triggered_Effect(
            name = 'Fallen Angel atk pump check',
            effect_func = Fallen_Angel_atk_chk,
            trigger= Trigger(
                name = 'Fallen Angel atk check trigger',
                type = 'start of combat'
            ),
        ),
        Triggered_Effect(
            name = 'Fallen Angel hlth pump check',
            effect_func = Fallen_Angel_hlth_chk,
            trigger= Trigger(
                name = 'Fallen Angel hlth check trigger',
                type = 'start of combat'
            )
        ),
        Global_Static_Effect(
            name = 'Fallen Angel atk pump',
            effect_func = lambda char: char.add_modifier(Fallen_Angel_atk_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Fallen_Angel_atk_Modifier),
            condition = lambda char: char.owner.trackers['Fallen_Angel_atk_chk'],
            modifier= Fallen_Angel_atk_Modifier
        ),
        Global_Static_Effect(
            name = 'Fallen Angel hlth pump',
            effect_func = lambda char: char.add_modifier(Fallen_Angel_hlth_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Fallen_Angel_hlth_Modifier),
            condition = lambda char: char.owner.trackers['Fallen_Angel_hlth_chk'],
            modifier= Fallen_Angel_hlth_Modifier
        )
    ]
)

def Geppetto_effect(source, summoned):
    summoned.change_eob_atk_mod(summoned.owner.lvl)
    summoned.change_eob_hlth_mod(summoned.owner.lvl)

Geppetto = Hero(name='Geppetto',
    abils = [
        Triggered_Effect(
            name = 'Geppetto effect',
            effect_func = Geppetto_effect,
            trigger = Trigger(
                name = 'Geppetto effect trigger',
                type = 'summon'
            )
        )
    ]
)

Grandmother_Modifier = Modifier(
    name= 'Grandmother Modifier',
    atk_func = lambda char, atk, source: atk + 5,
    hlth_func = lambda char, hlth, source: hlth + 5
)

Grandmother = Hero(name='Grandmother',
    life = 50,
    abils=[
        Global_Static_Effect(
            name = 'Grandmother effect',
            effect_func = lambda char: char.add_modifier(Grandmother_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Grandmother_Modifier),
            condition = lambda char: char.owner.lvl==6,
            modifier= Grandmother_Modifier
        )
    ]
)

def Gwen_effect_func(source):
    if len(source.owner.hand) + len(source.owner.spell_hand) < 11:
        source.owner.spell_hand.append(Knighthood)

Gwen = Hero(
    name='Gwen',
    abils = [
        Triggered_Effect(
            name = 'Gwen gain hero effect',
            effect_func = Gwen_effect_func,
            trigger = Trigger(
                name = 'Gwen gain hero trigger',
                type = 'gain hero'
            )
        )
    ]
)

Hoard_Dragon = Hero(name='Hoard Dragon',
    life = 45,
    abils=[
        Treasure_Level_Mod(
            name='Hoard Dragon treasure level effect',
            effect_func= lambda base_lvl: base_lvl + 1
        )
    ]
)

Jacks_Giant_Modifier = Modifier(
    name= "Jack's Giant Modifier",
    hlth_func = lambda char, hlth, source: hlth + 2
)

def Jacks_Giant_remove_effect(char):
    char.remove_modifier(Jacks_Giant_Modifier)

Jacks_Giant = Hero(
    name="Jack's Giant",
    abils=[
        Global_Static_Effect(
            name = 'Mrs Claus effect',
            effect_func = lambda char: char.add_modifier(Jacks_Giant_Modifier),
            reverse_effect_func = Jacks_Giant_remove_effect,
            condition = lambda char: char.position in [1,2,3,4],
            modifier= Jacks_Giant_Modifier
        )
    ]
)

Krampus_Modifier = Modifier(
    name= 'Krampus Modifier',
    atk_func = lambda char, atk, source: atk + 1,
    hlth_func = lambda char, hlth, source: hlth + 1
)

Krampus = Hero(
    name='Krampus',
    abils=[
        Global_Static_Effect(
            name = 'Mrs Claus effect',
            effect_func = lambda char: char.add_modifier(Krampus_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Krampus_Modifier),
            condition = lambda char: char.check_alignment('Evil'),
            modifier= Krampus_Modifier
        )
    ]
)

def Loki_spell_effect(eff, player):
    player.spells_in_shop.append(False)

def Loki_spell_reverse_effect(eff, player):
    player.spells_in_shop.remove(False)

def Loki_random_spell_effect(spell):
    elig_spells = [i for i in spell.owner.game.spells if i.target==None and i.name!="Genie's Wish"
        and i.spell_for_turn]
    elig_target_spells = [
        'Magic Research',
        'Sugar and Spice',
        "Witch's Brew",
        "Luna's Grace",
        'Flourish',
        'Worm Root',
        "Beauty's Influence",
        'Burning Palm',
        'Stoneskin',
        "Merlin's Test",
        "Queen's Grace",
        'Gigantify',
        'Hugeify',
        'Knighthood',
        'Evil Twin'
    ]
    elig_spells = elig_spells + [i for i in spell.owner.game.spells if i.name in elig_target_spells]
    # ensure selected spell has legal targets
    while True:
        selected = random.choice(elig_spells)
        selected.owner = spell.owner
        if selected.target == None:
            break
        else:
            try:
                selected.target.target_select(random_target= True)
            # returns IndexError if no legal target
            except IndexError:
                pass
    selected.cast(spell.owner, random_target=True)

Loki = Hero(
    name='Loki',
    abils = [
        Player_Effect(
            name='Loki Spell Effect',
            effect_func= Loki_spell_effect,
            reverse_effect_func = Loki_spell_reverse_effect
        ),
        Triggered_Effect(
            name='Loki Random Spell Effect',
            effect_func = Loki_random_spell_effect,
            trigger = Trigger(
                name = 'Loki trigger',
                type = 'start of turn'
            )
        )
    ]

)

# Mad catter ability is hard coded into player's roll_shop function
Mad_Catter = Hero(name='Mad Catter')

# TODO: MAsk
Mask = Hero(name='Mask')

def Merlin_cast_effect(source, in_combat):
    if in_combat:
        effect_chars = [i for i in source.owner.board.values() if i!= None]
    else:
        effect_chars = [i for i in source.owner.hand if i!= None]

    if effect_chars != []:
        selected = random.choice(effect_chars)
        selected.change_atk_mod(2)
        selected.change_hlth_mod(1)

Merlin = Hero(
    name='Merlin',
    abils = [
        Triggered_Effect(
            name = 'Merlin cast effect',
            effect_func = Merlin_cast_effect,
            trigger = Trigger(
                name = 'Merlin cast trigger',
                type = 'cast'
            )
        )
    ]
)

Mihri_King_Lion_Modifier = Modifier(
    name= 'Mihri, King Lion Modifier',
    atk_func = lambda char, atk, source: atk + char.owner.trackers['Royals_upgraded'],
    hlth_func = lambda char, hlth, source: hlth + char.owner.trackers['Royals_upgraded'] * 2
)

Mihri_King_Lion = Hero(
    name='Mihri, King Lion',
    abils = [
        Global_Static_Effect(
            name = 'Mihri, King Lion effect',
            effect_func = lambda char: char.remove_modifier(Mihri_King_Lion_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(Mihri_King_Lion_Modifier),
            condition = lambda char: 'Prince' in char.type or 'Princess' in char.type,
            modifier= Mihri_King_Lion_Modifier
        )
    ]
)

def Mordred_effect(source, dead_char):
    spawn_pos = source.owner.find_next_spawn_position(dead_char.position)
    if spawn_pos == None:
        source.abils[0].activated_this_turn == False
    else:
        reserve_chars = [i for i in source.owner.hand if i not in source.owner.deployed_chars]
        if reserve_chars != []:
            highest_atk = max([i.atk() for i in reserve_chars])
            highest_chars = [i for i in reserve_chars if i.atk() == highest_atk]
            highest_chars[0].summon(source.owner, position=dead_char.position)

Mordred = Hero(
    name='Mordred',
    life = 45,
    abils = [
        Triggered_Effect(
            name = 'Mordred effect',
            effect_func = Mordred_effect,
            trigger = Trigger(
                name = 'Mordred trigger',
                type = 'die'
            ),
            once_per_turn = True
        )
    ]
)

def Morgan_le_Fay_20_life_effect(source):
    source.owner.select_treasure(source.owner.lvl)
    source.owner.trackers['Morgan_le_Fay_20_life_used'] = True
    import pdb; pdb.set_trace()

def Morgan_le_Fay_5_life_effect(source):
    source.owner.select_treasure(source.owner.lvl)
    source.owner.trackers['Morgan_le_Fay_5_life_used'] = True

def Morgan_20_life_cond(source, condition_obj):
    result = (condition_obj.source.owner.life <= 20) & \
        (condition_obj.source.owner.trackers['Morgan_le_Fay_20_life_used'] == False)
    return result

Morgan_le_Fay = Hero(
    name='Morgan le Fay',
    abils = [
        Triggered_Effect(
            name = 'Morgan le Fay 20 life effect',
            effect_func = Morgan_le_Fay_20_life_effect,
            trigger = Trigger(
                name = 'Morgan le Fay 20 life trigger',
                type = 'end of turn',
                condition = Morgan_20_life_cond
            )
        ),
        Triggered_Effect(
            name = 'Morgan le Fay 5 life effect',
            effect_func = Morgan_le_Fay_5_life_effect,
            trigger = Trigger(
                name = 'Morgan le Fay 5 life trigger',
                type = 'end of turn',
                condition = lambda source, condition_obj:
                    (condition_obj.source.owner.life <= 5) & \
                    (condition_obj.source.owner.trackers['Morgan_le_Fay_5_life_used'] == False)
            )
        )
    ]
)

Mrs_Claus_Modifier = Modifier(
    name= 'Mrs. Claus Modifier',
    atk_func = lambda char, atk, source: atk + 1,
    hlth_func = lambda char, hlth, source: hlth + 1
)

def Mrs_Claus_effect(char):
    char.add_modifier(Mrs_Claus_Modifier)

Mrs_Claus = Hero(name='Mrs. Claus',
    abils=[
        Global_Static_Effect(
            name = 'Mrs Claus effect',
            effect_func = Mrs_Claus_effect,
            reverse_effect_func = lambda char: char.remove_modifier(Mrs_Claus_Modifier),
            condition = lambda char: char.check_alignment('Good'),
            modifier= Mrs_Claus_Modifier
        )
    ]
)


def Muerte_effect(eff, player):
    player.last_breath_multiplier += 1

def Muerte_reverse_effect(eff, player):
    player.last_breath_multiplier -= 1


Muerte = Hero(name='Muerte',
    life = 45,
    abils = [
        Player_Effect(
            name='Muerte Effect',
            effect_func= Muerte_effect,
            reverse_effect_func = Muerte_reverse_effect
        )
    ]
)

def Pans_Shadow_effect(char):
    char.change_cost(-1)

def Pans_Shadow_reverse_effect(char):
    char.change_cost(1)

def Pans_Shadow_track_evil_effect(source):
    source.owner.Evil_char_purchased_this_turn = True

def Pans_Shadow_reset_tracker_effect(source):
    source.owner.Evil_char_purchased_this_turn = False

Pans_Shadow = Hero(
    name="Pan's Shadow",
    abils = [
        Shop_Effect(
            name = "Pan's Shadow shop effect",
            char_effect_func = Pans_Shadow_effect,
            char_reverse_effect_func = Pans_Shadow_reverse_effect,
            condition = lambda char: char.check_alignment('Evil') and \
                char.owner.Evil_char_purchased_this_turn == False
        ),
        Triggered_Effect(
            name = "Pan's Shadow track evil char",
            effect_func = Pans_Shadow_track_evil_effect,
            trigger = Trigger(
                name = "Pan's Shadow track evil char trigger",
                type = 'purchase',
                condition = lambda self, char: char.check_alignment('Evil')
            )
        ),
        Triggered_Effect(
            name = "Pan's Shadow reset track char",
            effect_func = Pans_Shadow_reset_tracker_effect,
            trigger = Trigger(
                name = "Pan's Shadow reset track trigger",
                type = 'start of turn',
            )
        )
    ]
)


# Peter Pants level up counter hardcoded into player level_up function
def Peter_Pants_effect(char):
     char.change_atk_mod(char.owner.trackers['Peter_Pants_lvl_up_count'])
     char.change_hlth_mod(char.owner.trackers['Peter_Pants_lvl_up_count'])

def Peter_Pants_reverse_effect(char):
    assert char.owner.hero.name == 'Peter Pants'
    char.change_atk_mod(-1 * char.owner.trackers['Peter_Pants_lvl_up_count'])
    char.change_hlth_mod(-1 * char.owner.trackers['Peter_Pants_lvl_up_count'])

def Peter_Pants_gain_hero_effect(source):
    if source.owner.lvl < 3:
        source.owner.lvl = 3
    elif source.owner.lvl > 3:
        lvl_change = source.owner.lvl - 3
        source.owner.trackers['Peter_Pants_lvl_up_count'] = lvl_change
        source.owner.lvl = 3

Peter_Pants = Hero(
    name='Peter Pants',
    abils = [
        Triggered_Effect(
            name = 'Peter Pants gain hero effect',
            effect_func = Peter_Pants_gain_hero_effect,
            trigger = Trigger(
                name = 'Peter Pants gain hero trigger',
                type = 'gain hero'
            )
        ),
        Shop_Effect(
            name='Peter Pants Effect',
            char_effect_func = Peter_Pants_effect,
            char_reverse_effect_func = Peter_Pants_reverse_effect
        )
    ]
)

# pied piper effect hard coded into shop generation
Pied_Piper = Hero(name='Pied Piper')

# extra spell hardcoded into shop generation
def Potion_Master_pump_effect(source, targeted):
    targeted.change_atk_mod(1)
    targeted.change_hlth_mod(1)

Potion_Master = Hero(
    name='Potion Master',
    abils = [
        Triggered_Effect(
            name = 'Potion Master pump effect',
            effect_func = Potion_Master_pump_effect,
            trigger = Trigger(
                name = 'Potion master target trigger',
                type = 'target'
            )
        )
    ]
)

# Beauty alignment altering effect is hardcoded into alignment checks
Beauty = Hero(name='Beauty')

Pup_the_Magic_Dragon = Hero(name='Pup the Magic Dragon')
Sad_Dracula = Hero(name='Sad Dracula')
Sir_Galahad = Hero(name='Sir Galahad')
Skip_the_Time_Skipper = Hero(name='Skip, the Time Skipper')
Snow_Angel = Hero(name='Snow Angel')
The_Cursed_King = Hero(name='The Cursed King')


The_Fates_Modifier = Modifier(
    name= 'The Fates Modifier',
    atk_func = lambda char, atk, source: atk + 5,
    hlth_func = lambda char, hlth, source: hlth + 5
)

The_Fates = Hero(name='The Fates',
    abils=[
        Global_Static_Effect(
            name = 'The Fates effect',
            effect_func = lambda char: char.add_modifier(The_Fates_Modifier),
            reverse_effect_func = lambda char: char.remove_modifier(The_Fates_Modifier),
            condition = lambda char: char.upgraded,
            modifier= The_Fates_Modifier
        )
    ]
)

The_Headless_Horseman = Hero(name='The Headless Horseman')
Trophy_Hunter = Hero(name='Trophy Hunter')
Wonder_Waddle = Hero(name='Wonder Waddle')
Xelhua = Hero(name='Xelhua',
    life = 45
)

objs=deepcopy(list(locals().keys()))
master_hero_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Hero):
        master_hero_list.append(obj)
