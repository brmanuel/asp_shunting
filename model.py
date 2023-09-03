
from clorm import Predicate, IntegerField


class Track(Predicate):
    idx=IntegerField

class Car(Predicate):
    idx=IntegerField

class Initbefore(Predicate):
    first_car=IntegerField
    second_car=IntegerField
    track=IntegerField
    
class Initlast(Predicate):
    car=IntegerField
    track=IntegerField

class Before(Predicate):
    first_car=IntegerField
    second_car=IntegerField
    track=IntegerField
    move=IntegerField

class Last(Predicate):
    car=IntegerField
    track=IntegerField
    move=IntegerField

class Predecessor(Predicate):
    first_car=IntegerField
    second_car=IntegerField
    move=IntegerField

class Shunt(Predicate):
    track=IntegerField
    move=IntegerField



