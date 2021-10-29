import copy

class Treasure:
    def __init__(self,name, lvl, abils):
        self.name=name
        self.lvl=lvl
        self.abils=abils
        self.last_owner = None
        if abils!=None:
            for i in self.abils:
                i.add_to_obj(self)

    def create_copy(self):
        copy_treasure = copy.deepcopy(self)
        if copy_treasure.abils!=None:
            for i in copy_treasure.abils:
                i.add_to_obj(copy_treasure)

        return(copy_treasure)

    def __repr__(self):
        return self.name
