class signal_generator:
    """ Signal generator class

    It creates different signals depending on the events it's given.

    Examplee of an events list:
    [
        {
            "start": {
                "value": 10
            }
        },
        {
            "step": {
                "cycle": 100,
                "value": 0
            }
        },
        {
            "ramp_up": {
                "cycle": 200,
                "value": 0.01   # increase in output per cycle
            }
        },
        {
            "ramp_down": {
                "cycle": 300,
                "value": 0.02   # increase in output per cycle
            }
        },
        {
            "pause": {
                "cycle": 350            
            }
        }
    ]
    """
    def __init__(self, events):
        self.events = events
        self.current_value = 0
        self.cycles_with_events = self.get_cycles_with_events()
        self.current_event = None

        for el in events:
            if "start" in el:
                self.current_value = el["start"]["value"]

    def get_cycles_with_events(self):
        """ Return a list with which cycles an event change will occur. """
        cycles = []
        for el in self.events:
            for key in el:
                if type(el[key]) == dict and "cycle" in el[key]:
                    cycles.append(el[key]["cycle"])
        return cycles if  len(cycles) > 0 else None
    
    def calculate(self, cycle):
        # at first cycle just return the initial value
        if cycle == 0:
            return self.current_value
        # update current event
        if self.cycles_with_events:
            if cycle in self.cycles_with_events:
                self.current_event = self.get_event_by_cycle(cycle)
        # run current event
        if self.current_event:
            key = list(self.current_event)[0]
            updater = getattr(self, key, None)
            if callable(updater):
                updater()
        return self.current_value

    def get_event_by_cycle(self, cycle):
        for el in self.events:
            for key in el:
                if type(el[key]) == dict and "cycle" in el[key]:
                    if el[key]["cycle"] == cycle:
                        return el
    
    # event functions
    def step(self):
        value = self.current_event["step"]["value"]
        self.current_value = value

    def ramp_up(self):
        value = self.current_event["ramp_up"]["value"]
        self.current_value = self.current_value + value

    def ramp_down(self):
        value = self.current_event["ramp_down"]["value"]
        self.current_value = self.current_value - value

    def pause(self):
        # no need to update the current value
        pass
