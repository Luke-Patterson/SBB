from copy import deepcopy

class Character:
    def __init__(self, name, type, atk, hlth, lvl, abils=[], alignment='Neutral'):
        self.name=name
        self.type=type
        self.base_atk=atk
        self.base_htlh=hlth
        self.atk_mod= 0
        self.htlh_mod= 0
        self.abils=abils
        self.lvl=lvl
        self.alignment=alignment
        self.base_cost = lvl
        self.current_cost= lvl
        self.owner = None
        self.zone = None

    def purchase(self, player):
        self.owner = player
        self.owner.shop.remove(self)
        self.zone = self.owner.hand
        self.owner.hand.append(self)
        self.owner.current_gold -= self.current_cost
        if self.owner.game.verbose_lvl>=2:
            print(self.owner, 'purchases', self)

    def get_cost(self):
        return self.current_cost

    def sell(self):
        self.owner.hand.remove(self)
        self.owner.game.char_pool.append(self)
        self.owner.current_gold += 1
        if self.owner.game.verbose_lvl>=2:
            print(self.owner, 'sells', self)
        self.owner = None

    def __repr__(self):
        return self.name

Baad_Billy_Gruff = Character(
    name='B-a-a-d Billy Gruff',
    atk=2,
    hlth=3,
    alignment='Evil',
    lvl=2,
    type=['Animal']
)

Tiny = Character(
    name='Tiny',
    atk=6,
    hlth=1,
    alignment='Neutral',
    lvl=2,
    type=['Dwarf']
)

Golden_Chicken = Character(
    name='Golden Chicken',
    atk=2,
    hlth=2,
    alignment='Neutral',
    lvl=2,
    type=['Animal']
)

Blind_Mouse = Character(
    name='Blind Mouse',
    atk=2,
    hlth=2,
    alignment='Neutral',
    lvl=2,
    type=['Animal']
)

Cinderella = Character(
    name='Cinder-ella',
    atk=2,
    hlth=2,
    alignment='Neutral',
    lvl=2,
    type=['Princess','Mage']
)

Fanny = Character(
    name='Fanny',
    atk=2,
    hlth=2,
    alignment='Neutral',
    lvl=2,
    type=['Dwarf']
)

objs=deepcopy(list(locals().keys()))
master_char_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Character):
        master_char_list.append(obj)
