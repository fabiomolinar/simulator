import itertools

class Line():
    def __init__(self, model, variable, spec):
        """ A class used to extract values from the models
        
        If there is no data transformation to be done, 
        then just return the value from the model. Otherwise,
        transform the data and save it here to avoid recalculation.
        
        """
        self.model = model
        self.variable = variable
        self.multiplier = spec["multiplier"] if "multiplier" in spec else None
        self.spec = spec
        self.transformed_values = []
        self.first = True

    def get_values(self):
        model_values = getattr(self.model, self.variable)
        if not self.multiplier:
            return model_values
        else:
            """ For additional values on the returned values 
            from the model transform and save it """
            for value in itertools.islice(model_values, len(self.transformed_values), None):
                if value is None:
                    self.transformed_values.append(None)
                else:
                    self.transformed_values.append(value*self.multiplier)
            return self.transformed_values
