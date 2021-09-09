from copy import deepcopy

class Spell:

    def __init__(self, name, lvl, cost, effects):
        self.name=name
        self.lvl=lvl
        self.cost=cost
        self.effects=effects

    def __repr__(self):
        return self.name

objs=deepcopy(list(locals().keys()))
master_spell_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Spell):
        master_spell_list.append(obj)
