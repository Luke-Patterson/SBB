from c_Treasure import Treasure
import random

class Effect:
    def __init__(self,name, effect_func=None, reverse_effect_func = None, condition = lambda x: True,
        modifier = None, once_per_turn=False, multi_ignore = False):
        self.name = name
        self.effect_func = effect_func
        self.reverse_effect_func = reverse_effect_func
        self.condition = condition
        self.source = None
        self.modifier = modifier
        self.once_per_turn = once_per_turn
        self.activated_this_turn = False
        # how many times each effect will trigger
        self.multiplier = 1
        self.effects = []
        # If a effect has no effect when multiplied, ignore multiplier changes
        self.multi_ignore = multi_ignore

    def add_to_obj(self, obj):
        self.source = obj
        if self.modifier!=None:
            self.modifier.source = obj
            self.modifier.source_abil = self

    def apply_effect(self, char):
        for _ in range(self.multipler):
            self.effect_func(char)

    def reverse_effect(self, char):
        self.reverse_effect_func(char)

    def increment_effect_multiplier(self):
        self.multiplier += 1

    def decrease_effect_multiplier(self):
        self.multiplier -= 1

    def __repr__(self):
        return self.name

# Effect to reduce number of characters needed to upgrade
class Upgrade_Reduce_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)

    # condition object stores the condition chars must meet for the char to require
    # only two chars

# Effect that modifiers level of treasures a player gets
# Effect is added to a player object's effect attribute
class Treasure_Level_Mod(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Treasure Level Modifier'

    def apply_effect(self, base_lvl):
        for _ in range(self.multiplier):
            base_lvl = self.effect_func(base_lvl)
        return base_lvl


class Treasure_Effect_Multiplier(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Treasure Effect Multiplier'

    def apply_effect(self, effect):
        if effect.multi_ignore == False and self.condition(effect):
            effect.increment_effect_multiplier()

    def reverse_effect(self, effect):
        if effect.multi_ignore == False and self.condition(effect):
            effect.decrease_effect_multiplier()

# class Support_Effect_Multiplier(Effect):
#     def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
#         condition = lambda x: True, modifier = None, multi_ignore=False):
#         super().__init__(name,effect_func, reverse_effect_func, condition, modifier
#             , multi_ignore= multi_ignore)
#         self.type='Support Effect Multiplier'
#
#     def apply_effect(self, effect):
#         if effect.multi_ignore == False and self.condition(effect):
#             for _ in range(self.multiplier):
#                 effect.increment_effect_multiplier()
#
#     def reverse_effect(self, effect):
#         if effect.multi_ignore == False and self.condition(effect):
#             for _ in range(self.multiplier):
#                 effect.decrease_effect_multiplier()


# Effect that affects a player
# Effect is added to a player object's effect attribute
class Player_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Player Effect'

    def apply_effect(self, source):
        for _ in range(self.multiplier):
            self.effect_func(self, source.owner)
            source.get_owner().effects.append(self)

    def reverse_effect(self, source):
        self.reverse_effect_func(self, source.owner)

    # for static effects, every time the multiplier changes, we have to
    # check all objects in a player's possession and add/remove an instance of the
    # effect accordingly
    def increment_effect_multiplier(self):
        self.multiplier += 1
        self.effect_func(self, self.source.owner)
        self.source.get_owner().effects.append(self)

    def decrease_effect_multiplier(self):
        self.multiplier -= 1
        assert self.multiplier != 0
        self.reverse_effect_func(self, self.source.owner)
        self.source.get_owner().effects.remove(self)

# Effect that provides a support bonus for supporting characters
# Effect is added to a character object's abil attribute
class Support_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Support Effect'

    def apply_effect(self, char):
        for _ in range(char.get_owner().support_effects_multiplier):
            self.effect_func(char, self.source)
            char.effects.append(self)

    # can rely on multiplier for reverse as there's no way to alter support
    # multipliers in combat, which is the only time support effects are reversed
    # update: don't need to use multiplier as a copy of the effect is added
    # for each multiplier and reverse_effect is called for each copy
    def reverse_effect(self, char):
        # for _ in range(char.get_owner().support_effects_multiplier):
        self.reverse_effect_func(char, self.source)

# Effect that occurs on a character's death
# Effect is added to a character object's abil attribute
class Last_Breath_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Death Effect'

    def apply_effect(self, char):
        for _ in range(self.multiplier):
            self.effect_func(char)

# Effect that affects a character on purchase
# Effect is added to a player's abil attribute
class Purchase_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, once_per_turn = False
        , multi_ignore=False, eob=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier,
            once_per_turn, multi_ignore= multi_ignore)
        self.type='Purchase Effect'
        self.eob = eob

    def apply_effect(self, eff, char):
        if self.activated_this_turn == False:
            for _ in range(self.multiplier):
                self.effect_func(char, eff)

        if self.once_per_turn:
            self.activated_this_turn = True

# Static effects that will only affect the character itself and are always
# on regardless of zone
# Effect is added to a character object's abil attribute
class Local_Static_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Local Static Effect'

    def add_to_obj(self, obj):
        self.source = obj
        self.apply_effect(obj)

    def apply_effect(self, selfchar):
        for _ in range(self.multiplier):
            self.effect_func(selfchar)

    def reverse_effect(self, selfchar):
        self.reverse_effect_func(selfchar)

    # for static effects, every time the multiplier changes, we have to
    # check all objects in a player's possession and add/remove an instance of the
    # effect accordingly
    def increment_effect_multiplier(self):
        self.multiplier += 1
        self.effect_func(self)
        self.source.get_owner().effects.append(self)

    def decrease_effect_multiplier(self):
        self.multiplier -= 1
        assert self.multiplier != 0
        self.reverse_effect_func(self)
        self.source.get_owner().effects.remove(self)


# Static effects that will affect all characters a player has (with conditions)
# Effect is added to both a character and player object's effect attribute
class Global_Static_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False, both_sides=False,
        eob = False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Global Static Effect'
        self.source = None
        self.both_sides = both_sides
        self.eob = eob

    def apply_effect(self, obj):
        for _ in range(self.multiplier):
            self.effect_func(obj)


    def reverse_effect(self, obj):
        for _ in range(self.multiplier):
            self.reverse_effect_func(obj)

    # for static effects, every time the multiplier changes, we have to
    # check all objects in a player's possession and add/remove an instance of the
    # effect accordingly
    def increment_effect_multiplier(self):
        self.multiplier += 1
        self.source.get_owner().effects.append(self)
        for char in self.source.get_owner().hand:
            if self in char.effects:
                self.effect_func(char)


    def decrease_effect_multiplier(self):
        self.multiplier -= 1
        assert self.multiplier != 0
        self.source.get_owner().effects.remove(self)
        for char in self.source.get_owner().hand:
            if self in char.effects:
                self.reverse_effect_func(char)


# effect that modifies objects in a player's shop
# Effect is added to a player's effect attribute. Character's costs/stats are
# modified, but effect is not stored in character's effect attribute
class Shop_Effect(Effect):
    def __init__(self, name:str, char_effect_func = None, char_reverse_effect_func = None,
            spell_effect_func = None, spell_reverse_effect_func=None,
            condition = lambda x: True, modifier= None, multi_ignore=False, eob = False):
        super().__init__(name, condition, modifier, multi_ignore= multi_ignore)

        def _error_raise(x):
            raise 'wrong type of effect func called for a shop effect. should be char_ or spell_ effect'
        self.effect_func = _error_raise
        self.reverse_effect_func = _error_raise

        self.type='Shop Effect'
        self.source = None
        self.char_effect_func = char_effect_func
        self.char_reverse_effect_func = char_reverse_effect_func
        self.spell_effect_func = spell_effect_func
        self.spell_reverse_effect_func = spell_reverse_effect_func
        self.eob = eob

    def apply_effect(self, obj):
        obj.effects.append(self)
        for _ in range(self.multiplier):
            if self.char_effect_func != None and obj.__class__.__name__=='Character' and self.condition(obj):
                self.char_effect_func(obj)
            if self.spell_effect_func != None and obj.__class__.__name__=='Spell' and self.condition(obj):
                self.spell_effect_func(obj)

    def reverse_effect(self, obj):
        if self.char_reverse_effect_func != None and obj.__class__.__name__=='Character':
            self.char_reverse_effect_func(obj)
        if self.spell_reverse_effect_func != None and obj.__class__.__name__=='Spell':
            self.spell_reverse_effect_func(obj)

    # for static effects, every time the multiplier changes, we have to
    # check all objects in a player's possession and add/remove an instance of the
    # effect accordingly
    def increment_effect_multiplier(self):
        self.multiplier += 1
        self.source.get_owner().effects.append(self)
        for obj in self.source.get_owner().shop:
            if self in obj.effects:
                if self.char_effect_func != None and obj.__class__.__name__=='Character' and self.condition(obj):
                    self.char_effect_func(obj)
                if self.spell_effect_func != None and obj.__class__.__name__=='Spell' and self.condition(obj):
                    self.spell_effect_func(obj)

    def decrease_effect_multiplier(self):
        self.multiplier -= 1
        assert self.multiplier != 0
        self.source.get_owner().effects.remove(self)
        for obj in self.source.get_owner().shop:
            if self in obj.effects:
                if self.char_reverse_effect_func != None and obj.__class__.__name__=='Character':
                    self.char_reverse_effect_func(obj)
                if self.spell_reverse_effect_func != None and obj.__class__.__name__=='Spell':
                    self.spell_reverse_effect_func(obj)

# effect that triggers on a certain condition.
# Effect is added to a player's effect attribute or character's abil attribute,
# depending on the type of trigger.
class Triggered_Effect(Effect):
    def __init__(self, name:str, trigger, effect_func, condition = lambda obj: True,
        counter = None, eob=False, multi_ignore=False, once_per_turn = False):
        super().__init__(name, effect_func, condition = condition , multi_ignore=multi_ignore)
        self.trigger = trigger
        self.trigger.source = self
        self.effect_func = effect_func
        self.source = None
        self.condition = condition
        self.counter = counter
        self.eob = eob
        self.activated_this_turn = False
        self.once_per_turn = once_per_turn
        self.type = 'Triggered Effect'

    def trigger_effect(self, effect_kwargs= None):

        # if statement handles two types of trigger limiters
        # first statement handles if a counter trigger hits zero, or it doesn't have a counter
        # second statement handles if a once per turn trigger has been activated
        if (self.counter == None or self.counter <= 0) and \
            self.activated_this_turn == False:
            if self.condition(self.source):
                if self.once_per_turn:
                    self.activated_this_turn = True

                for _ in range(self.multiplier):
                    if effect_kwargs == None:
                        self.effect_func(self.source)
                    else:
                        self.effect_func(self.source, **effect_kwargs)


            # for treasures with counters, remove them when they hit zero
            if self.counter != None and isinstance(self.source, Treasure) \
                and self.source.owner != None:
                self.source.get_owner().discard_treasure(self.source)


        elif self.counter != None:
            self.counter -= 1

    def apply_effect(self, obj):
        self.source = obj
        obj.effects.append(self)
        obj.triggers.append(self.trigger)

    def remove_effect(self, obj):
        self.source = None
        obj.effects.remove(self)
        obj.triggers.remove(self.trigger)

    def __repr__(self):
        return self.name


class Quest(Triggered_Effect):
    def __init__(self, name:str, trigger, counter, effect_func = None, increment = 1
        , multi_ignore=False):
        super().__init__(name, trigger, effect_func , multi_ignore = multi_ignore)
        self.counter = counter
        self.counter_start_val = counter
        self.source = None
        self.increment = increment
        self.completed = False
        self.finish_effect_resolved = False
        self.type = 'Quest'

    def finish_effect(self):
        if self.source.game.verbose_lvl >= 3:
            print(self.source,'Quest finishes')
        self.source.upgraded = True

        selected_lvl = self.source.lvl
        if self.source.get_owner().check_for_treasure('Noble Steed'):
            selected_lvl += 1
            if self.source.get_owner().check_for_treasure('Mimic'):
                selected_lvl += 1
            if self.source.get_owner().hero.name == 'Celestial Tiger':
                selected_lvl += 1

        self.source.get_owner().select_treasure(selected_lvl)
        self.finish_effect_resolved = True

    # args added so the function can handle triggers with effect kwargs
    def trigger_effect(self, *args, **kwargs):
        if self.trigger.type == 'deal damage':
            # damage dealt should be being passed in kwargs
            self.counter -= locals()['args'][0]['damage_dealt']
            if self.source.game.verbose_lvl >= 4:
                print(self,'counter decreases by', locals()['args'][0]['damage_dealt'])
        else:
            self.counter -= self.increment
            if self.source.game.verbose_lvl >= 4:
                print(self,'counter decreases')

        if self.counter<=0:
            self.completed = True



    def __repr__(self):
        return self.name

class Spell_Multiplier(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Spell Multiplier'

    def apply_effect(self, spell, multiplier):
        for _ in range(self.multiplier):
            if self.condition(spell):
                multiplier += 1

        return multiplier


class Modifier:
    def __init__(self, name:str, atk_func = None, hlth_func=None, oth_func=None,
        oth_reverse_func=None, eob = False):
        self.name = name
        self.source= None
        self.source_abil = None
        self.atk_func = atk_func
        self.hlth_func = hlth_func
        self.oth_func = oth_func
        self.oth_reverse_func = oth_reverse_func
        self.eob = eob

    def __repr__(self):
        return self.name

class Trigger:
    def __init__(self, name:str, type, condition= lambda self, condition_obj,
        triggered_obj = None: True):

        '''
        object representing a trigger that needs to be checked for
        params:
        name - name of trigger
        type - type of trigger. influences when this particular trigger is checked for
        condition - a function with three arguments:
            self - this should be the trigger object itself
            condition_obj - the object that caused the trigger to activate. For
            example, for slay triggers, this is the character that slew.
            For many triggers this is just the source of the trigger and often not used.
            triggered_obj - only used by slay triggers triggered. This is the character
            that was slew in that case.
        '''

        self.name = name
        assert type in ['buy','start of combat','end of combat','cast','purchase'
            ,'slay','die','opponent die','attack', 'target', 'global slay', # if any char slays
            'start of turn', 'end of turn', 'survive damage','clear front row',
            'summon', 'deal damage', 'atk/hlth >25','attacked', 'change_mod',
            'gain treasure','gain hero','start of game','lose life']
        # make sure type is one of the ones that have been programmed
        self.type = type
        self.condition = condition
        self.source=None

    def __repr__(self):
        return self.name

class Target:

    def __init__(self, name:str, condition = lambda x: True):
        self.name = name
        self.condition = condition
        self.source= None

    def target_select(self, random_target):
        legal_targets = []
        for i in self.source.get_owner().hand:
            if self.condition(i):
                legal_targets.append(i)
        if random_target:
            self.source.selected_target = random.choice(legal_targets)
        else:
            self.source.selected_target = self.source.get_owner().input_choose(legal_targets)

        # only check for target triggers if the spell was purchased
        if self.source.purchased:
            self.source.get_owner().check_for_triggers('target', triggering_obj = self.source.selected_target,
                effect_kwargs={'targeted':self.source.selected_target})

        # hard coded hack to get sleeping princess' transform to transfer the
        # target of the spell to the transformed Awakened Princess.
        if self.source.purchased and self.source.selected_target.name == 'Sleeping Princess':
            # the last object in the owner's hand should be the transformed princess
            assert self.source.get_owner().hand[-1].name == 'Awakened Princess'
            self.source.selected_target = self.source.get_owner().hand[-1]

    def check_for_legal_targets(self, plyr):
        legal_targets = []
        for i in plyr.hand:
            if self.condition(i):
                legal_targets.append(i)
        return len(legal_targets)>0

    def __repr__(self):
        return self.name
