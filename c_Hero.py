from copy import deepcopy

class Hero:
    def __init__(self, name:str, abils=None, reverse_abils=None, life=40):
        self.name=name
        self.life=life
        self.abils=abils
        if abils!=None:
            for i in self.abils:
                i.source = self
        self.reverse_abils=reverse_abils
        self.owner=None

    def apply_effect(self):
        if self.abils!=None:
            for abil in self.abils:
                abil.apply_effect(self)
                if hasattr(abil, 'trigger'):
                    self.owner.triggers.append(abil.trigger)

    def __repr__(self):
        return self.name
