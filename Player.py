
class Player:
    def __init__(self, name=None):
        self.name=name
        self.game = None
        self.board={1:None, 2:None, 3:None, 4:None, 5:None, 6:None, 7:None}
        self.hand=[]
        self.shop=[]
        self.life=40
        self.lvl =2
        self.xp=0
        self.start_turn_gold=2
        self.current_gold=0
        self.treasures=[]
        self.logic=None

    def choose_hero(self, choices):
        hero = self.input_choose(choices, label='hero selection', squeeze=False)
        self.hero = hero
        not_chosen = choices
        not_chosen.remove(hero)
        return(not_chosen)

    #================= turn order functions==============

    def start_of_turn_effects(self):
        if self.start_turn_gold<12:
            self.start_turn_gold += 1
        self.current_gold = self.start_turn_gold

    def do_shop_phase(self):
        shop = self.game.generate_shop(self)

    def end_of_turn_effects(self):
        self.gain_exp()

    #================= misc utility functions==============

    def gain_exp(self, amt=1):
        if self.lvl < 6:
            self.xp += amt
            self.check_for_lvl_up()

    def check_for_lvl_up(self):
        while self.xp>=3 & self.lvl<6:
            self.xp -= 3
            self.lvl += 1

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
