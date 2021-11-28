from copy import deepcopy
from copy import copy
from Effects import *
import random
import collections

class Character:
    def __init__(self, name:str, type, atk, hlth, lvl,  abils=[],
        keyword_abils=[], alignment='Neutral', token=False, inshop=True):
        self.name=name
        self.type=type
        self.base_atk=atk
        self.base_hlth=hlth
        self.last_atk = atk
        self.last_hlth = hlth
        self.atk_mod= 0
        self.hlth_mod= 0
        # modifiers that only last til end of battle
        self.eob_atk_mod = 0
        self.eob_hlth_mod = 0

        self.dmg_taken = 0
        self.abils=abils
        if token:
            self.lvl = 1
        else:
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
        # track if character is to transform back into another character at the
        # end of the battle
        self.eob_revert_char = None
        # target that character is attacking
        self.atk_target = None
        # tracking whether character is attacking or not
        self.attacking = False
        # track if they died from an attack
        self.death_from_attacking = False
        # tracker for different effects
        self.trackers = {'Mirror_Mirror_respawn':0, 'Croc_Bait_char':None,
            'Peter_Pants_pump':0}
        self.init_trackers = {'Mirror_Mirror_respawn':0, 'Croc_Bait_char':None,
            'Peter_Pants_pump':0}
        self.slay_multiplier = 1

    def purchase(self, player):
        assert self.owner != None

        # ensure attack/ hlth are at or above default values; shouldn't happen
        # could be indicative of some effect not resolving properly
        assert self.atk() >= self.base_atk
        assert self.hlth() >= self.base_hlth

        if self.game.verbose_lvl>=2:
            print(self.owner, 'purchases', self)
        player.shop.remove(self)


        self.add_to_hand(player)

        self.get_owner().check_for_triggers('purchase', triggering_obj=self)

        # see if there are any effects to apply on purchase
        for eff in player.effects:
            if isinstance(eff, Purchase_Effect) and eff.condition(self):
                eff.apply_effect(eff, self)

        self.get_owner().current_gold -= self.current_cost

        if 'Dwarf' in self.type:
            self.get_owner().dwarves_bought += 1


    def create_copy(self, owner, origin, plain_copy = False, inshop=False):
        '''
        function to create a copy of a character
        params:
        owner - Player object who will own the copy
        origin - a string noting what generated the token
        plain_copy - boolean indicating whether a copy has the buffs of the original
        inshop - boolean indicating whether when sold the copy will return to the
            character pool
        assign_id - whether to assign id to the token. This is only not done
            when making copies preserving what a blocker looks like before attacks.
        game - if owner is None, passing a game object to use for master_char_list
        '''
        master_obj = [i for i in owner.game.master_char_list if i.name==self.name][0]

        from datetime import datetime
        start = datetime.now()
        copy = deepcopy(master_obj)
        end= datetime.now() - start
        if end.microseconds> 100000:
            print('unexpectedly long time to make copy, '+ str(end) +
            ', check for deep copies being made')

        if plain_copy==False:
            copy.atk_mod=self.atk_mod
            copy.eob_atk_mod = self.eob_atk_mod
            copy.hlth_mod=self.hlth_mod
            copy.eob_hlth_mod = self.eob_hlth_mod
            copy.upgraded = False

        copy.trackers = self.trackers
        copy.origin = origin
        copy.inshop=inshop
        copy.owner = owner
        copy.game = owner.game
        owner.game.assign_id(copy)
        copy.game.char_universe.append(copy)
        copy.damage_taken = 0

        return copy

    # TODO: if add to shop, shouldn't count as purchasing
    def add_to_hand(self, player, store_in_shop=False, transforming = False, dead_player = False):
        assert self.id != None
        if player.get_hand_len()>=11 and store_in_shop == False and transforming == False and dead_player == False:
            raise "too many objects in owner's hand"
        # when transforming/copying dead player, it's ok to have one too many objects as one will
        elif player.get_hand_len()>=12 and store_in_shop == False and (transforming or dead_player):
            raise "too many objects in owner's hand"
        # go away after this function is finished
        elif player.get_hand_len()>=11 and store_in_shop and transforming==False:
            if self.game.verbose_lvl>=3:
                print('Note: too many objects in hand, storing', self, 'in next shop')
            self.owner = player
            self.set_zone('shop')
            self.current_cost= 0
            self.scrub_buffs()
            player.next_shop.append(self)

        elif player.get_hand_len()>=12 and store_in_shop and transforming:
            if self.game.verbose_lvl>=3:
                print('Note: too many objects in hand, storing', self, 'in next shop')
            self.owner = player
            self.set_zone('shop')
            self.current_cost= 0
            self.scrub_buffs()
            player.next_shop.append(self)

        else:
            self.owner = player
            self.set_zone(self.get_owner().hand)
            self.get_owner().hand.append(self)
            self.get_owner().to_hand_this_turn.append(self)
            if any([isinstance(i, Quest) for i in self.abils]):
                self.get_owner().quest_chars_gained.append(self.name)
            # add any triggers that are in any of the abilities of the char
            for i in self.abils:
                if hasattr(i, 'trigger'):
                    self.get_owner().triggers.append(i.trigger)

                if isinstance(i, Player_Effect):
                    i.apply_effect(source=i.source)

    def transform(self, trans_char, preserve_mods =True, temporary = False, temp_reversion = False):
        '''
        function to transform one character into another
        params:
        trans_char - the character to be transformed into
        preserve_mods - whether to carry over upgrades and atk/hlth mods from orig char
        temporary - whether this transformation is only until end of battle or not
        temp_reversion - whether this transformation is a function call that's
            reverting a temporary transformation
        '''
        if trans_char.inshop and temp_reversion == False:
            self.game.char_pool.remove(trans_char)

        if trans_char.token:
            trans_char.owner = self.owner
        else:
            trans_char.add_to_hand(self.owner, transforming = True, store_in_shop=True)

        trans_char.game = self.game
        if self.game.verbose_lvl>=3:
            if temporary == False:
                print(self, 'transforms into', trans_char)
            else:
                print(self, 'temporarily transforms into', trans_char)

        if self.position != None:
            position = self.position
            self.remove_from_board()
            trans_char.add_to_board(self.owner, position)

        if preserve_mods:
            if self.upgraded:
                trans_char.upgraded = True
            trans_char.atk_mod = self.atk_mod
            trans_char.hlth_mod = self.hlth_mod
            trans_char.eob_atk_mod = self.eob_atk_mod
            trans_char.eob_hlth_mod = self.eob_hlth_mod

        # transfer over trackers if transforming temporarily
        if temporary or temp_reversion:
            trans_char.trackers = self.trackers.copy()

        if self in self.get_owner().hand:
            if temporary:
                # if this is just a temp tranformation, don't return to the char pool
                self.remove_from_hand(return_to_pool=False)
            else:
                self.remove_from_hand()

        if temporary and (self.token == False):
            # if this char already has a character its transforming back to,
            # transfer that char over
            if self.eob_revert_char !=None:
                trans_char.eob_revert_char = self.eob_revert_char
            else:
                trans_char.eob_revert_char = self

        # if reverting to another character, remove eob_revert_char
        if temp_reversion:
            self.eob_revert_char = None


    def summon(self, plyr, position=None):
        spawn_pos = self.get_owner().find_next_spawn_position(position)
        if spawn_pos != None:
            self.add_to_board(plyr, spawn_pos)
            self.get_owner().check_for_triggers('summon',triggering_obj= self,
                effect_kwargs={'summoned':self})
            if self.get_owner().game.verbose_lvl>=3:
                print(plyr, 'summons', self)


    def add_to_board(self, plyr, position):
        if self.token:
            self.owner = plyr
        self.get_owner().board[position] = self
        self.position = position
        for i in self.abils:
            # if hasattr(i, 'trigger'):
            #     self.get_owner().triggers.append(i.trigger)

            if isinstance(i, Global_Static_Effect):
                self.get_owner().effects.append(i)

            if isinstance(i, Support_Effect):
                if plyr.check_for_treasure('Horn of Olympus') and position in [5,6,7]:
                    support_pos = [1,2,3,4]
                elif position == 5:
                    support_pos = [1,2]
                elif position == 6:
                    support_pos = [2,3]
                elif position == 7:
                    support_pos = [3,4]
                else:
                    support_pos = []
                if support_pos != []:
                    for pos in support_pos:
                        char = plyr.board[pos]
                        if char != None and i.condition(char) and i not in char.effects:
                            i.apply_effect(char)

        self.death_from_attacking = False




    # function to remove a character from the board (but not from a player's control)
    def remove_from_board(self, death=False):

        # note last stats prior to death
        self.last_atk = self.atk()
        self.last_hlth = self.hlth()
        # position may be none if the unit's been removed from the owner's control
        # as part of the death ability (e.g. Polywoggle slaying)
        self.last_position = self.position
        if self.position != None:
            self.get_owner().board[self.position] = None

        # if due to death, apply death effects
        if death and self.position != None:
            if self.owner == None:
                self.last_owner.check_for_triggers('die', triggering_obj=self,
                effect_kwargs={'dead_char':self})
                self.last_owner.opponent.check_for_triggers('opponent die', triggering_obj=self,
                effect_kwargs={'dead_char':self})
            else:
                self.get_owner().check_for_triggers('die', triggering_obj=self,
                effect_kwargs={'dead_char':self})
                self.get_owner().opponent.check_for_triggers('opponent die', triggering_obj=self,
                effect_kwargs={'dead_char':self})

        # remove effects from being on field
        for i in self.abils:
            # remove support effects
            if isinstance(i, Support_Effect):
                def _remove_support_effect(supported):
                    if supported!=None:
                        effect = [j for j in supported.effects if j==i]
                        if effect != []:
                            effect[0].reverse_effect(supported)

                if any([i.name == 'Horn of Olympus' for i in self.get_owner().treasures]):
                    if self.position == 5:
                        _remove_support_effect(self.get_owner().board[1])
                        _remove_support_effect(self.get_owner().board[2])
                        _remove_support_effect(self.get_owner().board[3])
                        _remove_support_effect(self.get_owner().board[4])
                    if self.position == 6:
                        _remove_support_effect(self.get_owner().board[1])
                        _remove_support_effect(self.get_owner().board[2])
                        _remove_support_effect(self.get_owner().board[3])
                        _remove_support_effect(self.get_owner().board[4])
                    if self.position == 7:
                        _remove_support_effect(self.get_owner().board[1])
                        _remove_support_effect(self.get_owner().board[2])
                        _remove_support_effect(self.get_owner().board[3])
                        _remove_support_effect(self.get_owner().board[4])
                else:
                    if self.position == 5:
                        _remove_support_effect(self.get_owner().board[1])
                        _remove_support_effect(self.get_owner().board[2])
                    if self.position == 6:
                        _remove_support_effect(self.get_owner().board[2])
                        _remove_support_effect(self.get_owner().board[3])
                    if self.position == 7:
                        _remove_support_effect(self.get_owner().board[3])
                        _remove_support_effect(self.get_owner().board[4])

            if isinstance(i, Global_Static_Effect):
                self.get_owner().effects.remove(i)
                for char in self.get_owner().board.values():
                    if char!=None and i in char.effects:
                        i.reverse_effect(char)
                        char.effects.remove(i)
                # print(self)
                # print(self.get_owner().board)

            # remove any triggers unit uses
            # if hasattr(i, 'trigger') and i in self.get_owner()triggers:
            #     self.get_owner().triggers.remove(i.trigger)

        self.position = None

        # resolve last breath effects after position has been reset
        for i in self.abils:
            if death and isinstance(i, Last_Breath_Effect):
                for n in range(self.get_owner().last_breath_multiplier):
                    if n == 0 or self.get_owner().last_breath_multiplier_used_this_turn == False:
                        i.apply_effect(self)
                        if n != 0:
                            self.get_owner().last_breath_multiplier_used_this_turn = True

        # remove any support effects from self
        rm_eff = []
        for eff in self.effects:
            if isinstance(eff, Support_Effect):
                eff.reverse_effect(self)
                rm_eff.append(eff)

        for eff in rm_eff:
            self.effects.remove(eff)

        self.damage_taken = 0

    def remove_from_hand(self, return_to_pool=True):
        self.get_owner().hand.remove(self)
        for i in self.abils:
            if hasattr(i, 'trigger'):
                self.get_owner().triggers.remove(i.trigger)
            if isinstance(i, Player_Effect):
                for _ in range(collections.Counter(self.get_owner().effects)[i]):
                    i.reverse_effect(self)
                    self.get_owner().effects.remove(i)

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
        self.set_zone('pool')



    def get_cost(self):
        return self.current_cost

    def sell(self):

        # the transforming prince/princesses can get caught in the options objevt
        # and this will try to sell them after they've transformed, so we check
        # for ownership before proceeding
        if self.owner != None:
            if self.game.verbose_lvl>=2:
                print(self.owner, 'sells', self)
            if self.name == 'Golden Chicken' and self.upgraded==False:
                self.get_owner().current_gold += 2
            elif self.name == 'Golden Chicken' and self.upgraded:
                self.get_owner().current_gold += 4
            else:
                self.get_owner().current_gold += 1

            self.remove_from_hand()



    def select_target(self, player):
        '''
        function to select a target for a character to attack.
        '''
        check_for_front_row_chars = any([player.board[i] != None and
            player.board[i] != self for i in range(1,5)])
        check_for_back_row_chars = any([player.board[i] != None and
            player.board[i] != self for i in range(5,8)])

        if check_for_front_row_chars and self.flying==False:
            targets = [player.board[i] for i in range(1,5) if player.board[i]!= None]

        elif self.flying and check_for_back_row_chars == False:
            targets = [player.board[i] for i in range(1,5) if player.board[i]!= None]

        else:
            targets = [player.board[i] for i in range(5,8) if player.board[i]!= None]

        targets = [i for i in targets]
        if targets != []:
            selected = random.choice(targets)
        else:
            selected = None
        return selected

    def atk(self):
        if self.upgraded:
            atk = self.base_atk * 2 + self.atk_mod + self.eob_atk_mod
        else:
            atk = self.base_atk + self.atk_mod + self.eob_atk_mod
        for i in self.modifiers:
            if i.atk_func!=None:
                atk = i.atk_func(self, atk, source=i.source) # * i.source_abil.multiplier
        return max(atk,0)

    def hlth(self):
        if self.upgraded:
            hlth = self.base_hlth * 2 + self.hlth_mod + self.eob_hlth_mod
        else:
            hlth = self.base_hlth + self.hlth_mod + + self.eob_hlth_mod
        for i in self.modifiers:
            if i.hlth_func!=None:
                hlth = i.hlth_func(self, hlth, source=i.source) # * i.source_abil.multiplier
        return max(hlth, 0)

    def check_alignment(self, alignment):
        if self.alignment_mod == []:
            result = self.alignment
        else:
            result = self.alignment_mod[-1]

        if self.get_owner() != None and self.get_owner().hero.name == 'Beauty' and result in ('Good','Evil') \
            and alignment in ('Good', 'Evil'):
            return True
        else:
            return result == alignment

    def get_alignment(self):
        if self.alignment_mod == []:
            return self.alignment
        else:
            return self.alignment_mod[-1]

    def take_damage(self, amt, source, attacking = False):

        # amt is the amount of damage taken
        # source is the object that's dealing damage
        # attacking parameter is whether the source is attacking or not
        # function returns whether or not the target was slain

        assert amt > 0, '0 or less damage being dealt'

        # hardcoded ability for soltak ancient
        def _soltak_ancient_check(self):
            check_pos_map = {5:[1,2], 6:[2,3],7:[3,4]}
            result = False
            if self.position in check_pos_map.keys():
                for i in check_pos_map[self.position]:
                    if self.get_owner().board[i] != None and self.get_owner().board[i].name =='Soltak Ancient':
                        result = True
            return result

        # verify either attacking or soltak ancient is not in front of the char
        if _soltak_ancient_check(self)==False or self.attacking:
            self.dmg_taken += amt
            if self.game.verbose_lvl>=3:
                print(self, 'takes',amt,'damage.',self.dmg_taken,'taken total.')

            if isinstance(source, Character):
                if source.owner == None:
                    plyr = source.last_owner
                else:
                    plyr = source.owner
                plyr.check_for_triggers('deal damage', triggering_obj = source,
                    effect_kwargs={'damage_dealt':amt, 'damaged_char':self, 'attacking':attacking})

            if self.dmg_taken >= self.hlth():
                if attacking and isinstance(source, Character):
                    self.death_from_attacking = True
                self.dies()
                return True

            # pump effects can sometime make survive damage trigger when it shouldn't
            # so setting a check to ensure it's still on the board
            elif self.position != None:
                self.get_owner().check_for_triggers('survive damage', triggering_obj = self,
                    effect_kwargs={'damaged_char':self})
                return False

            else:
                return True
                # for abil in self.abils:
                #     if isinstance(abil, Triggered_Effect) and abil.trigger.type=='survive damage':
                #         abil.trigger_effect()

    def dies(self):
        # only trigger this stuff if object is still on the board
        if self.position != None:
            if self.owner!= None and self.token == False:
                self.get_owner().chars_dead.append(self)
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
        # elif self.name != 'Polywoggle':
        #     raise
        # can die to mummy



    def make_attack(self, player = None):
        # Harvest_Moon has been removed
        # hardcoded interaction with harvest moon; note it doesn not interact with mimic
        # if any([i.name == 'Harvest Moon' for i in self.get_owner().treasures]) and \
        #     any([i.trigger.type == 'slay' for i in self.abils]):
        #     n = 2
        #
        # else:
        #     n = 1
        # for _ in range(n):
            if self.atk()> 0:
                self.attacking = True
                # player param is a specific player board the char is attacking. Only used by cupid currently
                if player == None:
                    player = self.get_owner().opponent
                # set owner now just for Humpty dying, which causes owner = None
                # prior to check effects statements

                owner = self.get_owner()
                self.atk_target = self.select_target(player)
                if self.atk_target != None:
                    # preserve original attack target mods as it is before attacks, in case
                    # an ability needs to reference it after it dies. Currently this is only
                    # relevant for Southern_Siren's slay ability.
                    orig_attack_target_attribs = {
                        'atk_mod': self.atk_target.atk_mod,
                        'eob_atk_mod': self.atk_target.eob_atk_mod,
                        'hlth_mod': self.atk_target.hlth_mod,
                        'eob_hlth_mod': self.atk_target.eob_hlth_mod,
                        'upgraded': self.atk_target.upgraded
                    }

                    if self.game.verbose_lvl>=2:
                        print(self, 'attacks',self.atk_target)
                    owner.check_for_triggers('attack',triggering_obj= self, effect_kwargs=
                        {'attacker':self})

                    if self.atk_target.owner != None:
                        owner2 = self.atk_target.owner
                    else:
                        owner2 = self.atk_target.last_owner
                    owner2.check_for_triggers('attacked',triggering_obj= self.atk_target, effect_kwargs=
                        {'attacker':self})

                    # take damage function will return boolean indicating whether target was slain
                    slay_result = self.atk_target.take_damage(self.atk(), source = self, attacking = True)

                    if self.ranged==False and self.atk_target.atk()>0:
                        self.take_damage(self.atk_target.atk(), source = self.atk_target)

                    if slay_result:
                        for _ in range(self.slay_multiplier):
                            self.get_owner().check_for_triggers('global slay',
                            triggering_obj = self, triggered_obj = self.atk_target,
                            effect_kwargs = {'slain':self.atk_target, 'slayer':self})


                        for abil in self.abils:
                            if isinstance(abil, Triggered_Effect) and abil.trigger.type=='slay':
                                for _ in range(self.slay_multiplier):

                                    # if it's a trophy hunter abil, need to pass appropriate args
                                    if 'Trophy Hunter Slay' in abil.name:
                                        abil.trigger_effect()
                                    else:
                                        abil.trigger_effect(effect_kwargs={'slain':self.atk_target,
                                            'slain_attribs': orig_attack_target_attribs})


                owner.check_effects()
                owner.opponent.check_effects()
                self.atk_target = None
                self.attacking = False

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

            if isinstance(eff, Support_Effect):
                eff.reverse_effect(self)
                rm_eff.append(eff)

        for mod in rm_mod:
            self.remove_modifier(mod)

        for eff in rm_eff:
            self.effects.remove(eff)

        self.eob_atk_mod = 0
        self.eob_hlth_mod = 0

        # for when we are not just scrubbing end of battle buffs
        if eob_only==False:
            for eff in self.effects:
                eff.reverse_effect(self)
            self.modifiers=[]
            self.effects=[]
            self.alignment_mod=[]
            self.current_cost = self.base_cost
            self.upgraded = False
            self.atk_mod = 0
            self.hlth_mod = 0
            self.trackers = self.init_trackers.copy()

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
        if self.name =='Dubly' and amt > 0:
            amt = amt * (2 + self.upgraded)
        # make sure atk mod not lowered below 0
        self.atk_mod += amt
        if self.name != 'Echowood':
            self.get_owner().check_for_triggers('change_mod', effect_kwargs = {'amt':amt, 'type':'atk'})
        if self.atk_mod < 0:
            print('Warning: atk_mod is negative')
            self.atk_mod = 0

    def change_hlth_mod(self, amt):
        if self.name =='Dubly' and amt > 0:
            amt = amt * (2 + self.upgraded)

        self.hlth_mod += amt

        # adjust dmg taken so health reduction effects are wiping damage .
        if self.dmg_taken > 0 and amt < 0:
            self.dmg_taken += amt
        self.dmg_taken = max(0, self.dmg_taken)

        if self.name != 'Echowood':
            self.get_owner().check_for_triggers('change_mod', effect_kwargs = {'amt':amt, 'type':'hlth'})

        # assert self.hlth_mod >= 0
        if self.hlth_mod < 0:
            print('Warning: hlth_mod is negative')
            self.hlth_mod = 0

    def change_eob_atk_mod(self, amt):
        if self.name =='Dubly' and amt > 0:
            amt = amt * (2 + self.upgraded)
        self.eob_atk_mod += amt
        if self.name != 'Echowood':
            self.get_owner().check_for_triggers('change_mod', effect_kwargs = {'amt':amt, 'type':'atk'})

    def change_eob_hlth_mod(self, amt):
        if self.name =='Dubly' and amt > 0:
             amt = amt * (2 + self.upgraded)
        self.eob_hlth_mod += amt

        # adjust dmg taken so health reduction effects are wiping damage .
        if self.dmg_taken > 0 and amt < 0:
            self.dmg_taken += amt
        self.dmg_taken = max(0, self.dmg_taken)

        if self.name != 'Echowood':
            self.get_owner().check_for_triggers('change_mod', effect_kwargs = {'amt':amt, 'type':'hlth'})

    def set_zone(self, zone):
        self.zone = zone

    def change_cost(self, amt):
        self.current_cost = max(0, self.current_cost + amt)

    def reset_cost(self):
        self.current_cost = self.base_cost

    def get_owner(self):
        if self.owner != None:
            return self.owner
        else:
            return self.last_owner

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
