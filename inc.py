"""Multi-Shot control loop for shunting.
Taken largely from
https://github.com/potassco/clingo/blob/master/examples/clingo/multishot/inc.py
"""

import sys
import click

from clingo.application import clingo_main, Application, ApplicationOptions
from clingo.solving import SolveResult
from clingo.symbol import Function, Number

from clorm.clingo import Control
from clorm import FactBase

from model import (
    Track,
    Car,
    Initbefore,
    Initlast,
    Before,
    Last,
    Predecessor,
    Shunt
)
from visualize import Visualize, VisualizeText, VisualizeBasic


class IncApp(Application):
    """ASP Application implementing Multi-Shot control loop."""
    
    def register_options(self, options: ApplicationOptions):
        """ Register program options."""
        # no options implemented
        pass

    @staticmethod
    def _on_model(model):
        vis = VisualizeText()
        vis.visualize(model)
        

    def main(self, ctl_: Control, files):
        """The main function implementing incremental solving."""
        if not files or len(files) == 0:
            print("Usage: python inc.py <theory1.lp> [<theoryN.lp> ...]")
            exit(1)

        ctl = Control(
            unifier=[Track, Car, Initbefore, Before, Last, Predecessor, Shunt],
            control_=ctl_
        )
        for file in files:
            ctl.load(file)

        # Add the external atom "query" that selectively turns on the
        # solution check of each step t.
        # ctl.add("check", ["t"], "#external query(t).")
        init_facts = [
            Initbefore(first_car=5, second_car=4, track=1),
            Initbefore(first_car=4, second_car=3, track=1),
            Initbefore(first_car=3, second_car=2, track=1),
            Initbefore(first_car=2, second_car=1, track=1),
            Initlast(car=1, track=1)
        ]
        instance = FactBase(init_facts)
        ctl.add_facts(instance)

        step = 0
        ret = None
        while True:
            parts = []
            parts.append(("check", [Number(step)]))
            if step > 0:
                ctl.release_external(Function("query", [Number(step - 1)]))
                parts.append(("step", [Number(step)]))
            else:
                parts.append(("base", []))
            ctl.ground(parts)

            ctl.assign_external(Function("query", [Number(step)]), True)
            ret = ctl.solve(on_model=IncApp._on_model)
            step += 1
            if ret.satisfiable:
                break


clingo_main(IncApp(), sys.argv[1:])
