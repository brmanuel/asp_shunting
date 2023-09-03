
from abc import abstractmethod, ABC


from model import Before, Last, Shunt


class Visualize(ABC):
    @abstractmethod
    def visualize(self, model):
        """Visualize the solution to the hump-shunting problem given by <model>."""


class VisualizeBasic(Visualize):
    def visualize(self, model):
        solution = model.facts(atoms=True)
        befores = solution.query(Before).all()
        print(list(befores))

class VisualizeText(Visualize):
      
    
    def visualize(self, model):
        solution = model.facts(atoms=True)
        befores = solution.query(Before).all()
        lasts = solution.query(Last).all()
        shunts = solution.query(Shunt).all()
        steps = {}
        
        for before in befores:
            if before.move not in steps:
                steps[before.move] = {}
            step_tracks = steps[before.move]
            if before.track not in step_tracks:
                step_tracks[before.track] = {}
            track = step_tracks[before.track]
            track[before.second_car] = before.first_car
        for last in lasts:
            step_tracks = steps[last.move]
            if last.track not in step_tracks:
                step_tracks[last.track] = {}
            track = step_tracks[last.track]
            track["LAST"] = last.car

        step_shunt = {}
        for shunt in shunts:
            step_shunt[shunt.move] = shunt.track
            
        for step in sorted(steps.keys())[1:]:
            print(f"Step {step}")
            for track in sorted(steps[step].keys()):
                track_order = steps[step][track]
                car = track_order["LAST"]
                sorted_track = [car]
                while car in track_order:
                    car = track_order[car]
                    sorted_track.insert(0, car)
                track_str = f"{track}: {sorted_track}"
                if step_shunt[step] == track:
                    track_str += " -->"
                print(track_str)
            print()
                
        
