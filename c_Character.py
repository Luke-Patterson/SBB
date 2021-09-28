from copy import deepcopy
from copy import copy
from Effects import *
import random

class Character:
    def __init__(self, name:str, type, atk, hlth, lvl,  abils=[],
        keyword_abils=[], alignment='Neutral', token=False, inshop=True):
        self.name=name
        self.type=type
        self.base_atk=atk
        self.base_hlth=hlth
        self.atk_mod= 0
        self.hlth_mod= 0
        self.dmg_taken = 0
        self.abils=abils
        self.lvl=lvl
        self.alignment=alignment
        self.alignment_mod = []
        self.base_cost = lvl
        self.current_cost= lvl
        self.owner = None
        self.position = None
        self.zone = None
        self.id= None
        self.game = None
        self.keyword_abils = keyword_abils
        if 'flying' in keyword_abils:
            self.flying=True
        else:
            self.flying=False
        if 'ranged' in keyword_abils:
            self.ranged = True
        else:
            self.ranged = False
        self.upgraded = False
        self.upgrade_copies=[]
        self.eob_reverse_effects=[]
        self.token = token
        self.modifiers = []
        self.effects= []
        for i in self.abils:
            i.add_to_obj(self)
        self.inshop=inshop

    def purchase(self, player):
        if self.game.verbose_lvl>=2:
            print(self.owner, 'purchases', self)
        player.shop.remove(self)

        # see if there are any effects to apply on purchase
        for eff in player.effects:
            if isinstance(eff, Purchase_Effect) and eff.condition(self):
                eff.apply_effect(eff, self)

        self.add_to_hand(player)
        self.owner.current_gold -= self.current_cost

    def create_token(self, owner):
        token = deepcopy(self)
        token.owner = owner
        token.game = owner.game
        return token

    def add_to_hand(self, player):
        self.owner = player
        self.zone = self.owner.hand
        self.owner.hand.append(self)
        # add any triggers that are in any of the abilities of the char
        for i in self.abils:
            if hasattr(i, 'trigger'):
                self.owner.triggers.append(i.trigger)

            if isinstance(i, Player_Effect):
                i.apply_effect(source=i.source)


    def permanent_transform(self, trans_char):
        trans_char.add_to_hand(self.owner)
        trans_char.game = self.game
        if self.game.verbose_lvl>=3:
            print(self, 'transforms into', trans_char)

        if self.position != None:
            position = self.position
            self.remove_from_board()
            trans_char.add_to_board(self.owner, position)

        if self.upgraded:
            trans_char.upgraded = True
        trans_char.atk_mod = self.atk_mod
        trans_char.hlth_mod = self.hlth_mod

        self.remove_from_hand()

    def add_to_board(self, plyr, position):
        if self.token:
            self.owner = plyr
        self.owner.board[position] = self
        self.position = position
        if self.name=='Frog Prince':
            print('Position',self.position)
        for i in self.abils:
            if hasattr(i, 'trigger') and i.trigger.battle_trigger:
                self.owner.battle_triggers.append(i.trigger)

            if isinstance(i, Player_Effect):
                self.owner.effects.append(i)


    def remove_from_hand(self):
        self.owner.hand.remove(self)
        for i in self.abils:
            if hasattr(i, 'trigger'):
                self.owner.triggers.remove(i.trigger)
            if isinstance(i, Player_Effect):
                i.reverse_effect(i.source)
                self.owner.effects.remove(i)

        if self.inshop:
            self.game.char_pool.append(self)
            if self.upgraded:
                for i in self.upgrade_copies:
                    self.game.char_pool.append(i)
                self.upgrade_copies = []
        self.scrub_buffs(eob_only=False)
        self.owner = None
        self.zone = 'pool'

    def get_cost(self):
        return self.current_cost

    def sell(self):
        if self.game.verbose_lvl>=2:
            print(self.owner, 'sells', self)
        if self.name == 'Golden Chicken' and self.upgraded==False:
            self.owner.current_gold += 2
        elif self.name == 'Golden Chicken' and self.upgraded:
            self.owner.current_gold += 4
        else:
            self.owner.current_gold += 1
        self.remove_from_hand()


    def select_target(self):
        if any([self.owner.opponent.board[i] for i in range(1,5)]) and self.flying==False:
            targets = [self.owner.opponent.board[i] for i in range(1,5) if self.owner.opponent.board[i]!= None]
        elif self.flying and any([self.owner.opponent.board[i] for i in range(5,8)])==False:
            targets = [self.owner.opponent.board[i] for i in range(1,5) if self.owner.opponent.board[i]!= None]
        else:
            targets = [self.owner.opponent.board[i] for i in range(5,8) if self.owner.opponent.board[i]!= None]

        selected = random.choice(targets)
        return selected

    def atk(self):
        if self.upgraded:
            atk = self.base_atk * 2 + self.atk_mod
        else:
            atk = self.base_atk + self.atk_mod
        for i in self.modifiers:
            if i.atk_func!=None:
                atk = i.atk_func(self, atk, source=i.source)
        return atk

    def hlth(self):
        if self.upgraded:
            hlth = self.base_hlth * 2 + self.hlth_mod
        else:
            hlth = self.base_hlth + self.hlth_mod
        for i in self.modifiers:
            if i.hlth_func!=None:
                hlth = i.hlth_func(self, hlth, source=i.source)
        return hlth

    def get_alignment(self):
        if self.alignment_mod == []:
            return self.alignment
        else:
            return self.alignment_mod[-1]

    def take_damage(self, amt, source, attacking = False):
        self.dmg_taken += amt
        if self.game.verbose_lvl>=3:
            print(self, 'takes',amt,'damage.',self.dmg_taken,'taken total.')
        if self.dmg_taken >= self.hlth():
            self.dies()
            if attacking== True and isinstance(source, Character):
                for abil in source.abils:
                    if isinstance(abil, Triggered_Effect) and abil.trigger.type=='slay':
                        abil.trigger_effect()


    def dies(self):
        assert self.owner.board[self.position]==self

        self.remove_from_board(death=True)

        if self.game.verbose_lvl>=2:
            print(self, 'dies')

    # function to remove a character from the board (but not from a player's control)
    def remove_from_board(self, death=False):
        self.owner.board[self.position] = None

        # remove effects from being on field
        for i in self.abils:
            # remove support effects
            if isinstance(i, Support_Effect):
                def _remove_support_effect(supported):
                    if supported!=None:
                        effect = [j for j in supported.eob_reverse_effects if j==i]
                        if effect != []:
                            effect[0].reverse_effect(supported)
                            supported.eob_reverse_effects.remove(effect[0])

                if self.position == 5:
                    _remove_support_effect(self.owner.board[1])
                    _remove_support_effect(self.owner.board[2])
                if self.position == 6:
                    _remove_support_effect(self.owner.board[2])
                    _remove_support_effect(self.owner.board[3])
                if self.position == 7:
                    _remove_support_effect(self.owner.board[3])
                    _remove_support_effect(self.owner.board[4])

            # if due to death, apply death effects
            if death:
                if isinstance(i, Death_Effect):
                    i.apply_effect(self)

            # remove any triggers unit uses
            if hasattr(i, 'trigger') and i.trigger.battle_trigger:
                self.owner.battle_triggers.remove(i.trigger)

        self.position = None
        self.damage_taken = 0


    def make_attack(self):
        if self.atk()> 0:
            # set owner now just for Humpty dying, which causes owner = None
            # prior to check effects statements
            owner = self.owner
            target = self.select_target()
            if self.game.verbose_lvl>=2:
                print(self, 'attacks',target)
            target.take_damage(self.atk(), source = self, attacking = True)
            if self.ranged==False and target.atk()>0:
                self.take_damage(target.atk(), source = target)
            owner.check_effects()
            owner.opponent.check_effects()

    def scrub_buffs(self, eob_only = True):

        for i in self.eob_reverse_effects:
            i.reverse_effect(self)
        self.eob_reverse_effects = []

        rm_mod = []
        for mod in self.modifiers:
            if mod.eob:
                rm_mod.append(mod)
        for mod in rm_mod:
            self.modifiers.remove(mod)

        # for when we are not just scrubbing end of battle buffs
        if eob_only==False:
            self.atk_mod = 0
            self.hlth_mod = 0
            for eff in self.effects:
                eff.reverse_effect(self)
            self.modifiers=[]
            self.effects=[]
            self.current_cost = self.base_cost
            self.upgraded = False

    def add_modifier(self, modifier):
        modifier.source = self
        self.modifiers.append(modifier)
        if modifier.oth_func!=None:
            modifier.oth_func(self)

    def remove_modifier(self, modifier):
        modifier.source = None
        self.modifiers.remove(modifier)
        if modifier.oth_reverse_func!=None:
            modifier.oth_reverse_func(self)

    def increase_atk_mod(self, amt):
        self.atk_mod += amt

    def increase_hlth_mod(self, amt):
        self.hlth_mod += amt

    def __repr__(self):
        printed = self.name
        if self.id != None and self.game.verbose_lvl>=4:
            printed = self.name + '_#' + str(self.id)
        if self.owner!=None and self.game.verbose_lvl>=3:
            printed = printed + ' (' + str(self.atk()) + '/' + str(self.hlth()) + ')'
        elif self.owner==None and self.game.verbose_lvl>=3:
            printed = printed + ' (' + str(self.base_atk) + '/' + str(self.base_hlth) + ')'
        if self.upgraded:
            printed = printed + ' (gold)'
        return printed
