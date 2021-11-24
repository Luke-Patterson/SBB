from copy import deepcopy
from Effects import Player_Effect
from Effects import Treasure_Effect_Multiplier
from Effects import Shop_Effect
from Effects import Global_Static_Effect
from Effects import Effect
from c_Treasure import Treasure
import collections
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

    def apply_effects(self):
        if self.abils!=None:
            for abil in self.abils:

                if isinstance(abil, Treasure_Effect_Multiplier):
                    for eff in self.owner.effects:
                        if abil not in eff.effects and isinstance(eff, Treasure_Effect_Multiplier) == False \
                        and isinstance(eff.source, Treasure) and abil.condition(eff.source):
                            eff.effects.append(abil)
                            abil.apply_effect(eff)

                elif isinstance(abil, Player_Effect):
                    abil.apply_effect(self)

                elif isinstance(abil, Shop_Effect):
                    for i in self.owner.shop:
                        abil.apply_effect(i)

                if hasattr(abil, 'trigger'):
                    self.owner.triggers.append(abil.trigger)

                if isinstance(abil, Effect) and abil not in self.owner.effects:
                    self.owner.effects.append(abil)

    def remove_effects(self):
        if self.abils!=None:
            for abil in self.abils:

                if isinstance(abil, Player_Effect):
                    for _ in range(collections.Counter(self.owner.effects)[abil]):
                        abil.reverse_effect(self)
                        self.owner.effects.remove(abil)

                elif isinstance(abil, Global_Static_Effect):
                    self.owner.remove_effect(abil)

                elif isinstance(abil, Shop_Effect):
                    for i in self.owner.shop:
                        for _ in range(collections.Counter(i.effects)[abil]):
                            abil.reverse_effect(i)
                            i.effects.remove(abil)

                if hasattr(abil, 'trigger'):
                    self.owner.triggers.remove(abil.trigger)

                if isinstance(abil, Effect) and abil in self.owner.effects:
                    self.owner.effects.remove(abil)

    def __repr__(self):
        return self.name
