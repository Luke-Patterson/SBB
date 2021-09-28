from Effects import *
from Heroes import *
import itertools
import copy
import random
from Spells import *
from Characters import *
import pandas as pd

class Player:
    def __init__(self, name:str, logic=None):
        self.name=name
        self.game = None
        # 1-4 is the front row from left to right, 5-7 is the back row
        self.board={1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None}
        self.hand=[]
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
        self.logic=logic
        self.spell_played_this_turn = False
        self.opponent = None
        self.dead = False
        self.effects=[]
        self.triggers=[]
        # triggers that are specific to battles
        self.battle_triggers=[]
        # effects specific to a battle
        self.battle_effects=[]

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
        self.current_gold = self.start_turn_gold + self.next_turn_addl_gold
        self.next_turn_addl_gold = 0
        self.spell_played_this_turn = False

    def do_shop_phase(self):
        if self.locked_shop==False:
            self.shop = self.game.generate_shop(self)

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

            # TODO: add selling as a legal option
            if selected=='roll':
                self.roll_shop()
            elif selected=='pass':
                if self.game.verbose_lvl>=2:
                    print(self, 'passes')
                break
            elif isinstance(selected, Spell)==False and selected.zone!='pool':
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
            for i in self.shop:
                if isinstance(i, Character):
                    self.game.char_pool.append(i)
            self.shop = []

    def roll_shop(self, free=False):

        for i in self.shop:
            i.scrub_buffs(eob_only=False)
            i.owner = None
            if isinstance(i, Character):
                self.game.char_pool.append(i)

        self.shop = []
        self.shop = self.game.generate_shop(self)
        for eff in self.effects:
            if isinstance(eff, Shop_Effect):
                for obj in self.shop:
                    eff.apply_effect(obj)

        if free==False:
            self.current_gold -=1
        if self.game.verbose_lvl >=2:
            print(self, 'rolls')

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
        self.gain_exp()
        # remove all EOB modifiers from every character
        for i in self.hand:
            i.scrub_buffs(eob_only=True)

        self.check_for_triggers('end of turn')

        if self.start_turn_gold<12:
            self.start_turn_gold += 1

        #=================Treasure related functions==============
    def select_treasure(self,lvl):
        # check to see if there's any modifiers to the treasure level present
        lvl = self.check_treasure_level(lvl)
        if lvl > 7:
            lvl = 7

        treasures = [i for i in self.game.treasures if i.lvl == lvl and i not in self.treasures]
        choices = random.sample(treasures, 3)
        choice = self.input_choose(choices,label='treasure select')
        if self.game.verbose_lvl>=2:
            print(self, 'gains', choice)
        assert len(self.treasures)<=3
        if len(self.treasures)==3:
            remove_choice = self.input_choose(self.treasures, label='treasure remove')
            if self.game.verbose_lvl>=2:
                print(self, 'discards', remove_choice)
            self.discard_treasure(remove_choice)
        self.gain_treasure(choice)

    def gain_treasure(self, treasure):
        treasure_copy = treasure.create_copy()
        self.treasures.append(treasure_copy)
        treasure_copy.owner = self
        if treasure_copy.abils!=None:
            for abil in treasure_copy.abils:
                if isinstance(abil, Effect):
                    self.effects.append(abil)
                if hasattr(abil, 'trigger'):
                    self.triggers.append(abil.trigger)

    def discard_treasure(self, treasure):
        assert treasure.owner == self
        self.treasures.remove(treasure)
        treasure.owner = None
        if treasure.abils!=None:
            for abil in treasure.abils:
                if isinstance(abil, Global_Static_Effect):
                    self.remove_effect(abil)
                if hasattr(abil, 'trigger'):
                    self.triggers.remove(abil.trigger)

    def check_for_upgrades(self):
        name_counts = pd.Series([i.name for i in self.hand if i.upgraded==False]).value_counts()
        for name in name_counts.loc[name_counts>=3].index:
            if self.game.verbose_lvl>=2:
                print(self,'upgrades',name)
            copies = [i for i in self.hand if i.name==name]
            keep_copy = random.choice(copies)
            limbo_copies = copies.copy()
            limbo_copies.remove(keep_copy)
            for i in limbo_copies:
                i.scrub_buffs(eob_only=False)
                self.hand.remove(i)
                keep_copy.upgrade_copies.append(i)
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


    def check_for_triggers(self, type):
        for i in self.triggers:
            if i.type == type:
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

    def life_loss(self, amt):
        self.life -= amt
        if self.game.verbose_lvl>=2:
            print(self,'loses',amt,'life. Life total is now',self.life)

    # check if dead, if so remove self from game
    def check_for_death(self):
        if self.life <= 0:
            if self.game.verbose_lvl>=1:
                print(self, 'is out of the game')
            self.dead= True
            for i in self.hand.copy():
                i.owner.game.char_pool.append(i)

                # make a copy in case needed for ghost fight
                i.owner.hand.append(copy.copy(i))
                i.owner.hand.remove(i)
                i.scrub_buffs()
                i.owner = None
            self.game.players.remove(self)
            self.game.ghosts.append(self)
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

    def __repr__(self):
        return self.name
