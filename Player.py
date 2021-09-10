import itertools
import random
from Spells import *
from Characters import *

class Player:
    def __init__(self, name=None, logic=None):
        self.name=name
        self.game = None
        # 1-4 is the front row from left to right, 5-7 is the back row
        self.board={1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None}
        self.hand=[]
        self.shop=[]
        self.locked_shop = False
        self.life=40
        self.lvl =2
        self.xp=0
        self.start_turn_gold=2
        self.current_gold=0
        self.treasures=[]
        self.logic=logic
        self.spell_played_this_turn = False

    def choose_hero(self, choices):
        hero = self.input_choose(choices, label='hero selection')
        self.hero = hero
        not_chosen = choices
        not_chosen.remove(hero)
        return(not_chosen)

    #================= turn order functions==============

    def start_of_turn_effects(self):
        self.current_gold = self.start_turn_gold
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
                import pdb; pdb.set_trace()
                options = options + sell_options
            selected = self.input_choose(options)

            # TODO: add selling as a legal option
            if selected=='roll':
                for i in self.shop:
                    self.game.char_pool.append(i)
                self.shop = []
                self.shop = self.game.generate_shop(self)
                self.current_gold -=1
                if self.game.verbose_lvl >=2:
                    print(self, 'rolls')
            elif selected=='pass':
                if self.game.verbose_lvl>=2:
                    print(self, 'passes')
                break
            elif isinstance(selected, Spell)==False and selected.owner==self:
                selected.sell()
            else:
                selected.purchase(self)

        if self.input_bool('lock shop'):
            self.locked_shop = True
            if self.game.verbose_lvl>=2:
                print(self, 'locks the shop')
        else:
            for i in self.shop:
                self.game.char_pool.append(i)
            self.shop = []

    # deploy characters from hand to field
    def deploy_for_battle(self):
        options = self.hand + ['empty']
        for pos in range(1,8):
            selected = self.input_choose(options, label='position ' + str(pos))
            if selected != 'empty':
                self.board[pos] = selected
                options.remove(selected)
        import pdb; pdb.set_trace()

    def end_of_turn_effects(self):
        self.gain_exp()
        if self.start_turn_gold<12:
            self.start_turn_gold += 1

    #================= misc utility functions==============

    def get_possible_shop_options(self, buy_options):
        # convert combinations to costs
        legal_buy_options=[]
        if self.current_gold>0:
            legal_buy_options.append('roll')
        for item in buy_options:
            if isinstance(item, Spell) and item.get_cost()<= self.current_gold and self.spell_played_this_turn==False:
                legal_buy_options.append(item)
            if isinstance(item, Character) and item.get_cost()<= self.current_gold and len(self.hand)<11:
                legal_buy_options.append(item)
        return legal_buy_options

    def gain_exp(self, amt=1):
        if self.lvl < 6:
            self.xp += amt
            self.check_for_lvl_up()

    def check_for_lvl_up(self):
        while self.xp>=3 & self.lvl<6:
            self.xp -= 3
            self.lvl += 1
            if self.game.verbose_lvl>=2:
                print(self, 'levels up to level', self.lvl)

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
