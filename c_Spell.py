from copy import deepcopy
from Effects import *

class Spell:

    def __init__(self, name:str, lvl, cost, effect, target = None, spell_for_turn=True):
        self.name=name
        self.lvl=lvl
        self.base_cost=cost
        self.current_cost=cost
        self.effect=effect
        self.target= target
        if target != None:
            self.target.source = self
        self.selected_target = None
        # boolean for whether this spell allows for another spell to be played this turn
        self.spell_for_turn = spell_for_turn
        self.owner = None

    def purchase(self,player):
        player.current_gold -= self.current_cost
        if player.game.verbose_lvl>=2:
            print(player, 'purchases', self)
        if self.spell_for_turn:
            player.spell_played_this_turn=True
        player.shop.remove(self)
        self.cast(player)

    def cast(self, owner):
        self.owner = owner

        if self.target != None:
            self.target.target_select()
            if self.owner.game.verbose_lvl>=3:
                print(self.owner,'casts',self,'targeting',self.selected_target)
        elif self.owner.game.verbose_lvl>=3:
            print(self.owner,'casts',self)

        self.owner.check_for_triggers('cast')

        self.effect(self)

        # clean up
        self.selected_target=None
        self.owner = None

    def scrub_buffs(self, eob_only = True):
        self.current_cost = self.base_cost

    def get_cost(self):
        return self.current_cost

    def __repr__(self):
        return self.name
