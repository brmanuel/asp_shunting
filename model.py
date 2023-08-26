
from clorm import Predicate, ConstantField, IntegerField


class Track(Predicate):
    idx=ConstantField

class Car(Predicate):
    idx=ConstantField

class InitBefore(Predicate):
    first_car=ConstantField
    second_car=ConstantField
    track=ConstantField
    
class Before(Predicate):
    first_car=ConstantField
    second_car=ConstantField
    track=ConstantField
    move=IntegerField

class Last(Predicate):
    car=ConstantField
    track=ConstantField
    move=IntegerField

class Predecessor(Predicate):
    first_car=ConstantField
    second_car=ConstantField
    move=IntegerField

class Shunt(Predicate):
    track=ConstantField
    move=IntegerField



