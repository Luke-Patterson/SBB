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
        # modifiers that only last til end of battle
        self.eob_atk_mod = 0
        self.eob_hlth_mod = 0

        self.dmg_taken = 0
        self.abils=abils
        self.lvl=lvl
        self.alignment=alignment
        self.alignment_mod = []
        self.base_cost = lvl
        self.current_cost= lvl
        self.owner = None
        self.last_owner = None
        self.position = None
        self.zone = None
        self.id= None
        self.game = None
        self.keyword_abils = keyword_abils
        if 'flying' in keyword_abils or 'Flying' in keyword_abils:
            self.flying=True
        else:
            self.flying=False
        if 'ranged' in keyword_abils or 'Ranged' in keyword_abils:
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
        if token:
            self.inshop = False
        else:
            self.inshop=inshop
        # attribute to track origin of character object
        self.origin = 'original'

    def purchase(self, player):
        assert self.owner != None
        if self.game.verbose_lvl>=2:
            print(self.owner, 'purchases', self)
        player.shop.remove(self)
        # see if there are any effects to apply on purchase
        for eff in player.effects:
            if isinstance(eff, Purchase_Effect) and eff.condition(self):
                eff.apply_effect(eff, self)

        self.owner.check_for_triggers('purchase', triggering_obj=self)

        self.add_to_hand(player)

        self.owner.current_gold -= self.current_cost

    def create_copy(self, owner, origin, plain_copy = False, inshop=False):
        '''
        function to create a copy of a character
        params:
        owner - Player object who will own the copy
        origin - a string noting what generated the token
        plain_copy - boolean indicating whether a copy has the buffs of the original
        inshop - boolean indicating whether when sold the copy will return to the
            character pool
        '''

        if self.token:
            copy = deepcopy(self)
        else:
            master_obj = [i for i in owner.game.master_char_list if i.name==self.name][0]
            copy = deepcopy(master_obj)
            if plain_copy==False:
                copy.atk_mod=self.atk_mod
                copy.eob_atk_mod = self.eob_atk_mod
                copy.hlth_mod=self.hlth_mod
                copy.eob_hlth_mod = self.eob_hlth_mod
                copy.upgraded = False

        copy.owner = owner
        copy.origin = origin
        copy.game = owner.game
        owner.game.assign_id(copy)
        copy.game.char_universe.append(copy)
        copy.inshop=inshop

        return copy

    def add_to_hand(self, player, store_in_shop=False, transforming = False):
        assert self.id != None
        if len(player.hand)>=11 and store_in_shop == False and transforming == False:
            raise "too many objects in owner's hand"
        # when transforming, it's ok to have one too many objects as one will
        elif len(player.hand)>=12 and store_in_shop == False and transforming:
            raise "too many objects in owner's hand"
        # go away after this function is finished
        elif len(player.hand)>=11 and store_in_shop and transforming==False:
            self.owner = player
            self.zone = 'shop'
            self.current_cost= 0
            player.next_shop.append(self)

        elif len(player.hand)>=12 and store_in_shop and transforming:
                self.owner = player
                self.zone = 'shop'
                self.current_cost= 0
                player.next_shop.append(self)

        else:
            self.owner = player
            self.zone = self.owner.hand
            self.owner.hand.append(self)
            self.owner.to_hand_this_turn.append(self)
            # add any triggers that are in any of the abilities of the char
            for i in self.abils:
                if hasattr(i, 'trigger'):
                    self.owner.triggers.append(i.trigger)

                if isinstance(i, Player_Effect):
                    i.apply_effect(source=i.source)

    def permanent_transform(self, trans_char):
        if trans_char.inshop:
            self.game.char_pool.remove(trans_char)
        trans_char.add_to_hand(self.owner, transforming = True, store_in_shop=True)
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
        trans_char.eob_atk_mod = self.eob_atk_mod
        trans_char.eob_hlth_mod = self.eob_hlth_mod

        if self.token == False:
            self.remove_from_hand()

    def add_to_board(self, plyr, position):
        if self.token:
            self.owner = plyr
        self.owner.board[position] = self
        self.position = position
        for i in self.abils:
            if hasattr(i, 'trigger') and i.trigger.battle_trigger:
                self.owner.battle_triggers.append(i.trigger)

            if isinstance(i, Global_Static_Effect):
                self.owner.effects.append(i)

    # function to remove a character from the board (but not from a player's control)
    def remove_from_board(self, death=False):

        # position may be none if the unit's been removed from the owner's control
        # as part of the death ability (e.g. Polywoggle slaying)
        self.last_position = self.position
        if self.position != None:
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
            if death and self.position != None:
                if isinstance(i, Last_Breath_Effect):
                    i.apply_effect(self)
                if self.owner == None:
                    self.last_owner.check_for_triggers('die', triggering_obj=self,
                    effect_kwargs={'dead_char':self})
                else:
                    self.owner.check_for_triggers('die', triggering_obj=self,
                    effect_kwargs={'dead_char':self})

            if isinstance(i, Global_Static_Effect):
                self.owner.effects.remove(i)
                for char in self.owner.board.values():
                    if char!=None and i in char.effects:
                        i.reverse_effect(char)
                        char.effects.remove(i)
                # print(self)
                # print(self.owner.board)

            # remove any triggers unit uses
            if self.owner != None:
                if hasattr(i, 'trigger') and i.trigger.battle_trigger:
                    self.owner.battle_triggers.remove(i.trigger)
            # some units (e.g. after Polywoggle slays) will not have an owner
            # at this point in the process. We'll use their last owner for that
            else:
                if hasattr(i, 'trigger') and i.trigger.battle_trigger and i.trigger \
                    in self.last_owner.battle_triggers:
                    self.last_owner.battle_triggers.remove(i.trigger)

        self.position = None
        self.damage_taken = 0

    def remove_from_hand(self, return_to_pool=True):
        self.owner.hand.remove(self)
        for i in self.abils:
            if hasattr(i, 'trigger'):
                self.owner.triggers.remove(i.trigger)
            if isinstance(i, Player_Effect):
                i.reverse_effect(i.source)

            # reset counter of any quests to the quest start val
            if isinstance(i, Quest):
                i.counter = i.counter_start_val

        if self.inshop and return_to_pool:
            self.game.add_to_char_pool(self)
            if self.upgraded:
                for i in self.upgrade_copies:
                    self.game.add_to_char_pool(i)
                self.upgrade_copies = []
        self.scrub_buffs(eob_only=False)
        self.last_owner = self.owner
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
            atk = self.base_atk * 2 + self.atk_mod + self.eob_atk_mod
        else:
            atk = self.base_atk + self.atk_mod + self.eob_atk_mod
        for i in self.modifiers:
            if i.atk_func!=None:
                atk = i.atk_func(self, atk, source=i.source)
        return atk

    def hlth(self):
        if self.upgraded:
            hlth = self.base_hlth * 2 + self.hlth_mod + self.eob_hlth_mod
        else:
            hlth = self.base_hlth + self.hlth_mod + + self.eob_hlth_mod
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

        # amt is the amount of damage taken
        # source is the object that's dealing damage
        # attacking parameter is whether the source is attacking or not

        assert amt > 0, '0 or less damage being dealt'
        self.dmg_taken += amt
        if self.game.verbose_lvl>=3:
            print(self, 'takes',amt,'damage.',self.dmg_taken,'taken total.')
        if self.dmg_taken >= self.hlth():
            self.dies()
            if attacking== True and isinstance(source, Character):
                source.owner.check_for_triggers('global slay',
                    triggering_obj = source, triggered_obj = self,
                    effect_kwargs = {'slain':self, 'slayer':source})

                for abil in source.abils:
                    if isinstance(abil, Triggered_Effect) and abil.trigger.type=='slay':
                        abil.trigger_effect()

        else:
            self.owner.check_for_triggers('survive damage', triggering_obj = self)
            # for abil in self.abils:
            #     if isinstance(abil, Triggered_Effect) and abil.trigger.type=='survive damage':
            #         abil.trigger_effect()

    def dies(self):
        # only trigger this stuff if object is still on the board
        if self.position != None:
            if self.owner!= None and self.token == False:
                self.owner.chars_dead.append(self)
            elif self.owner== None and self.token == False:
                self.last_owner.chars_dead.append(self)

            if self.game.verbose_lvl>=2:
                print(self, 'dies')

            self.remove_from_board(death=True)

            if self.owner == None:
                owner = self.last_owner
            else:
                owner = self.owner
            if all([i==None for i in list(owner.board.values())[0:4]]):
                owner.check_for_triggers('clear front row')
        # I think this is only the case for when polywoggle is slaying while
        # also dying simulatenously
        # raise an exception if this is not the case so we can check it out
        elif self.name != 'Polywoggle':
            raise




    def make_attack(self):
        if self.atk()> 0:
            # set owner now just for Humpty dying, which causes owner = None
            # prior to check effects statements
            owner = self.owner
            target = self.select_target()
            if self.game.verbose_lvl>=2:
                print(self, 'attacks',target)
            owner.check_for_triggers('attack',triggering_obj= self)
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

        rm_eff = []
        for eff in self.effects:
            if hasattr(eff, 'eob') and eff.eob:
                rm_eff.append(eff)

        for mod in rm_mod:
            self.remove_modifier(mod)

        for eff in rm_eff:
            self.effects.remove(eff)

        self.eob_atk_mod = 0
        self.eob_hlth_mod = 0

        # for when we are not just scrubbing end of battle buffs
        if eob_only==False:
            self.atk_mod = 0
            self.hlth_mod = 0
            for eff in self.effects:
                eff.reverse_effect(self)
            self.modifiers=[]
            self.effects=[]
            self.alignment_mod=[]
            self.current_cost = self.base_cost
            self.upgraded = False

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)
        if modifier.oth_func!=None:
            modifier.oth_func(self)

    def add_effect(self, eff):
        eff.source = self
        self.effects.append(eff)

    def remove_modifier(self, modifier):
        if modifier in self.modifiers:
            self.modifiers.remove(modifier)
            if modifier.oth_reverse_func!=None:
                modifier.oth_reverse_func(self)
        elif self.game.verbose_lvl>=4:
            print('Warning: attempted to remove', modifier, 'but its not in', self,'modifiers')

    def change_atk_mod(self, amt):
        self.atk_mod += amt

    def change_hlth_mod(self, amt):
        self.hlth_mod += amt

    def change_eob_atk_mod(self, amt):
        self.eob_atk_mod += amt

    def change_eob_hlth_mod(self, amt):
        self.eob_hlth_mod += amt

    def __repr__(self):
        printed = self.name
        if self.id != None and (self.game==None or self.game.verbose_lvl>=4):
            printed = self.name + '_#' + str(self.id)
        if self.owner!=None and (self.game==None or self.game.verbose_lvl>=3):
            printed = printed + ' (' + str(self.atk()) + '/' + str(self.hlth()) + ')'
        elif self.owner==None and (self.game==None or self.game.verbose_lvl>=3):
            printed = printed + ' (' + str(self.base_atk) + '/' + str(self.base_hlth) + ')'
        if self.upgraded:
            printed = printed + ' [gold]'
        return printed
