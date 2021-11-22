from copy import deepcopy
from Effects import *

class Spell:

    def __init__(self, name:str, lvl, cost, effect, target = None, spell_for_turn=True,
        battle_effect=None, ignore_multiplier = False):
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
        self.effects = []
        # boolean for whether multi-casting a spell does anything
        self.ignore_multiplier = ignore_multiplier


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

    def cast(self, owner, in_combat=False, random_target = False):
        '''
        function to cast a spell
        params:
        owner - owner of spell
        in_combat - whether spell is being cast in combat or not
        random_target - whether to choose a target randomly
        '''
        self.owner = owner
        if self.target != None:
            self.target.target_select(random_target=random_target)
            if self.owner.game.verbose_lvl>=3:
                print(self.owner,'casts',self,'targeting',self.selected_target)
        elif self.owner.game.verbose_lvl>=3:
            print(self.owner,'casts',self)

        multiplier = 1
        for abil in self.owner.effects:
            if isinstance(abil, Spell_Multiplier):
                multiplier = abil.apply_effect(spell = self, multiplier=multiplier)

        # hardcoded Black Prism effect for targeted spells affected by multipliers
        if self.target != None and self.owner.check_for_treasure('Black Prism')  \
            and self.ignore_multiplier==False:
            for char in self.owner.hand:
                self.selected_target = char
                if multiplier != 1 and self.owner.game.verbose_lvl>=3:
                    print(self,'duplicated', multiplier, 'times')
                for n in range(multiplier):
                    self.owner.check_for_triggers('cast', cond_kwargs= {'in_combat':in_combat},
                        effect_kwargs= {'in_combat':in_combat})

                    # only has effect if first time or multiplier is not ignored
                    if n == 0 or self.ignore_multiplier==False:
                        if in_combat and self.battle_effect != None:
                            self.battle_effect(self)
                        else:
                            self.effect(self)
                    self.owner.spells_cast_this_game += 1

        else:
            if multiplier != 1 and self.owner.game.verbose_lvl>=3:
                print(self,'duplicated', multiplier, 'times')
            for n in range(multiplier):
                self.owner.check_for_triggers('cast', cond_kwargs= {'in_combat':in_combat},
                    effect_kwargs= {'in_combat':in_combat})

                # only has effect if first time or multiplier is not ignored
                if n == 0 or self.ignore_multiplier==False:
                    if in_combat and self.battle_effect != None:
                        self.battle_effect(self)
                    else:
                        self.effect(self)
                self.owner.spells_cast_this_game += 1

        # clean up
        self.selected_target=None
        self.owner = None

    def scrub_buffs(self, eob_only = True):
        self.current_cost = self.base_cost

    def get_cost(self):
        return self.current_cost

    def change_cost(self, amt):
        self.current_cost = max(0, self.current_cost + amt)

    def reset_cost(self):
        self.current_cost = self.base_cost


    def __repr__(self):
        return self.name
