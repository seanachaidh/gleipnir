class QValue:

    def add_estimate(self, value):
        pass
    
    def __init__(self, initial):
        self.value = initial
        pass

class Player:
    _Believes = [1,1,1]
    def __init__(self):
        pass
    

class State:
    def __init__(self, nactons):
        self.nactions = nactions
        self.probabilities = [1/nactions] * nactions

class Game:
    def __init__(self):
        pass
        
    def select_action(self):
        pass
    def observe_and_update(self, action):
        pass
    
    #Methods to inherit
    def update_probability(self):
        pass
    
