from Effects import *
from Heroes import *
from Treasures import *
from c_Treasure import Treasure
import itertools
import copy
import random
from Spells import *
from Characters import *
import pandas as pd
import math
from datetime import datetime
import collections

class Player:
    def __init__(self, name:str, logic=None, random_logic = True):
        self.name=name
        self.player_id = None
        self.game = None
        # 1-4 is the front row from left to right, 5-7 is the back row
        self.board={1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None}
        # tracker for board at start of combat
        self.starting_board={1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None}
        self.hand=[]
        self.spell_hand=[]
        # track what chars went into hand this turn
        self.to_hand_this_turn=[]
        self.purchased_this_turn=[]
        # list to hold  units used for an upgrade separate
        self.upgrade_limbo=[]
        self.shop=[]
        self.locked_shop = False
        self.life=40
        self.lvl =2
        self.xp=0
        self.start_turn_gold=2
        self.total_gold_this_turn = 0
        self.current_gold=0
        self.next_turn_addl_gold=0
        self.treasures=[]
        # list of all treasures obtained during a game (can't be obtained again)
        self.obtained_treasures = []
        self.logic=logic
        self.random_logic = random_logic
        self.spell_played_this_turn = False
        self.names_of_spells_this_turn = []
        self.spell_purchased_this_turn = False

        self.opponent = None
        self.last_opponent = None
        self.dead = False
        # final position finished in the game
        self.game_position = None
        self.effects=[]
        self.triggers=[]
        # effects specific to a battle
        self.battle_effects=[]
        # track the dead chars
        self.chars_dead = []
        # track what is going into the next shop
        self.next_shop = []
        # track whether to spawn spells in the shop
        self.spells_in_shop = [True]
        # track last combat results
        self.last_combat = 'draw'
        # tracking spells cast this game for storm king
        self.spells_cast_this_game = 0
        # multiplier for last breath effects:
        self.last_breath_multiplier = 1
        self.last_breath_multiplier_used_this_turn = False
        # multiplier for support effects
        self.support_effects_multiplier = 1
        # list of quest char names that the player has gained this game
        self.quest_chars_gained = []
        # list of heros that player has gained this game
        self.heroes_gained = []
        # number of dwarves a player has bought this Game
        self.dwarves_bought = 0
        # keep track of last opponents played. players at the front are next in order to be played
        self.opponent_history = []
        # track what chars were deployed this turn
        self.deployed_chars = []

        # tracker for different effects
        self.trackers = {'Animals_dead_this_combat':0, 'Apocalypse_abil_used':False,
            'Fallen_Angel_atk_chk': False, 'Fallen_Angel_hlth_chk': False,
            'Royals_upgraded':0, 'Evil_char_purchased_this_turn':False,
            'Peter_Pants_lvl_up_count':0, 'Morgan_le_Fay_20_life_used':False,
            'Morgan_le_Fay_5_life_used':False,'Snow_Angel_good_chars_bought':0,
            'Mask_effect_used':False}

    def choose_hero(self, choices):

        hero = self.input_choose(choices, label='hero selection')

        # code for testing certain heros
        force_hero = "Pied Piper"
        if any([i.name ==force_hero for i in choices]):
            hero = [i for i in choices if i.name ==force_hero][0]

        self.add_hero(hero)

        self.game.available_heroes.remove(hero)

    def add_hero(self, hero):
        self.hero = hero
        self.hero.owner = self
        self.hero.apply_effects()
        self.heroes_gained.append(hero)
        self.check_for_triggers('gain hero')

    def remove_hero(self):
        self.hero.remove_effects()
        self.game.available_heroes.append(self.hero)
        self.hero.owner = None
        self.hero = None

    #================= turn order functions==============

    def start_of_turn_effects(self):
        # reset shop
        if self.locked_shop==False:
            self.roll_shop(free=True, beginning_of_turn = True)
        else:
            self.roll_partial_shop()

        self.check_for_triggers('start of turn')
        self.check_quest_completion()
        upgrade_chars = self.check_for_upgrades()
        self.process_upgrades(upgrade_chars[0], upgrade_chars[1])

        # reset gold
        if any([i.name=='Piggie Bank' for i in self.treasures]):
            self.current_gold = math.floor(self.current_gold * 1.2) + self.start_turn_gold + self.next_turn_addl_gold
        else:
            self.current_gold = self.start_turn_gold + self.next_turn_addl_gold
        self.total_gold_this_turn = self.current_gold
        # reset turn-specific trackers
        self.next_turn_addl_gold = 0
        self.spell_played_this_turn = False
        self.spell_purchased_this_turn = False
        self.chars_dead = []
        self.last_breath_multiplier_used_this_turn = False
        self.names_of_spells_this_turn = []

    def do_shop_phase(self):

        # obsolete code, chunking it out into choices for individual actions, as too many actions are not independent
        # # get all possible combinations of actions one could do at current shop
        # combinations = []
        # opts = self.shop + ['roll']
        # for n in range(len(opts)+1):
        #     combinations.append([i for i in itertools.combinations(opts, n)])
        # combinations = [item for sublist in combinations for item in sublist]
        #
        # # assess which choices can be done with current gold
        # legal_choices = self.get_possible_shop_options(combinations)
        #
        # choice = self.input_choose(legal_choices)
        for i in self.next_shop:
            for eff in self.effects:
                if isinstance(eff, Shop_Effect):
                    eff.apply_effect(i)
            i.set_zone('shop')
            self.shop.append(i)
        self.next_shop = []

        while True:
            # generate options list: buy each item in the shop, roll, or pass
            if len(self.shop) > 7:
                buy_options = self.shop[0:7]
            else:
                buy_options = self.shop
            sell_options = [i for i in self.hand]
            # assess legality of each choice
            legal_buy_options = self.get_possible_shop_options(buy_options)

            # if playing without logic, prevent selling as an option unless hand is full.
            # this is to make it play a little more realistically
            options = legal_buy_options + ['pass']

            # if there are legal targets for spells in hand, add them to options
            if self.spell_played_this_turn == False:
                for spell in self.spell_hand:
                    if spell.target == None:
                        options.append(spell)
                    else:
                        try:
                            spell.owner = self
                            spell.target.target_select(random_target= True)
                            spell.owner = None
                            options.append(spell)
                        # returns IndexError if no legal target
                        except IndexError:
                            pass

            if (self.logic!=None and self.logic.purchase_toggle) \
                or len(self.hand)+len(self.spell_hand)==11:
                options = options + sell_options
            selected = self.input_choose(options)
            for i in options:
                if hasattr(i,'name') and i.name == "Cat's Call":
                    selected = i
            if selected=='roll':
                if self.game.data_collector != None:
                    self.game.data_collector.collect_purchase_data(self, selected)
                self.roll_shop()
            elif selected=='pass':
                if self.game.verbose_lvl>=2:
                    print(self, 'passes')
                break
            elif isinstance(selected, Spell)==False and selected.zone!='shop':
                selected.sell()

            elif isinstance(selected, Spell) and selected in self.spell_hand:
                self.spell_hand.remove(selected)
                selected.cast(self)
            else:
                if self.game.data_collector != None:
                    self.game.data_collector.collect_purchase_data(self, selected)
                selected.purchase(self)
                upgrade_chars = self.check_for_upgrades()
                self.process_upgrades(upgrade_chars[0], upgrade_chars[1])
                self.check_effects()
            self.check_quest_completion()

        if self.input_bool('lock shop'):
            self.locked_shop = True
            if self.game.verbose_lvl>=2:
                print(self, 'locks the shop')
        else:
            self.locked_shop = False
            for i in self.shop:
                i.scrub_buffs(eob_only=False)
                i.owner = None
                if isinstance(i, Character):
                    self.game.add_to_char_pool(i)
            self.shop = []

    def roll_shop(self, free=False,beginning_of_turn = False):
        # reminder: Masquerade Ball, Drink me potion has a lot of similar code, modifications
        # here may need to be carried over there
        if self.game.verbose_lvl >=2:
            print(self, 'rolls shop')
        for i in self.shop:
            i.scrub_buffs(eob_only=False)

            i.owner = None
            if isinstance(i, Character) and i.inshop:
                self.game.add_to_char_pool(i)

        self.shop = []
        if beginning_of_turn and self.game.turn_counter == 1:
            self.shop = self.game.generate_shop(self, first_shop = True)
        else:
            self.shop = self.game.generate_shop(self)

        for eff in self.effects:
            if isinstance(eff, Shop_Effect):
                for obj in self.shop:
                    eff.apply_effect(obj)

        if free==False:
            self.current_gold -=1


        # hard coded mad catter hero effect
        if beginning_of_turn == False and self.hero.name=='Mad Catter':
            selected = random.choice([i for i in self.shop if isinstance(i, Character)])
            selected.change_atk_mod(self.lvl)
            selected.change_hlth_mod(self.lvl)


    def roll_partial_shop(self):
        addl_shop = self.game.generate_partial_shop(self)
        for eff in self.effects:
            if isinstance(eff, Shop_Effect):
                for obj in addl_shop:
                    eff.apply_effect(obj)
        self.shop = self.shop + addl_shop

        if self.game.verbose_lvl >=2:
            print(self, 'rolls partial shop')

    # deploy characters from hand to field
    def deploy_for_battle(self):
        # if player is dead, follow the last starting board as closely as possible
        if self.dead:
            for pos in range(1,8):
                if self.starting_board[pos] == None:
                    pass
                elif self.starting_board[pos] in self.hand:
                    self.starting_board[pos].add_to_board(plyr=self, position = pos)

        # TODO: Remove len() != 11, as it's a testing thing
        elif self.random_logic or len(self.hand) != 11:
            options = self.hand + ['empty']

            for pos in range(1,8):
                selected = self.input_choose(options, label='position_' + str(pos))
                if selected != 'empty':
                    selected.add_to_board(plyr=self, position = pos)
                    options.remove(selected)
        else:
            self.logic.deploy_chars_decision()

        self.deployed_chars = [i for i in self.board.values() if i != None]
        # apply all effects relevant to the board
        self.apply_board_effects()
        self.starting_board = self.board.copy()

    def apply_board_effects(self):
        # apply support effects
        # removing because support was already being added elsewhere
        # def _apply_support_effects(pos, support_pos):
        #     if pos != None:
        #         for i in pos.abils:
        #             if isinstance(i, Support_Effect):
        #                 for j in support_pos:
        #                     if j!= None and i.condition(j):
        #                         i.apply_effect(j)
        #
        # if any([i.name == 'Horn of Olympus' for i in self.treasures]):
        #     _apply_support_effects(self.board[5],(self.board[1],self.board[2],self.board[3],self.board[4]))
        #     _apply_support_effects(self.board[6],(self.board[1],self.board[2],self.board[3],self.board[4]))
        #     _apply_support_effects(self.board[7],(self.board[1],self.board[2],self.board[3],self.board[4]))
        # else:
        #     _apply_support_effects(self.board[5],(self.board[1],self.board[2]))
        #     _apply_support_effects(self.board[6],(self.board[2],self.board[3]))
        #     _apply_support_effects(self.board[7],(self.board[3],self.board[4]))

        self.check_effects()

    def end_of_turn_effects(self):
        # code to force a treasure to be discarded for testing purposes
        # if any([i.name=="Fool's Gold" for i in self.treasures]):
        #     self.discard_treasure([i for i in self.treasures if i.name == "Fool's Gold"][0])
        self.gain_exp()
        self.check_for_triggers('end of turn')
        assert self.get_hand_len() <= 11
        # remove all EOB modifiers from every character
        revert_transform = []
        for i in self.hand:
            i.scrub_buffs(eob_only=True)
            if i.eob_revert_char != None:
                revert_transform.append(i)

        for i in revert_transform:
            i.transform(i.eob_revert_char, temp_reversion = True,
                preserve_mods = False)

        assert all([i.token == False for i in self.hand if isinstance(i, Character)])

        rm_effects=[]
        for i in self.effects:
            if isinstance(i, Triggered_Effect) or isinstance(i, Purchase_Effect):
                # currently activated_this_turn only used by Fancy Pants and Phoenix_Feather
                i.activated_this_turn = False
                if i.eob:
                    i.remove_effect(self)

            if isinstance(i, Global_Static_Effect):
                if i.eob:
                    self.remove_effect(i)
                    rm_effects.append(i)

            if isinstance(i, Shop_Effect):
                if i.eob:
                    self.remove_shop_effect(i)
                    rm_effects.append(i)

        for i in rm_effects:
            self.effects.remove(i)

        if self.start_turn_gold<12:
            self.start_turn_gold += 1

        self.to_hand_this_turn=[]
        self.purchased_this_turn=[]

        #self.check_for_upgrades()

        #=================Treasure related functions==============
    def select_treasure(self,lvl, max_lim = 3):
        '''
            function for player to select a treasure to gain
            lvl - level of treasure to select
            max_lim - limit of number of treasures player can have. Only deviates from
                 3 when an effect will discard a treasure later.
        '''
        # check to see if there's any modifiers to the treasure level present
        lvl = self.check_treasure_level(lvl)
        if lvl > 7:
            lvl = 7

        # option to select treasures from any level to make it easier to test treasures
        if self.game.treasure_test:
            treasures = [i for i in self.game.treasures if i not in
                self.treasures and i not in self.obtained_treasures]
        else:
            treasures = [i for i in self.game.treasures if i.lvl == lvl and i not in
                self.treasures and i not in self.obtained_treasures]
        # remove treasures with conflicting alignment settings
        if any([i.name == 'Corrupted Heartwood' for i in self.treasures]) and \
            any([i.name == 'Crown of Atlas' for i in treasures]):
                treasures.remove(Crown_of_Atlas)
        if any([i.name == 'Crown of Atlas' for i in self.treasures])  and \
            any([i.name == 'Corrupted Heartwood' for i in treasures]):
            treasures.remove(Corrupted_Heartwood)

        # select candidate treasures
        choices = random.sample(treasures, 3)
        choice = self.input_choose(choices,label='treasure select')
        #choice = [i for i in self.game.treasures if i.name == 'Sword of Fire and Ice'][0]
        if self.game.verbose_lvl>=2:
            print(self, 'gains', choice)
        assert len(self.treasures)<=max_lim
        if len(self.treasures)==max_lim:
            remove_choice = self.input_choose(self.treasures, label='treasure remove')
            if self.game.verbose_lvl>=2:
                print(self, 'discards', remove_choice)
            self.discard_treasure(remove_choice)

        # code to test a certain treasures effect with mimic
        if self.game.mimic_test:
            if all([i.name!="Mimic" for i in self.treasures]) and \
                len(self.treasures)<=0:
                choice = [i for i in self.game.treasures if i.name == "Mimic"][0]
                self.gain_treasure(choice)
                choice = [i for i in self.game.treasures if i.name == "Evil Eye"][0]
                #choice = random.choice([i for i in self.game.treasures])

        # code to force a treasure to be taken for testing purposes
        if lvl == 2 and self.game.mimic_test == False and all([i.name!="Helm of the Ugly Gosling" for i in self.treasures]):
            choice = [i for i in self.game.treasures if i.name == "Helm of the Ugly Gosling"][0]

        self.gain_treasure(choice)

    def gain_treasure(self, treasure):

        '''
        function for player to gain treasure
        treasure - treasure object to gain
        '''
        assert treasure.name not in [i.name for i in self.treasures]

        treasure_copy = treasure.create_copy()
        self.check_for_triggers('gain treasure')
        self.treasures.append(treasure_copy)
        self.obtained_treasures.append(treasure)
        treasure_copy.owner = self
        treasure_copy.game = self.game
        if treasure_copy.abils!=None:

            # add treasure effects to player
            for abil in treasure_copy.abils:

                # add triggers
                if hasattr(abil, 'trigger'):
                    self.triggers.append(abil.trigger)

                # special instructions depending on the type of effect
                if isinstance(abil, Treasure_Effect_Multiplier):
                    for eff in treasure_copy.get_owner().effects:
                        if abil not in eff.effects and isinstance(eff, Treasure_Effect_Multiplier) == False \
                        and isinstance(eff.source, Treasure) and abil.condition(eff.source):
                            eff.effects.append(abil)
                            abil.apply_effect(eff)

                if isinstance(abil, Player_Effect):
                    abil.apply_effect(abil.source)

                if isinstance(abil, Shop_Effect):
                    for i in self.shop:
                        abil.apply_effect(i)

                # if not one of the above types, add to effects
                if isinstance(abil, Effect) and abil not in self.effects:
                    self.effects.append(abil)

            # check for any treasure multipler effects already on the player
            for abil in self.effects:
                if isinstance(abil, Treasure_Effect_Multiplier):
                    for eff in treasure_copy.abils:
                        if abil not in eff.effects \
                            and isinstance(eff.source, Treasure) and abil.condition(eff.source):
                            eff.effects.append(abil)
                            abil.apply_effect(eff)


    def discard_treasure(self, treasure):
        assert treasure.owner == self
        if treasure.abils!=None:
            for abil in treasure.abils:

                if isinstance(abil, Player_Effect):
                    for _ in range(collections.Counter(self.effects)[abil]):
                        abil.reverse_effect(abil.source)
                        self.effects.remove(abil)

                elif isinstance(abil, Global_Static_Effect):
                    for _ in range(collections.Counter(self.effects)[abil]):
                        self.remove_effect(abil)

                elif isinstance(abil, Treasure_Effect_Multiplier):
                    for eff in treasure.get_owner().effects:
                        if abil in eff.effects:
                            eff.effects.remove(abil)
                            abil.reverse_effect(eff)

                elif isinstance(abil, Shop_Effect):
                    for i in self.shop:
                        for _ in range(collections.Counter(i.effects)[abil]):
                            abil.reverse_effect(i)
                            i.effects.remove(abil)

                if hasattr(abil, 'trigger'):
                    self.triggers.remove(abil.trigger)

                if abil in self.effects:
                    self.effects.remove(abil)
        self.treasures.remove(treasure)
        treasure.last_owner = self
        treasure.owner = None


    # get counts
    def check_for_upgrades(self):
        name_counts = collections.Counter([i.name for i in self.hand if i.upgraded==False])

        # note any characters with three or more copies
        upgrade_chars = [i for i in name_counts if name_counts[i] >= 3]
        # check for any characters that only require two characters
        if 'Nian, Sea Terror' in name_counts.keys():
            two_char_check = ['Nian, Sea Terror']
        else:
            two_char_check = []
        for abil in self.effects:
            if isinstance(abil, Upgrade_Reduce_Effect):
                for char in self.hand:
                    if abil.condition(char) and char.name not in two_char_check \
                        and char.upgraded == False:
                        two_char_check.append(char.name)

        for name in two_char_check:
            if name_counts[name] == 2:
                upgrade_chars.append(name)

        return [upgrade_chars,two_char_check]

    def process_upgrades(self, upgrade_chars, two_char_check):
        for name in upgrade_chars:
            if self.game.verbose_lvl>=2:
                print(self,'upgrades',name)
            if name in two_char_check:
                copies = [i for i in self.hand if i.name==name][0:2]

            else:
                copies = [i for i in self.hand if i.name==name][0:3]
            keep_copy = random.choice(copies)
            if 'Prince' in keep_copy.type or 'Princess' in keep_copy.type:
                self.trackers['Royals_upgraded'] += 1
            # if any of the copies have a different alignment than the base alignment
            # the upgraded copy will have that different alignment
            diff_align_copies = [i for i in copies if i.get_alignment() != i.alignment]
            for i in diff_align_copies:
                diff_align = i.get_alignment()
                keep_copy.alignment_mod.append(diff_align)

            # move the rest of the copies into limbo (not in hand, but not in pool)
            limbo_copies = copies.copy()
            limbo_copies.remove(keep_copy)
            for i in limbo_copies:

                # add buffs to upgraded copy
                keep_copy.change_atk_mod(max(0, i.atk_mod))
                keep_copy.change_hlth_mod(max(0, i.hlth_mod))

                i.scrub_buffs(eob_only=False)
                i.remove_from_hand(return_to_pool=False)
                keep_copy.upgrade_copies.append(i)
                i.set_zone(keep_copy.upgrade_copies)
            keep_copy.upgraded=True
            treasure_lvl = keep_copy.lvl
            # hard coded blind mouse treasure increase
            if name == 'Blind Mouse':
                treasure_lvl +=2
            self.select_treasure(treasure_lvl)


    # check for effects to modify treasure level
    def check_treasure_level(self, lvl):
        for eff in self.effects:
            if isinstance(eff,Treasure_Level_Mod):
                lvl = eff.apply_effect(base_lvl=lvl)
        return lvl

    #================= misc utility functions==============

    def check_for_triggers(self, type, triggering_obj=None, triggered_obj = None, effect_kwargs = None,
        cond_kwargs = None):
        '''
        Function to check player's trigger attribute for any appropriate triggers
        params:
        type - string, type of trigger being checked for
        triggering_obj - if appropriate, the object that caused the trigger. If present,
        check to make sure the object also meets the trigger's condition
        triggered_obj - if appropriate, the object that had the trigger applied
        to it. This is currently only for slay trigger when a creature is slain
        '''

        # identify triggers of the checked type
        triggers = [i for i in self.triggers if i.type == type]

        self.resolve_triggers(type, triggers, triggering_obj = triggering_obj,
            triggered_obj = triggered_obj, effect_kwargs = effect_kwargs,
            cond_kwargs = cond_kwargs)

    def resolve_triggers(self, type, triggers,triggering_obj=None, triggered_obj = None,
        effect_kwargs=None, cond_kwargs=None):

        for i in triggers:
            # if object present, check to ensure the condition is met
            if triggering_obj != None:
                condition_obj = triggering_obj
            # if it's none, check the condition for the source of the trigger
            else:
                condition_obj = i.source

            # types of triggers with triggered objs, and effect kwargs
            if type == 'global slay':
                if i.condition(i, condition_obj, triggered_obj):
                    if self.game.verbose_lvl>=4:
                        print('triggering',i)
                    i.source.trigger_effect(effect_kwargs)

            # types of triggers with effect kwargs
            elif type in ['die','opponent die', 'survive damage','summon','attack', 'deal damage','attacked',
                'change_mod','target', 'lose life']:
                if i.condition(i, condition_obj):
                    if self.game.verbose_lvl>=4:
                        print('triggering',i)
                    i.source.trigger_effect(effect_kwargs)

            # types of triggers with cond_kwargs
            elif type in ['cast']:
                if i.condition(i, condition_obj, cond_kwargs['in_combat']):
                    if self.game.verbose_lvl>=4:
                        print('triggering',i)
                    i.source.trigger_effect(effect_kwargs)

            # all other triggers
            else:
                if i.condition(i, condition_obj):
                    if self.game.verbose_lvl>=4:
                        print('triggering',i)
                    i.source.trigger_effect()

        # for i in p.hand:
        #     for abil in i.abils:
        #         if isinstance(abil, Triggered_Effect) and abil.trigger.type==type:
        #             abil.trigger_effect()
        #
        # for t in p.treasures:
        #     for abil in i.abils:
        #         if isinstance(abil, Triggered_Effect) and abil.trigger.type==type:
        #             abil.trigger_effect()

    # check to see if any global effects affect anything new
    def check_effects(self):

        self.check_for_triggers('atk/hlth >25')

        # check for effects
        assert all([i.zone == self.hand for i in self.hand if isinstance(i, Character)])
        for eff in self.effects:
            if isinstance(eff, Global_Static_Effect):
                apply_scope = self.hand
                # if eff.both_sides and self.opponent != None:
                #     apply_scope += self.opponent.hand
                for char in apply_scope:

                    if char!= None:
                        if eff not in char.effects and eff.condition(char):
                            char.effects.append(eff)
                            eff.apply_effect(char)

                        if eff in char.effects and eff.condition(char)==False:
                            char.effects.remove(eff)
                            eff.reverse_effect(char)


        # check to see if characters have gone

            # if isinstance(eff, Treasure_Effect_Multiplier):
            #     for plyr_eff in self.effects:
            #         if eff not in plyr_eff.effects and isinstance(plyr_eff, Treasure_Effect_Multiplier) == False \
            #             and isinstance(plyr_eff.source, Treasure) and eff.condition(plyr_eff.source):
            #                 plyr_eff.effects.append(eff)
            #                 plyr_eff.multiplier = eff.apply_effect(plyr_eff.multiplier)
            #
            #         if eff in plyr_eff.effects and isinstance(plyr_eff, Treasure_Effect_Multiplier) == False \
            #             and isinstance(plyr_eff.source, Treasure) and eff.condition(plyr_eff.source)==False:
            #                 plyr_eff.effects.remove(eff)
            #                 plyr_eff.multiplier = eff.reverse_effect(plyr_eff.multiplier)


    def check_quest_completion(self):
        for char in self.hand:
            for abil in char.abils:
                if isinstance(abil, Quest) and abil.completed and abil.finish_effect_resolved == False:
                    for _ in range(abil.multiplier):
                        abil.finish_effect()



    # remove an effect that's leaving
    def remove_effect(self, effect):
        for char in self.hand:
            if char!=None:
                if effect in char.effects:
                    char.effects.remove(effect)
                    effect.reverse_effect(char)

    def remove_shop_effect(self, effect):
        for char in self.shop:
            if char!=None:
                if effect in char.effects:
                    # effect removed from char in reverse_effect call
                    effect.reverse_effect(char)

    def gain_gold_next_turn(self, amt):
        self.next_turn_addl_gold += amt

    def get_possible_shop_options(self, buy_options):
        # convert combinations to costs
        legal_buy_options=[]
        if self.current_gold>0:
            legal_buy_options.append('roll')
        for item in buy_options:
            if isinstance(item, Spell) and item.get_cost()<= self.current_gold and self.spell_played_this_turn==False:
                # if the spell targets, make sure there's a legal target
                if item.target==None:
                    legal_buy_options.append(item)
                elif item.target.check_for_legal_targets(self):
                    legal_buy_options.append(item)
            if isinstance(item, Character) and item.get_cost()<= self.current_gold and self.get_hand_len()<11:
                legal_buy_options.append(item)

        assert all([i in buy_options or i=='roll' for i in legal_buy_options])
        return legal_buy_options

    def gain_exp(self, amt=1):
        if self.lvl < 6:
            self.xp += amt
            self.check_for_lvl_up()

    def check_for_lvl_up(self):
        while self.xp>=3 and self.lvl<6:
            self.xp -= 3
            if self.hero.name != 'Peter Pants':
                self.lvl += 1
                if self.game.verbose_lvl>=2:
                    print(self, 'levels up to level', self.lvl)
            else:
                self.trackers['Peter_Pants_lvl_up_count'] += 1

    def clear_board(self):
        # reverse order for clearing board so chars with support effects are removed first
        for i in reversed(range(1,8)):
            char = self.board[i]
            if char != None:
                char.remove_from_board()

        self.board={1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None}

    def check_for_empty_board(self):
        return all([i==None for i in self.board.values()])

    # function for spawning multiple tokens
    def multi_spawn(self, ori_token, num, start_pos, upgraded):
        position = start_pos
        for _ in range(num):
            if position != None:
                token = ori_token.create_copy(self, ori_token.name+ ' Spawn')
                if upgraded:
                    token.base_atk *= 2
                    token.base_hlth *= 2
                self.board[position] = token
                token.position = position
                # if there are no empty positions, this function will return None and
                # no further tokens will be spawned
                position = self.find_next_spawn_position(position)

    # function for finding where to spawn the next token
    def find_next_spawn_position(self, start_pos):
        if start_pos == 1:
            order = [1,2,3,4,5,6,7]
        if start_pos == 2:
            order = [2,3,1,4,5,6,7]
        if start_pos == 3:
            order = [3,4,2,1,6,7,5]
        if start_pos == 4:
            order = [4,3,2,1,7,6,5]
        if start_pos == 5:
            order = [5,6,7,1,2,3,4]
        if start_pos == 6:
            order = [6,5,7,2,3,4,1]
        if start_pos == 7:
            order = [7,5,6,4,3,2,1]

        # depending on the position that the call started from,
        # go through the position order and find the first empty space
        for n in order:
            if self.board[n] == None:
                return n

        # if no empty spaces exist, return None
        assert all([i!=None for i in self.board.values()])
        return None


    def life_loss(self, amt):
        self.check_for_triggers('lose life', effect_kwargs={'amount':amt})
        self.life -= amt
        if self.game.verbose_lvl>=2:
            if self not in self.game.ghosts:
                print(self,'loses',amt,'life. Life total is now',self.life)
            else:
                print(self,'loses',amt,'life.', self, 'is already a ghost.')

    def life_gain(self, amt):
        self.life += amt
        if self.game.verbose_lvl>=2:
            print(self,'gains',amt,'life. Life total is now',self.life)


    # check if dead, if so remove self from game
    def check_for_death(self):
        if self.life <= 0:
            if self.game.verbose_lvl>=1:
                print(self, 'is out of the game')
            self.dead= True
            self.game_position = len(self.game.active_players)

            self.remove_hero()

            No_Hero = Hero(name='No Hero')
            self.add_hero(No_Hero)

            start = datetime.now()

            # return any chars to the shop
            for i in self.shop:
                i.scrub_buffs(eob_only=False)

                i.owner = None
                if isinstance(i, Character) and i.inshop:
                    self.game.add_to_char_pool(i)

            self.shop = []

            for i in self.hand.copy():
                owner = i.owner

                # make a copy in case needed for ghost fight
                # start = datetime.now()
                char_copy = i.create_copy(owner, 'Ghost Copy')
                # end= datetime.now() - start
                # if end.microseconds> 100000:
                #     print('unexpectedly long time to make copy, '+ str(end) +
                #     ', check for deep copies being made')
                #
                # return a copy to the char pool
                i.remove_from_hand()

                char_copy.add_to_hand(owner, dead_player = True)
                i.scrub_buffs()
                i.owner = None

            self.game.active_players.remove(self)
            self.game.ghosts.append(self)

    def check_spells_in_shop(self):
        return all(self.spells_in_shop)

    def get_hand_len(self):
        return len(self.hand) + len(self.spell_hand)
    #================= actions requiring player input==============
    # Yes/No input
    def input_bool(self,label=None,obj=None):
        decision=self.rand_decisions([True, False])
        # if self.logic!=None:
        #    decision=self.logic.input_bool(player=self,obj=obj,decision=decision,label=label)
        return(decision)

    # choose from list
    def input_choose(self, choices, label=None, n=1,
        permit_empty_list=False, squeeze=True):
        if permit_empty_list and choices==[]:
            if self.game.verbose>=2:
                print('no choices available')
            return None
        if n == 'any':
            decision=self.rand_decisions(choices, np.random.randint(0,len(choices)+1))
        else:
            decision=self.rand_decisions(choices, n)
        # if self.logic!=None:
        #     decision=self.logic.input_choose(player=self,decision=decision,
        #         choices=choices, label=label,n=n)

        if squeeze==False and isinstance(decision, list)==False:
            decision=[decision]
        return(decision)

    # specify an order of a list of objects
    def input_order(self, object_list,label=None):
        random.shuffle(object_list)
        # if self.logic!=None:
        #     object_list=self.logic.input_order(player=self,object_list=object_list
        #         ,label=label)
        return(object_list)

    # placeholder decision making: random
    def rand_decisions(self,choices,n=1):
        if n==1:
            choice=random.choice(choices)
        else:
            choice=random.sample(choices,n)
        return(choice)

    def check_for_treasure(self, treasure_name):
        return any([i.name == treasure_name for i in self.treasures])

    def display_status(self):
        print(self)
        print('Life:',self.life)
        print('Level:',self.lvl,'Exp:',self.xp)
        print('Hero:',self.hero)
        print('Hand:',self.hand)
        print('Board:',self.board)
        print('Treasures:',self.treasures)
        print('Shop:',self.shop)

    def get_board_char_names(self):
        return [i.name for i in self.board.values() if i != None]

    def __repr__(self):
        output = self.name
        if self.game.verbose_lvl >=3 and self.hero != None:
            output = self.name + ' (' + self.hero.name + ')'
        return output
