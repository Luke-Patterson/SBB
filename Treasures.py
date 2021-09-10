from copy import deepcopy

class Treasure:
    def __init__(self,name, level, abils):
        self.name=name
        self.level=level
        self.abils=abils

    def __repr__(self):
        return self.name

objs=deepcopy(list(locals().keys()))
master_treasure_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Treasure):
        master_treasure_list.append(obj)
