class BaseModel:
    def __init__(self):
        pass

    def update_attributes(self, **kwargs):
        """ Method to update the attributes from an instance

        If the type of the value equals the attribute, the value
        is copied to the attribute.

        But if the attribute is a list and the value is not,
        the value is appended to the list.

        """
        for attr in kwargs:
            try:
                instance_attr = getattr(self, attr)
                value_type = type(kwargs[attr])
                attr_type = type(instance_attr)
                if value_type == attr_type:
                    setattr(self, attr, kwargs[attr])
                elif attr_type == list:
                    instance_attr.append(kwargs[attr])
                else:
                    raise ValueError("Attribute exists but is not compatible with the given value", instance_attr, kwargs[attr])
            except AttributeError:
                pass

    def reset(self):
        raise NotImplementedError("Class {} don't implement a reset method.".format(self.__class__.__name__))