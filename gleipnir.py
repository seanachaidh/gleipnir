from random import random, gauss, randint

# Classes for actual QValues as well as estimated ones
class QValueEstimate:

    def __init__(self, initial):
        self.value = initial

    #Look if this is right considering identation
    def add_estimate(self, value, maxval = 0, alpha, gamma):
        self.value = (1 - self.alpha) * self.value + alpha * (value + gamma * maxval)

class QValue:
    def __init__(self, mean, stdDev = None):
        self.mean = mean
        self.stdDev = stdDev
    def get_reward(self):
        if stdDev is None:
            return self.mean
        else:
            return gauss(self.mean, self.stdDev)
#--------------------------------------------------

#Classes for managing states
#TODO: Default waardes implementeren rekening houdend met probabilities
class StateManager:
    def __init__(self, nactions):
        self.nactions = nactions
        self.states = dict()
    def get_state(self, state):
        if state in self.states:
            return self.states[state]
        else:
            self.states[state] = [QValueEstimate(0) for _ in range(nactions)]
            return self.states[state]
            
    # Operator overloading of []
    def __getitem__(self, key):
        return self.get_state(key)
#------------------------------------------------------------

#Classes for different types of players
class Player:
    def __init__(self, actions, states, initialstate = 0, alpha = 1.0, gamma = 0.0):
        self.gamma = gamma
        self.alpha = alpha
        self.state = initialstate
        
        self.QValueEstimates = StateManager(actions)

        self.probabilities = [[1/actions for _ in range(actions)] for _ in range(states)]

    def constraint_current_state_probability(self):
        sumProb = sum([x.value for x in self.probabilities[self.state]])
        for a in len(self.probabilities[self.state]):
            self.probabilities[self.state][a] = self.probabilities[self.state][a] / sumProb

    def select_action(self):
        randnum = random()
        currentProbs = self.probabilities[self.state]
        currentSum = 0
        currentInd = 0

        for p in range(len(currentProbs)):
            currentSum += currentProbs[p]
            if currentSum >= randnum:
                return p

    def observe_reward(self, reward, action, nextState):
        maxNext = max([x for x.value in self.QValueEstimates[nextState]])
        self.QValueEstimates[self.state][action].add_estimate(reward, maxNext, self.alpha, self.gamma)

    def move(self, nextState):
        if not nextState is None:
            self.state = nextState

    #The third step in each algorithm
    def update_probability(self, action):
        raise NotImplementedError('You are supposed to implement this method')

class PHCPlayer(Player):
    def __init__(self, actions, states, initialstate = 0, alpha = 1.0, gamma = 0.0, delta):
        super(PHCPlayer, self).__init__(actions, states, initialstate, alpha, gamma) #TODO: Nakijken of ik self aan init moet meegeven
        self.delta = delta

    def update_probability(self, action):
        mystate = self.state
        maxQ = max([x.value for x in QValueEstimates[mystate]])
        currentQ = QValueEstimates[mystate][action].value

        if maxQ == currentQ:
            toadd = self.delta
        else:
            toadd = -self.delta / (len(QValueEstimates[mystate]) - 1)
        self.probabilities[mystate][action] = self.probabilities[mystate][action] + toadd

        self.constraint_current_state_probability()


class WolfPlayer(Player):
    def __init__(self, actions, states, initialstate = 0, alpha = 1.0, gamma = 0.0, w_delta, l_delta):
        super(WolfPlayer, self).__init__(actions, states, initialstate, alpha, gamma)
        self.w_delta = w_delta
        self.l_delta = l_delta
        self.C = [0] * states
        self.average_policy =  [[1/actions for _ in range(actions)] for _ in range(states)]

    #method used to calculate the which delta will be used.
    def calculate_win(state):
        sum_policy_Q_estimate = 0
        sum_average_policy_Q_estimate = 0

        for action in range(len(self.probabilities[state])):
            sum_policy_Q_estimate = sum_policy_Q_estimate + (self.probabilities[state][action] * QValueEstimates[state][action].value)

        for action in range(len(self.average_policy[state])):
            sum_average_policy_Q_estimate = sum_average_policy_Q_estimate + (self.average_policy[state][action] * QValueEstimates[state][action].value)

        if (sum_policy_Q_estimate > sum_average_policy_Q_estimate):
            return True
        else:
            return False

    def update_probability(self, action):
        mystate = self.state
        maxQ = max([x.value for x in QValueEstimates[mystate]])
        currentQ = QValueEstimates[mystate][action].value

        self.c[mystate] = self.c[mystate] + 1

        for action in range(len(self.average_policy[mystate])):
            self.average_policy[mystate][action] = self.average_policy[mystate][action] + ((1/self.c[mystate])*(self.probabilities[mystate][action] - self.average_policy[mystate][action]))

        if(calculate_win(mystate) == true):
            self.delta = self.w_delta
        else:
            self.delta = self.l_delta

        if maxQ == currentQ:
            toadd = self.delta
        else:
            toadd = -self.delta / (len(QValueEstimates[mystate]) - 1)
        self.probabilities[mystate][action] = self.probabilities[mystate][action] + toadd

        self.constraint_current_state_probability()

#----------------------------------------------------------------------

# Classes for different types of games

class Game:
    def __init__(self, nstates, nactions):
        self.nstates = nstates
        self.nactions = nactions

        #None here means the agent remains in the same state. Good for single state games
        self.NextStates = [[None for _ in range(actions)] for _ in range(states)]
    
    # Supposed to return a tuple. Each element represents the next state of the player
    def next_states(self, player1_state, player1_action, player2_state, player2_action):
        raise NotImplementedError('You must implement this method')
    
    def add_players(self, player1, player2):
         self.player1 = player1
         self.player2 = player2

    def is_same_future_state(state_player_1, state_player_2):
        raise NotImplementedError('You must implement this method')

    def play_game(self):
        if self.player1 is None or self.player2 is None:
            raise RuntimeError('Players not properly set')

        action_player1 = player1.select_action()
        action_player2 = player2.select_action()
        
        p1_next, p2_next = self.next_states(player1.state, action_player1, player2.state, action_player2)
        
        #The wile loop is used for the Gridworld game. In case the future states are the same, a different action should be chosen.
        while is_same_future_state(p1_next, p2_next):
            action_player1 = player1.select_action()
            action_player2 = player2.select_action()

        rewards = (action_player1, player1.state, action_player2, player2.state)
        player1.observe_reward(rewards[0], action_player1, p1_next)
        player2.observe_reward(rewards[1], action_player2, p2_next)

        player1.update_probability()
        player2.update_probability()

        player1.move(p1_next)
        player2.move(p2_next)

    #Methods to implement. Supposed to return a 2-tuple
    #One for each player corresponding to an element
    def get_rewards(self, action1, state1, action2, state2):
        raise NotImplementedError('You must implement this method')

class MatrixGame(Game):
    def __init__(self, nstates, nactions):
        super(MatrixGame, self).__init__(nstates, nactions)
        self.QMatrix = [[QValue(0, 1) for _ in range(naction)] for _ in range(nstates)]
    
    def next_states(self, player1_state, player1_action, player2_state, player2_action):
        return (None, None)

    #There is no difference in states, we can just skip the while loop.
    def is_same_future_state(state_player_1, state_player_2):
        return False

    def set_qvalue(self, state, action, mean, stdDev):
        self.QMatrix[state][action] = QValue(mean, stdDev)

    def get_rewards(self, action1, state1, action2, state2):
        rew1 = QMatrix[state1][action1].get_reward()
        rew2 = QMatrix[state2][action2].get_reward()

        # Return the tuple
        return (rew1, rew2)

#-----------------------------------------------------------------------


class GridworldGame(Game):
    def __init__(self, nstates, nactions):
        super(GridworldGame, self).__init__(nstates, nactions)
        self.QMatrix = [[QValue(0, 1) for _ in range(naction)] for _ in range(nstates)]

    def set_qvalue(self, state, action, mean, stdDev):
        self.QMatrix[state][action] = QValue(mean, stdDev)
    
    def calculate_move(self, state, action):
        if action == 0:
            if state < self.nactons:
                retval = state # If you cannot move up anymore, stay there
            else:
                retval = state - (self.nactions - 1)
        else if action == 1:
            if (player1_state - (self.nactions - 1)) % self.nactions == 0:
                retval = state
            else:
                retval = state + 1
        else if action == 2:
            if state >= (self.nstates - self.nactions):
                retval = state
            else:
                retval = state + self.nactions
        return retval

    def next_states(self, player1_state, player1_action, player2_state, player2_action):
        s1 = self.calculate_move(player1_state, player1_action)
        s2 = self.calculate_move(player2_state, player2_action)
        return (s1, s2)

    def is_same_future_state(state_player_1, state_player_2):
        if (state_player_1 == state_player_2):
            return True
        else:
            return False

    def get_rewards(self, action1, state1, action2, state2):
        rew1 = QMatrix[state1][action1].get_reward()
        rew2 = QMatrix[state2][action2].get_reward()

        # Return the tuple
        return (rew1, rew2)

# TODO: FAILURE IMPLEMENTEREN
# State Format: ownstate|otherstate|stateb
class SoccerGame(Game):
    
    def state_to_coordinate(self,state):
        x = state - 1 // self.rows
        y = state - 1 % self.columns
        
        return (x + 1, y + 1)
        
    # CODE DUPLICATION!!!!!    
    def calculate_move(self, state, action):
        if action == 0:
            if state < self.nactons:
                retval = state # If you cannot move up anymore, stay there
            else:
                retval = state - (self.nactions - 1)
        else if action == 1:
            if (player1_state - (self.nactions - 1)) % self.nactions == 0:
                retval = state
            else:
                retval = state + 1
        else if action == 2:
            if state >= (self.nstates - self.nactions):
                retval = state
            else:
                retval = state + self.nactions
        return retval
        
    def next_states(self, player1_state, player1_action, player2_state, player2_action):
        currentP1State = int(player1_state.split('|')[0])
        currentP2State = int(player2_state.split('|')[0])
        
        # The ball should be for both players in the same spot
        # so it does not matter from which player we take it$
        currentBallState = player1_sate.split('|')[2]
        
        movedP1 = self.calculate_move(currentP1State)
        movedP2 = self.calculate_move(currentP2State)
        
        # Move the ball
        if currentP1State == currentBallState:
            movedBall = movedP1
        else if currentP2State == currentBallState:
            movedBall = movedP2
        else:
            movedBall = currentBallState
        
        # If player1 player2 and the ball are on the same location
        # One of them gets the ball
        if movedBall == movedP1 == movedP2:
            # The losing player moves back
            choice = random()
            if choice < 0.5:
                movedP1 = currentP1State
            else:
                movedP2 = currentP2State
        finalP1 = str(movedP1) + '|' + str(movedP2) + '|' + str(movedBall)
        finalP2 = str(movedP2) + '|' + str(movedP1) + '|' + str(movedBall)
        
        return (finalP1, finalP2)
    
    def calculate_manhattan(self, statex, statey):
        location_x = state_to_coordinate(statex)
        location_y = state_to_coordinate(statey)
        
        return abs(location_x[0] - location_y[0]) + abs(location_x[1] - location_y[1])
    
    # Initball is a state
    def __init__(self, states, actions, rows, columns, initball, player1Goal, player2Goal):
        super(SoccerGame, self).__init__(states,actions)
        self.rows = rows
        self.columns = columns
        self.ball_location = initball
        self.player1_goal = player1Goal
        self.player2_goal = player2Goal
    
    def get_rewards(self, action1, state1, action2, state2):
        player1NextState = self.NextStates[state1][action1]
        player2NextState = self.NextStates[state2][action2]
        
        player1HasBall = (state1 == self.ball_location)
        player2HasBall = (state2 == self.ball_location)
        
        if player1HasBall:
            rew1 = self.calculate_manhattan(self.player2_goal, player1NextState)
            #move the ball with the player
            self.ball_location = player1NextState
        else:
            rew1 = self.calculate_manhattan(self.ball_location, player1NextState)
        
        if player2HasBall:
            rew2 = self.calculate_manhattan(self.player1_goal, player2NextState)
            #Move the ball with the player
            self.ball_location = player2NextState
        else:
            rew2 = self.calculate_manhattan(self.ball_location, player2NextState)
        
        return (rew1, rew2)
        
#-----------------------------------------------------------------------
