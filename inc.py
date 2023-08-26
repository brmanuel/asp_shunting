"""Multi-Shot control loop for shunting.
Taken largely from
https://github.com/potassco/clingo/blob/master/examples/clingo/multishot/inc.py
"""

import sys

from clingo.application import clingo_main, Application, ApplicationOptions
from clingo.control import Control
from clingo.solving import SolveResult
from clingo.symbol import Function, Number


class IncApp(Application):
    """ASP Application implementing Multi-Shot control loop."""
    
    def register_options(self, options: ApplicationOptions):
        """ Register program options."""
        # no options implemented
        pass

    @staticmethod
    def _on_model(m):
        print("atoms")
        print("  positive: " + ", ".join(map(str, m.symbols(atoms=True))))
        print("  negative: " + ", ".join(map(str, m.symbols(atoms=True, complement=True))))


    def main(self, ctl: Control, files):
        """The main function implementing incremental solving."""
        if not files or len(files) == 0:
            print("Usage: python inc.py <theory1.lp> [<theoryN.lp> ...]")
            exit(1)

        for file in files:
            ctl.load(file)

        # Add the external atom "query" that selectively turns on the
        # solution check of each step t.
        ctl.add("check", ["t"], "#external query(t).")

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
