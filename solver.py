import click
from clorm.clingo import Control
from clorm import FactBase

from model import (
    Track,
    Car,
    Initbefore,
    Before,
    Last,
    Predecessor,
    Shunt
)



def on_model(model):
    solution = model.facts(atoms=True)
    befores = solution.query(Before).all()
    print(list(befores))


@click.command()
@click.argument("filename")
def main(filename):
    ctrl = Control(unifier=[Track, Car, Initbefore, Before, Last, Predecessor, Shunt])
    ctrl.load(filename)

    init_facts = [
        Initbefore(first_car=3, second_car=2, track=1),
        Initbefore(first_car=2, second_car=1, track=1)
    ]
    instance = FactBase(init_facts)
    ctrl.add_facts(instance)
    ctrl.ground([("base",[])])

    ctrl.solve(on_model=on_model)


if __name__ == "__main__":
    main()