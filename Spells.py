from c_Spell import Spell
from Effects import Target
from copy import deepcopy

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

def Witchs_Brew_effect(spell):
    spell.selected_target.atk_mod += 1
    spell.selected_target.hlth_mod += 1

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

objs=deepcopy(list(locals().keys()))
master_spell_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Spell):
        master_spell_list.append(obj)
