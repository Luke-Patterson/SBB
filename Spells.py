from copy import deepcopy

class Spell:

    def __init__(self, name, lvl, cost, effects, spell_for_turn=True):
        self.name=name
        self.lvl=lvl
        self.base_cost=cost
        self.current_cost=cost
        self.effects=effects
        # boolean for whether this spell allows for another spell to be played this turn
        self.spell_for_turn = spell_for_turn

    def purchase(self,player):
        player.current_gold -= self.current_cost
        if player.game.verbose_lvl>=2:
            print(player, 'purchases', self)
        if self.spell_for_turn:
            player.spell_played_this_turn=True
        player.shop.remove(self)

    def get_cost(self):
        return self.current_cost

    def __repr__(self):
        return self.name

Free_Roll = Spell(
    name='Free Roll',
    lvl=2,
    cost=0,
    effects='placeholder'
)

Forbidden_Fruit = Spell(
    name='Forbidden Fruit',
    lvl=2,
    cost=0,
    effects='placeholder'
)

objs=deepcopy(list(locals().keys()))
master_spell_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Spell):
        master_spell_list.append(obj)
