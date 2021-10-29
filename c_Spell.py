from copy import deepcopy
from Effects import *

class Spell:

    def __init__(self, name:str, lvl, cost, effect, target = None, spell_for_turn=True,
        battle_effect=None):
        self.name=name
        self.lvl=lvl
        self.base_cost=cost
        self.current_cost=cost
        self.effect=effect
        # when a spell has a different effect when cast in battle, it's stored here
        self.battle_effect = battle_effect
        self.target= target
        if target != None:
            self.target.source = self
        self.selected_target = None
        # boolean for whether this spell allows for another spell to be played this turn
        self.spell_for_turn = spell_for_turn
        self.owner = None


    def purchase(self,player):
        player.current_gold -= self.current_cost
        if player.game.verbose_lvl>=2 and self.selected_target == None:
            print(player, 'purchases', self)
        if player.game.verbose_lvl>=2 and self.selected_target != None:
            print(player, 'purchases', self, 'targetting', self.selected_target)
        if self.spell_for_turn:
            player.spell_played_this_turn=True
        player.shop.remove(self)
        self.cast(player)

    def cast(self, owner, in_combat=False):
        '''
        function to cast a spell
        params:
        owner - owner of spell
        in_combat - whether spell is being cast in combat or not
        '''
        self.owner = owner

        if self.target != None:
            self.target.target_select()
            if self.owner.game.verbose_lvl>=3:
                print(self.owner,'casts',self,'targeting',self.selected_target)
        elif self.owner.game.verbose_lvl>=3:
            print(self.owner,'casts',self)

        self.owner.check_for_triggers('cast')

        if in_combat and self.battle_effect != None:
            self.battle_effect(self)
        else:
            self.effect(self)

        # clean up
        self.owner.spells_cast_this_game += 1
        self.selected_target=None
        self.owner = None

    def scrub_buffs(self, eob_only = True):
        self.current_cost = self.base_cost

    def get_cost(self):
        return self.current_cost

    def __repr__(self):
        return self.name
