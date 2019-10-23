import os
import json
import time
import numpy as np
from multiprocessing.dummy import Pool
from functools import reduce
from simulator.settings import simulator_settings
from simulator.simulator import Simulator
from simulator.utils.performance_meter import PerformanceMeter


class BruteTuner:
    """Brute force algorithm to try to find the best PID settings
    
    This class runs multiple simulations with different PID settings
    and returns the best result found.
    """
    def __init__(self):
        self.settings = self.read_settings()
        self.cost_settings = self.settings["cost"]
        self.pid_name = self.settings["regulator"]["name"]
        self.p_range = self.settings.get("p_range", [1., 11.])
        self.p_steps = self.settings.get("p_steps")
        self.i_range = self.settings.get("i_range", [0., 10.])
        self.i_steps = self.settings.get("i_steps")
        self.d_range = self.settings.get("d_range", [0., 10.])
        self.d_steps = self.settings.get("d_steps")
        self.steps = self.settings.get("steps")
        self.max_combinations = self.settings.get("max_combinations", 1000)
        self.p_attr_name = "Kp"
        self.i_attr_name = "Ti"
        self.d_attr_name = "Td"
        self.results = []
        self.best_result = {}

        self.review_steps()

    def read_settings(self):
        path = os.path.join(simulator_settings["path_to_settings"], "tuner", "brute.json")
        if not os.path.exists(path):
            raise FileNotFoundError("Settings for the BruteTuner not found at {}".format(path))
        with open(path, "r") as rf:
            settings = json.load(rf)
        return settings

    def review_steps(self):
        """Method to make sure the step settings are correct
        
        This method is necessary due to the fact that the step settings
        can be set in different ways.
        """
        values_to_check = [self.p_steps, self.i_steps, self.d_steps]
        names_checked = ["p_steps", "i_steps", "d_steps"]
        # Return if all settings are already OK.
        if reduce(lambda x,y: x and y, map(lambda x: x is not None and x > 0, values_to_check)):
            return
        steps = self.steps
        # Fill non-confirming settings with self.steps if it's set.
        if steps is not None and steps > 0:
            for s in names_checked:
                s_value = getattr(self, s)
                if s_value is None or s_value < 1:
                    setattr(self, s, steps)
            return
        combinations_left = self.max_combinations
        # use the last resort setting to fill non-conforming steps settings.
        for i, s in enumerate(names_checked):
            s_value = getattr(self, s)
            if s_value is None or s_value < 1:
                value_to_try = int(combinations_left/(3-i))          
                value_to_set = value_to_try if value_to_try >= 1 else 1
                setattr(self, s, value_to_set)

    def run(self):
        # Check PerformanceMeter is enabled on the simulator.
        if not simulator_settings["performance_meter"]["enabled"]:
            raise ValueError("PerformanceMeter is not enabled.")
        p_to_test = np.linspace(self.p_range[0], self.p_range[1], self.p_steps)
        i_to_test = np.linspace(self.i_range[0], self.i_range[1], self.i_steps)
        d_to_test = np.linspace(self.d_range[0], self.d_range[1], self.d_steps)
        pid_possibilities = []
        for p in p_to_test:
            for i in i_to_test:
                for d in d_to_test:
                    pid_possibilities.append([p, i, d])
        # Adding simple parallelism
        pool = Pool()
        self.results = pool.starmap(self.run_sim, pid_possibilities)
        pool.close()
        pool.join()
        # Set best result
        self.find_best()
        # Printing results
        if not self.settings["quiet"]:
            print("""BruteTuner finished.
            Best result = {} with the following configuration:
            Kp = {}
            Ti = {}
            Td = {}
            """.format(
                self.best_result["result"],
                self.best_result["settings"]["p"],
                self.best_result["settings"]["i"],
                self.best_result["settings"]["d"]
            ))

    def find_best(self):
        self.best_result = self.results[0]
        for r in self.results:
            if r["result"] < self.best_result["result"]:
                self.best_result = r

    def run_sim(self, p, i, d):
        # Create simulation environment.
        duration = simulator_settings["duration"]
        dt = simulator_settings["dt"]
        sim = Simulator(simulator_settings["path_to_models"], dt, duration)
        pf = PerformanceMeter(sim, simulator_settings["performance_meter"])
        # Update PID settings.
        for tup in [(self.p_attr_name, p), (self.i_attr_name, i), (self.d_attr_name, d)]:
            setattr(sim.models[self.pid_name], tup[0], [tup[1]])
        # Run simulator.
        sim.run(None, pf)
        # Process result
        return {
            "result": self.calculate_result(pf),
            "settings": {
                "p": p,
                "i": i,
                "d": d
            }
        }

    def calculate_result(self, pf):
        # Getting references to the instances of performance meters
        _overshoot = pf.measurements[self.cost_settings["overshoot"]["name"]]
        _settling_time = pf.measurements[self.cost_settings["settling_time"]["name"]]
        # Getting weights and penalty settings
        overshoot_weight = self.cost_settings["overshoot"]["weight"]
        settling_time_weight = self.cost_settings["settling_time"]["weight"]
        settling_time_penalty = self.cost_settings["settling_time"]["not_settled_penalty"]
        # Calculate result
        overshoot_cost = _overshoot.max * overshoot_weight
        settling_time_cost = _settling_time.settle_time * settling_time_weight if _settling_time.settled else settling_time_penalty
        return overshoot_cost + settling_time_cost

class RecurringBruteTuner(BruteTuner):
    def __init__(self):
        super().__init__()
        self.divider = self.settings["recurring"]["divider"]
        self.threshold = self.settings["recurring"]["threshold"]
        self.max_loop_runs = self.settings["recurring"]["max_loop_runs"]

    def run(self):
        improvement = self.threshold + 1
        runs = 0
        while improvement > self.threshold and runs < self.max_loop_runs:
            if runs == 0:
                # only run it once and don't calculate improvement
                super().run()
                runs += 1
            else:
                # define new range
                divider = self.divider
                for s in [("p_range", "p"), ("i_range", "i"), ("d_range", "d")]:
                    s_value = getattr(self, s[0])
                    new_range = (s_value[1] - s_value[0])/divider
                    new_center = self.best_result["settings"][s[1]]
                    setattr(self, s[0], [new_center - new_range/2, new_center + new_range/2])
                # calculate new best
                old_best = self.best_result
                super().run()
                improvement = (old_best["result"] - self.best_result["result"])/old_best["result"]
                runs += 1            
        # Printing results
        if not self.settings["quiet"]:
            print("""RecurringBruteTuner finished.
            Best result = {} with the following configuration:
            Kp = {}
            Ti = {}
            Td = {}
            """.format(
                self.best_result["result"],
                self.best_result["settings"]["p"],
                self.best_result["settings"]["i"],
                self.best_result["settings"]["d"]
            ))