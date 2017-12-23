from random import random, gauss

class QValueEstimate:
    #Look if this is right considering identation
    def add_estimate(self, value, maxval = 0, alpha, gamma):
        self.value = (1 - self.alpha) * self.value + alpha *
            (value + gamma * maxval)
            
    def __init__(self, initial):
        self.value = initial
        
class QValue:
    def __init__(self, mean, stdDev = None):
        self.mean = mean
        self.stdDev = stdDev
    def get_reward(self):
        if stdDev is None:
            return self.mean
        else:
            return gauss(self.mean, self.stdDev)

class Player:
    def __init__(self, actions, states, initialstate = 0, alpha = 1.0, gamma = 0.0):
        self.gamma = gamma
        self.alpha = alpha
        self.state = initialstate
        
        self.probabilities = [[1/actions for _ in range(actions)] for _ in range(states)]
        self.QValueEstimates = [[QValueEstimate(0) for _ in range(actions)] for _ in range(states)]
    
    def select_action(self):
        randnum = random()
        currentProbs = self.probabilities[self.state]
        currentSum = 0
        currentInd = 0
        
        for p in range(len(currentProbs)):
            currentSum += currentProbs[p]
            if currentSum >= randnum:
                return p
    def observe_reward_and_move(self, reward, action, nextState):
        maxNext = max([x for x.value in self.QValueEstimates[nextState]])
        self.QValueEstimates[self.state][action].add_estimate(reward, maxNext, self.alpha, self.gamma)
        
        self.state = nextState
        
    def update_probability(self):
        raise NotImplementedError('You are supposed to implement this method')
        
                
class Game:
    def __init__(self, nstates, nactions):
        self.state = initialstate
        self.nstates = nstates
        self.nactions = nactions
        
        #None here means the agent remains in the same state. Good for single state games
        self.NextStates = [[None for _ in range(actions)] for _ in range(states)]
     
     def add_players(self, player1, player2):
         self.player1 = player1
         self.player2 = player2
        
    def play_game(self):
        if self.player1 is None or self.player2 is None:
            raise RuntimeError('Players not properly set')
        
        action_player1 = player1.select_action()
        action_player2 = player2.select_action()
        
        rewards = (action_player1, player1.state, action_player2, player2.state)
        player1.observe_reward_and_move(rewards[0], action_player1, self.NextStates[action_player1][player1.state])
        player2.observe_reward_and_move(rewards[1], action_player2, self.NextStates[action_player2][player2.state])
        
        
    #Methods to implement. Supposed to return a 2-tuple    
    def get_rewards(action1, state1, action2, state2):
        raise NotImplementedError('You must implement this method')
