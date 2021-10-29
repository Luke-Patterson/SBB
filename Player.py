from Effects import *
from Heroes import *
from c_Treasure import Treasure
import itertools
import copy
import random
from Spells import *
from Characters import *
import pandas as pd
from datetime import datetime

class Player:
    def __init__(self, name:str, logic=None):
        self.name=name
        self.game = None
        # 1-4 is the front row from left to right, 5-7 is the back row
        self.board={1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None}
        self.hand=[]
        # track what chars went into hand this turn
        self.to_hand_this_turn=[]
        # list to hold  units used for an upgrade separate
        self.upgrade_limbo=[]
        self.shop=[]
        self.locked_shop = False
        self.life=40
        self.lvl =2
        self.xp=0
        self.start_turn_gold=2
        self.current_gold=0
        self.next_turn_addl_gold=0
        self.treasures=[]
        # list of all treasures obtained during a game (can't be obtained again)
        self.obtained_treasures = []
        self.logic=logic
        self.spell_played_this_turn = False
        self.opponent = None
        self.last_opponent = None
        self.dead = False
        self.effects=[]
        self.triggers=[]
        # triggers that are specific to battles
        self.battle_triggers=[]
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

    def choose_hero(self, choices):
        # force a hero for testing
        # if Hoard_Dragon in choices:
        #     hero = Hoard_Dragon
        # else:
        hero = self.input_choose(choices, label='hero selection')
        self.hero = hero
        self.hero.owner = self
        self.hero.apply_effect()
        not_chosen = choices
        not_chosen.remove(hero)
        return(not_chosen)

    #================= turn order functions==============

    def start_of_turn_effects(self):
        # reset shop
        if self.locked_shop==False:
            self.roll_shop(free=True)
        else:
            self.roll_partial_shop()

        self.check_for_triggers('start of turn')
        self.check_for_upgrades()

        # reset gold
        if any([i.name=='Piggie Bank' for i in self.treasures]):
            self.current_gold = self.current_gold + self.start_turn_gold + self.next_turn_addl_gold
        else:
            self.current_gold = self.start_turn_gold + self.next_turn_addl_gold

        # reset turn-specific trackers
        self.next_turn_addl_gold = 0
        self.spell_played_this_turn = False
        self.chars_dead = []


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
            buy_options = self.shop
            sell_options = [i for i in self.hand]
            # assess legality of each choice
            legal_buy_options = self.get_possible_shop_options(buy_options)

            # if playing without logic, prevent selling as an option unless hand is full.
            # this is to make it play a little more realistically
            options = legal_buy_options + ['pass']
            if self.logic!=None or len(self.hand)==11:
                options = options + sell_options
            selected = self.input_choose(options)
            for i in options:
                if hasattr(i,'name') and i.name == "Cat's Call":
                    selected = i
            # TODO: add selling as a legal option
            if selected=='roll':
                self.roll_shop()
            elif selected=='pass':
                if self.game.verbose_lvl>=2:
                    print(self, 'passes')
                break
            elif isinstance(selected, Spell)==False and selected.zone!='shop':
                selected.sell()
            else:
                selected.purchase(self)
                self.check_for_upgrades()
                self.check_effects()



        if self.input_bool('lock shop'):
            self.locked_shop = True
            if self.game.verbose_lvl>=2:
                print(self, 'locks the shop')
        else:
            self.locked_shop = False
            for i in self.shop:
                if isinstance(i, Character):
                    self.game.add_to_char_pool(i)
            self.shop = []

    def roll_shop(self, free=False):
        # reminder: Masquerade Ball, Drink me potion has a lot of similar code, modifications
        # here may need to be carried over there
        for i in self.shop:
            i.scrub_buffs(eob_only=False)
            i.owner = None
            if isinstance(i, Character) and i.inshop:
                self.game.add_to_char_pool(i)


        self.shop = []
        self.shop = self.game.generate_shop(self)

        for eff in self.effects:
            if isinstance(eff, Shop_Effect):
                for obj in self.shop:
                    eff.apply_effect(obj)

        if free==False:
            self.current_gold -=1

        if self.game.verbose_lvl >=2:
            print(self, 'rolls shop')

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
        options = self.hand + ['empty']
        for pos in range(1,8):
            selected = self.input_choose(options, label='position_' + str(pos))
            if selected != 'empty':
                selected.add_to_board(plyr=self, position = pos)
                options.remove(selected)

        # apply all effects relevant to the board
        self.apply_board_effects()

    def apply_board_effects(self):
        # apply support effects
        def _apply_support_effects(pos, support_pos):
            if pos != None:
                for i in pos.abils:
                    if isinstance(i, Support_Effect):
                        for j in support_pos:
                            if j!= None and i.condition(j):
                                i.apply_effect(j)
                                j.eob_reverse_effects.append(i)

        _apply_support_effects(self.board[5],(self.board[1],self.board[2]))
        _apply_support_effects(self.board[6],(self.board[2],self.board[3]))
        _apply_support_effects(self.board[7],(self.board[3],self.board[4]))

        self.check_effects()

    def end_of_turn_effects(self):
        # code to force a treasure to be discarded for testing purposes
        # if any([i.name=="Fool's Gold" for i in self.treasures]):
        #     self.discard_treasure([i for i in self.treasures if i.name == "Fool's Gold"][0])
        self.gain_exp()
        self.check_for_triggers('end of turn')

        # remove all EOB modifiers from every character
        revert_transform = []
        for i in self.hand:
            i.scrub_buffs(eob_only=True)
            if i.eob_revert_char != None:
                revert_transform.append(i)

        for i in revert_transform:
            i.transform(i.eob_revert_char, temp_reversion = True,
                preserve_mods = False)

        assert all([i.token == False for i in self.hand])

        for i in self.effects:
            if isinstance(i, Triggered_Effect):
                # currently only used by Fancy Pants
                i.activated_this_turn = False
                if i.eob:
                    i.remove_effect(self)

        if self.start_turn_gold<12:
            self.start_turn_gold += 1

        self.to_hand_this_turn=[]

        self.check_for_upgrades()

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

        # code to force a treasure to be taken for testing purposes
        if lvl == 2 and all([i.name!="Mimic" for i in self.treasures]) and \
            len(self.treasures)<=1:
            choice = [i for i in self.game.treasures if i.name == "Mimic"][0]
            self.gain_treasure(choice)
            #choice = [i for i in self.game.treasures if i.name == "Locked Chest"][0]
            choice = random.choice([i for i in self.game.treasures])
            self.gain_treasure(choice)

        else:
            self.gain_treasure(choice)

    def gain_treasure(self, treasure):

        '''
        function for player to gain treasure
        treasure - treasure object to gain
        '''

        treasure_copy = treasure.create_copy()
        self.treasures.append(treasure_copy)
        self.obtained_treasures.append(treasure)
        treasure_copy.owner = self
        treasure_copy.game = self.game
        if treasure_copy.abils!=None:

            # check for any treasure multipler effects already on the player
            for abil in self.effects:
                if isinstance(abil, Treasure_Effect_Multiplier):
                    for eff in treasure_copy.abils:
                        if abil not in eff.effects \
                            and isinstance(eff.source, Treasure) and abil.condition(eff.source):
                            eff.effects.append(abil)
                            abil.apply_effect(eff)

            # add treasure effects
            for abil in treasure_copy.abils:
                if hasattr(abil, 'trigger'):
                    self.triggers.append(abil.trigger)
                elif isinstance(abil, Treasure_Effect_Multiplier):
                    for eff in treasure_copy.owner.effects:
                        if abil not in eff.effects and isinstance(eff, Treasure_Effect_Multiplier) == False \
                        and isinstance(eff.source, Treasure) and abil.condition(eff.source):
                            eff.effects.append(abil)
                            abil.apply_effect(eff)
                if isinstance(abil, Player_Effect):
                    abil.apply_effect(abil.source)
                elif isinstance(abil, Effect):
                    self.effects.append(abil)



    def discard_treasure(self, treasure):
        assert treasure.owner == self
        if treasure.abils!=None:
            for abil in treasure.abils:
                if isinstance(abil, Player_Effect):
                    abil.reverse_effect(abil.source)
                elif isinstance(abil, Global_Static_Effect):
                    self.remove_effect(abil)
                elif isinstance(abil, Treasure_Effect_Multiplier):
                    for eff in treasure.owner.effects:
                        if abil in eff.effects:
                            eff.effects.remove(abil)
                            abil.reverse_effect(eff)

                if hasattr(abil, 'trigger'):
                    self.triggers.remove(abil.trigger)

                self.effects.remove(abil)

        self.treasures.remove(treasure)
        treasure.last_owner = self
        treasure.owner = None

    def check_for_upgrades(self):
        name_counts = pd.Series([i.name for i in self.hand if i.upgraded==False]).value_counts()
        for name in name_counts.loc[name_counts>=3].index:
            if self.game.verbose_lvl>=2:
                print(self,'upgrades',name)
            copies = [i for i in self.hand if i.name==name][0:3]
            keep_copy = random.choice(copies)
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


    def check_for_triggers(self, type, triggering_obj=None, triggered_obj = None, effect_kwargs = None):
        '''
        Function to check player's trigger attribute for any appropriate triggers
        params:
        type - string, type of trigger being checked for
        triggering_obj - if appropriate, the object that caused the trigger. If present,
        check to make sure the object also meets the trigger's condition
        triggered_obj - if appropriate, the object that had the trigger applied
        to it. This is currently only for slay trigger when a creature is slain
        '''

        for i in self.triggers:
            # if object present, check to ensure the condition is met
            if triggering_obj != None:
                condition_obj = triggering_obj
            # if it's none, check the condition for the source of the trigger
            else:
                condition_obj = i.source
            if type == 'global slay':
                if i.type == type and i.condition(i, condition_obj, triggered_obj):
                    if self.game.verbose_lvl>=4:
                        print('triggering',i)
                    i.source.trigger_effect(effect_kwargs)
            elif type in ['die', 'survive damage']:
                if i.type == type and i.condition(i, condition_obj):
                    if self.game.verbose_lvl>=4:
                        print('triggering',i)
                    i.source.trigger_effect(effect_kwargs)
            else:
                if i.type == type and i.condition(i, condition_obj):
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
        assert all([i.zone == self.hand for i in self.hand])
        for eff in self.effects:
            if isinstance(eff, Global_Static_Effect):
                for char in self.hand:
                    if char!= None:
                        if eff not in char.effects and eff.condition(char):
                            char.effects.append(eff)
                            eff.apply_effect(char)

                        if eff in char.effects and eff.condition(char)==False:
                            char.effects.remove(eff)
                            eff.reverse_effect(char)

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


    # remove an effect that's leaving
    def remove_effect(self, effect):
        for char in self.hand:
            if char!=None:
                if effect in char.effects:
                    char.effects.remove(effect)
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
            if isinstance(item, Character) and item.get_cost()<= self.current_gold and len(self.hand)<11:
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
            self.lvl += 1
            if self.game.verbose_lvl>=2:
                print(self, 'levels up to level', self.lvl)

    def clear_board(self):
        for i in range(1,8):
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
            order = [2,3,4,5,6,7,1]
        if start_pos == 2:
            order = [3,1,4,5,6,7,2]
        if start_pos == 3:
            order = [4,2,1,6,7,5,3]
        if start_pos == 4:
            order = [3,2,1,7,6,5,4]
        if start_pos == 5:
            order = [6,7,1,2,3,4,5]
        if start_pos == 6:
            order = [5,7,2,3,4,1,6]
        if start_pos == 7:
            order = [5,6,4,3,2,1,7]

        # depending on the position that the call started from,
        # go through the position order and find the first empty space
        for n in order:
            if self.board[n] == None:
                return n

        # if no empty spaces exist, return None
        assert all([i!=None for i in self.board.values()])
        return None


    def life_loss(self, amt):
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
        start = datetime.now()
        if self.life <= 0:
            if self.game.verbose_lvl>=1:
                print(self, 'is out of the game')
            self.dead= True
            if self.name == 'Player6':
                import pdb; pdb.set_trace()
            for i in self.hand.copy():
                owner = i.owner

                # return a copy to the char pool
                i.remove_from_hand()

                # make a copy in case needed for ghost fight
                char_copy = i.create_copy(owner, 'Ghost Copy')
                char_copy.add_to_hand(owner)
                i.scrub_buffs()
                i.owner = None
            self.game.active_players.remove(self)
            self.game.ghosts.append(self)
            end= datetime.now() - start
            if end.microseconds> 100000:
                print('unexpectedly long time to process death, '+ str(end) +
                    ', check for deep copies being made')

    def check_spells_in_shop(self):
        return all(self.spells_in_shop)

    #================= actions requiring player input==============
    # Yes/No input
    def input_bool(self,label=None,obj=None):
        decision=self.rand_decisions([True, False])
        if self.logic!=None:
            decision=self.logic.input_bool(player=self,obj=obj,decision=decision,label=label)
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
        if self.logic!=None:
            decision=self.logic.input_choose(player=self,decision=decision,
                choices=choices, label=label,n=n)

        if squeeze==False and isinstance(decision, list)==False:
            decision=[decision]
        return(decision)

    # specify an order of a list of objects
    def input_order(self, object_list,label=None):
        random.shuffle(object_list)
        if self.logic!=None:
            object_list=self.logic.input_order(player=self,object_list=object_list
                ,label=label)
        return(object_list)

    # placeholder decision making: random
    def rand_decisions(self,choices,n=1):
        if n==1:
            choice=random.choice(choices)
        else:
            choice=random.sample(choices,n)
        return(choice)

    def display_status(self):
        print(self)
        print('Life:',self.life)
        print('Level:',self.lvl,'Exp:',self.exp)
        print('Hero:',self.hero)
        print('Hand:',self.hand)
        print('Board:',self.board)
        print('Treasures:',self.treasures)
        print('Shop:',self.shop)

    def __repr__(self):
        return self.name
