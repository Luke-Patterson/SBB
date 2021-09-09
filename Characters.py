from copy import deepcopy

class Character:
    def __init__(self, name, atk, hlth, lvl, abils=[], alignment='Neutral'):
        self.name=name
        self.base_atk=atk
        self.base_htlh=hlth
        self.atk_mod= 0
        self.htlh_mod= 0
        self.abils=abils
        self.lvl=lvl
        self.alignment=alignment
        self.base_cost = lvl
        self.current_cost= lvl

    def __repr__(self):
        return self.name

Baad_Billy_Gruff = Character(
    name='B-a-a-d Billy Gruff',
    atk=2,
    hlth=3,
    alignment='Evil',
    lvl=2
)

objs=deepcopy(list(locals().keys()))
master_char_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Character):
        master_char_list.append(obj)
