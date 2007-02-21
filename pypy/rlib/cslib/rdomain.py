
class ConsistencyError(Exception):
    pass

class BaseFiniteDomain:
    """
    Variable Domain with a finite set of int values
    """

    def __init__(self, values):
        """values is a list of values in the domain
        This class uses a dictionnary to make sure that there are
        no duplicate values"""
        #assert isinstance(values, dict)
        self._values = values.copy()
        self._changed = False

    def copy(self):
        return BaseFiniteDomain(self._values)
            
    def _value_removed(self):
        "The implementation of remove_value should call this method"
        if self.size() == 0:
            raise ConsistencyError, "tried to make a domain empty"
        
    def remove_value(self, value):
        """Remove value of domain and check for consistency"""
        del self._values[value]
        self._value_removed()
        self._changed = True

    def remove_values(self, values):
        assert isinstance(values, list)
        if len(values) > 0:
            for val in values:
                del self._values[val]
            self._value_removed()
            self._changed = True

    def size(self):
        """computes the size of a finite domain"""
        return len(self._values)
    
    def get_values(self):
        return self._values.keys()


    def __repr__(self):
        return "<Domain %s>" % self._values.keys()

# XXX finish this
class TodoBaseFiniteDomain:
    """
    Variable Domain with a finite set of int values
    """

    def __init__(self, values):
        """values is a list of values in the domain
        This class uses a dictionnary to make sure that there are
        no duplicate values"""
        assert isinstance(values, int)
        self._values = [True] * values

    def copy(self):
        dom = BaseFiniteDomain(len(self._values))
        for i, v in enumerate(self._values):
            dom._values[i] = v

    def _value_removed(self):
        "The implementation of remove_value should call this method"
        if self.size() == 0:
            raise ConsistencyError, "tried to make a domain empty"
        
    def remove_value(self, value):
        """Remove value of domain and check for consistency"""
        assert isinstance(value, int)
        del self._values[value]
        self._value_removed()

    def remove_values(self, values):
        assert isinstance(values, list)
        if len(values) > 0:
            for val in values:
                del self._values[val]
            self._value_removed()

    def size(self):
        """computes the size of a finite domain"""
        return len(self._values)
    
    def get_values(self):
        return self._values.keys()
