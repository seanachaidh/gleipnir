from random import random, gauss, randint
from operator import itemgetter

# Classes for actual QValues as well as estimated ones
class QValueEstimate:

    def __init__(self, initial):
        self.value = initial

    #Look if this is right considering identation
    def add_estimate(self, value, maxval = 0, alpha = 1.0, gamma = 0.0):
        self.value = (1 - alpha) * self.value + alpha * (value + gamma * maxval)
        
    def __repr__(self):
        return str(self.value)

class QValue:
    def __init__(self, mean, stdDev = None):
        self.mean = mean
        self.stdDev = stdDev
    def get_reward(self):
        if self.stdDev is None:
            return self.mean
        else:
            return gauss(self.mean, self.stdDev)
#--------------------------------------------------

#Classes for managing states
class StateManager:
    def __init__(self, nactions, initfunc, statesAreLists = True):
        self.nactions = nactions
        self.states = dict()
        self.initfunc = initfunc
        self.statesAreLists = statesAreLists
    def get_state(self, state):
        if state in self.states:
            return self.states[state]
        else:
            #~ print("initializing state")
            if self.statesAreLists:
                self.states[state] = [self.initfunc(self.nactions) for a in range(self.nactions)]
            else:
                self.states[state] = self.initfunc(self.nactions)
            return self.states[state]
            
    # Operator overloading of []
    def __getitem__(self, key):
        return self.get_state(key)
    def __setitem__(self, key, value):
        self.states[key] = value
#------------------------------------------------------------

#Classes for different types of players
class Player:
    def __init__(self, actions, states, initialstate = 0, alpha = 1.0, gamma = 0.0):
        self.gamma = gamma
        self.alpha = alpha
        self.state = initialstate
        self.steps = 0
        self.actions = actions
        
        self.QValueEstimates = StateManager(actions, lambda x: QValueEstimate(0))
        self.probabilities = StateManager(actions, lambda x: 1/x)

    def record_statistics(self):
        pass
    
    def __lower_upper_limit(self, x, low, high):
        if x < low:
            return low
        elif x > high:
            return high
        else:
            return x
    
    def constraint_current_state_probability(self, added_value, chosen_action):
        oldprob = self.probabilities[self.state][chosen_action]
        other_actions = [x for x in range(self.actions) if x != chosen_action]
        newprob = self.__lower_upper_limit(oldprob + added_value, 0, 1)
        diffprob = oldprob - newprob
        toadd_to_others = diffprob / len(other_actions)
        self.probabilities[self.state][chosen_action] = newprob
        
        for a in other_actions:
            self.probabilities[self.state][a] = self.__lower_upper_limit(self.probabilities[self.state][a] + toadd_to_others , 0, 1)

    def select_action(self):
        randnum = random()
        elementPr = [(a, self.probabilities[self.state][a]) for a in range(len(self.probabilities[self.state]))]
        currentProbs = sorted(elementPr, key=itemgetter(1))
        currentSum = 0
        print("probabilities:", elementPr)
        print("QValues:", [x.value for x in self.QValueEstimates[self.state]])
        for p in range(len(currentProbs)):
            currentSum += currentProbs[p][1]
            if currentSum >= randnum:
                print("selected action:", currentProbs[p][0])
                return currentProbs[p][0]

    def observe_reward(self, reward, action, nextState):
        maxNext = max([x.value for x in self.QValueEstimates[nextState]])
        self.QValueEstimates[self.state][action].add_estimate(reward, maxNext, self.alpha, pow(self.gamma, self.steps))

    def move(self, nextState):
        if not nextState is None:
            self.state = nextState

    #The third step in each algorithm
    def update_probability(self, action):
        raise NotImplementedError('You are supposed to implement this method')

class PHCPlayer(Player):
    def __init__(self, actions, states, initialstate = 0, alpha = 1.0, gamma = 0.0, delta = 0.2):
        super(PHCPlayer, self).__init__(actions, states, initialstate, alpha, gamma) #TODO: Nakijken of ik self aan init moet meegeven
        self.delta = delta

    def update_probability(self, action):
        mystate = self.state
        maxQ = max([x.value for x in self.QValueEstimates[mystate]])
        currentQ = self.QValueEstimates[mystate][action].value

        if maxQ == currentQ:
            toadd = self.delta
        else:
            toadd = -self.delta / (len(self.QValueEstimates[mystate]) - 1)
        self.probabilities[mystate][action] = self.probabilities[mystate][action] + toadd

        self.constraint_current_state_probability(toadd, action)


class WolfPlayer(Player):
    def __init__(self, actions, states, initialstate = 0, alpha = 1.0, gamma = 0.0, w_delta = 0.2, l_delta = 0.4):
        super(WolfPlayer, self).__init__(actions, states, initialstate, alpha, gamma)
        self.w_delta = w_delta
        self.l_delta = l_delta
        self.C = StateManager(actions, lambda x: 0, False)
        
        #self.average_policy =  [[1/actions for _ in range(actions)] for _ in range(states)]
        self.average_policy = StateManager(actions, lambda x: 1/x)

    #method used to calculate the which delta will be used.
    def calculate_win(self,state):
        sum_policy_Q_estimate = 0
        sum_average_policy_Q_estimate = 0

        for action in range(len(self.probabilities[state])):
            sum_policy_Q_estimate = sum_policy_Q_estimate + (self.probabilities[state][action] * self.QValueEstimates[state][action].value)

        for action in range(len(self.average_policy[state])):
            sum_average_policy_Q_estimate = sum_average_policy_Q_estimate + (self.average_policy[state][action] * self.QValueEstimates[state][action].value)

        if (sum_policy_Q_estimate > sum_average_policy_Q_estimate):
            return True
        else:
            return False
    
    def __check_average_policy(self, state):
        tocheck = sum(self.average_policy[self.state][a] for a in range(len(self.average_policy[self.state])))
        print("sum policy:", tocheck)
        print("Average policy:", self.average_policy[self.state])

    def __lower_upper_limit(self, x, low, high):
        if x < low:
            return low
        elif x > high:
            return  high
        else:
            return x
        
    def __constraint_average_policy(self, added_value, chosen_action):
        #~ sumprob = sum(self.__lower_limit(self.average_policy[self.state][a], 0) for a in range(len(self.average_policy[self.state])))
        #~ for a in range(len(self.average_policy[self.state])):
            #~ self.average_policy[self.state][a] = self.__lower_limit(self.average_policy[self.state][a],0)/sumprob

        oldprob = self.average_policy[self.state][chosen_action]
        other_actions = [x for x in range(self.actions) if x != chosen_action]
        newprob = self.__lower_upper_limit(oldprob + added_value, 0, 1)
        diffprob = oldprob-newprob
        toadd_to_others = diffprob / len(other_actions)
        self.average_policy[self.state][chosen_action] = newprob
        
        for a in other_actions:
            self.average_policy[self.state][a] = self.average_policy[self.state][a] + toadd_to_others
    
    def update_probability(self, action):
        mystate = self.state
        maxQ = max([x.value for x in self.QValueEstimates[mystate]])
        currentQ = self.QValueEstimates[mystate][action].value
        
        tmpvar = self.C[mystate]
        
        self.C[mystate] = tmpvar + 1

        for a in range(len(self.average_policy[mystate])):
            #~ self.average_policy[mystate][a] = self.average_policy[mystate][a] + ((1/self.C[mystate])*(self.probabilities[mystate][a] - self.average_policy[mystate][a]))
            self.__constraint_average_policy(((1/self.C[mystate])*(self.probabilities[mystate][a] - self.average_policy[mystate][a])), a)
        #self.__check_average_policy(mystate)

        if(self.calculate_win(mystate) == True):
            print("winning")
            curdelt = self.w_delta
        else:
            print("losing")
            curdelt = self.l_delta

        if maxQ == currentQ:
            toadd = curdelt
        else:
            toadd = -curdelt / (len(self.QValueEstimates[mystate]) - 1)
        print("adding:", toadd)
        #~ self.probabilities[mystate][action] = self.probabilities[mystate][action] + (toadd*(1/self.C[mystate]))
        #~ self.probabilities[mystate][action] = self.probabilities[mystate][action] + toadd
        self.constraint_current_state_probability(toadd, action)

#----------------------------------------------------------------------

# Classes for different types of games

class Game:
    def __init__(self, nstates, nactions, randomize = False):
        self.nstates = nstates
        self.nactions = nactions
        
        self.randomize = randomize
        
        #None here means the agent remains in the same state. Good for single state games
        self.NextStates = [[None for _ in range(nactions)] for _ in range(nstates)]
    
    def record_statistics(self):
        pass
    
    # Supposed to return a tuple. Each element represents the next state of the player
    def next_states(self, player1_state, player1_action, player2_state, player2_action):
        raise NotImplementedError('You must implement this method')
    
    def add_players(self, player1, player2):
         self.player1 = player1
         self.player2 = player2

    def is_same_future_state(self, state_player_1, state_player_2):
        raise NotImplementedError('You must implement this method')


    def play_game(self):
        if self.player1 is None or self.player2 is None:
            raise RuntimeError('Players not properly set')
            
        #Record some stats
        self.player1.record_statistics()
        self.player2.record_statistics()
        self.record_statistics()

        action_player1 = self.player1.select_action()
        if self.randomize:
            action_player2 = randint(0, self.nactions-1)
        else:
            action_player2 = self.player2.select_action()
        
        p1_next, p2_next = self.next_states(self.player1.state, action_player1, self.player2.state, action_player2)
        
        #The wile loop is used for the Gridworld game. In case the future states are the same, a different action should be chosen.
        while self.is_same_future_state(p1_next, p2_next):
            print("same")
            #~ print('current state player1:', self.player1.state)
            #~ print('current state player2:', self.player2.state)
            action_player1 = self.player1.select_action()
            action_player2 = self.player2.select_action()
            p1_next, p2_next = self.next_states(self.player1.state, action_player1, self.player2.state, action_player2)

        rewards = self.get_rewards(action_player1, self.player1.state, action_player2, self.player2.state)
        self.player1.observe_reward(rewards[0], action_player1, p1_next)
        self.player2.observe_reward(rewards[1], action_player2, p2_next)

        self.player1.update_probability(action_player1)
        self.player2.update_probability(action_player2)

        self.player1.move(p1_next)
        self.player2.move(p2_next)
        
        self.player1.steps+= 1
        self.player2.steps+= 1
        
        print('current state player1:', self.player1.state)
        print('current state player2:', self.player2.state)
        
    #Methods to implement. Supposed to return a 2-tuple
    #One for each player corresponding to an element
    def get_rewards(self, action1, state1, action2, state2):
        raise NotImplementedError('You must implement this method')
        
    def play_n_games(self, n):
        for _ in range(n):
            self.play_game()

class MatrixGame(Game):
    def __init__(self, nstates, nactions, randomize = False):
        super(MatrixGame, self).__init__(nstates, nactions, randomize)
        self.QMatrix = [[QValue(0, 1) for _ in range(nactions)] for _ in range(nactions)]
        
        self.player1_stats = [list() for _ in range(nactions)]
        self.player2_stats = [list() for _ in range(nactions)]
        
    def record_statistics(self):
        for a in range(len(self.player1.probabilities[self.player1.state])):
            self.player1_stats[a].append(self.player1.probabilities[self.player1.state][a])
        for a in range(len(self.player2.probabilities[self.player2.state])):
            self.player2_stats[a].append(self.player2.probabilities[self.player2.state][a])        
    
    def next_states(self, player1_state, player1_action, player2_state, player2_action):
        return (0, 0)

    #There is no difference in states, we can just skip the while loop.
    def is_same_future_state(self, state_player_1, state_player_2):
        return False

    def set_qvalue(self, action1, action2, mean, stdDev):
        self.QMatrix[action1][action2] = QValue(mean, stdDev)

    def get_rewards(self, action1, state1, action2, state2):
        rew1 = self.QMatrix[action1][action2].get_reward()
        # Return the tuple. Player two always gets the oposite reward
        return (rew1, -rew1)

#-----------------------------------------------------------------------


class GridworldGame(Game):
    def __init__(self, nstates, rows, columns, goal):
        super(GridworldGame, self).__init__(nstates, 4, False)
        self.goal = goal
        self.columns = columns
        self.rows = rows
        self.walls = [[False] * 4 for _ in range(nstates)]
    
    def state_to_coordinate(self,state):
        x = state // self.rows
        y = state % self.columns
        
        return (x + 1, y + 1)
        
    
    def wall_off_state(self, state, action):
        self.walls[state][action] = True
    
    # TODO: ENORMOUS CODE DUPLICATION!!!
    def calculate_manhattan(self, statex, statey):
        location_x = self.state_to_coordinate(statex)
        location_y = self.state_to_coordinate(statey)
        
        return abs(location_x[0] - location_y[0]) + abs(location_x[1] - location_y[1])
    
    def calculate_move(self, state, action):
        if action == 0:
            if state < self.columns or self.walls[state][0]:
                retval = state # If you cannot move up anymore, stay there
            else:
                retval = state - self.columns
        elif action == 1 or self.walls[state][1]:
            if (state - (self.columns - 1)) % self.columns == 0:
                retval = state
            else:
                retval = state + 1
        elif action == 2 or self.walls[state][2]:
            if state >= (self.nstates - self.columns):
                retval = state
            else:
                retval = state + self.columns
        elif action == 3 or self.walls[state][3]:
            if (state % self.columns) == 0:
                retval = state
            else:
                retval = state - 1
        return retval

    def next_states(self, player1_state, player1_action, player2_state, player2_action):
        # Lock the player in the "none" state if it is there
        # Put the player in the "none" state if he reached the goal
        
        tmp1 = int(player1_state.split('|')[0])
        tmp2 = int(player1_state.split('|')[1])
        m1 = self.calculate_move(tmp1, player1_action)
        m2 = self.calculate_move(tmp2, player2_action)
        
        if m1 == m2:
            s1 = tmp1
            s2 = tmp2
        else:
            if tmp1 == -1:
                s1 = -1
            else:
                s1 = self.calculate_move(tmp1, player1_action)
                if s1 == self.goal:
                    s1 = -1
            if tmp2 == -1:
                s2 = -1
            else:
                s2 = self.calculate_move(tmp2, player2_action)
                if s2 == self.goal:
                    s2 = -1
        return (str(s1) + '|' + str(s2), str(s2) + '|' + str(s1))

    def is_same_future_state(self, state_player_1, state_player_2):
        s1 = int(state_player_1.split('|')[0])
        s2 = int(state_player_1.split('|')[1])
        
        if (s1 == -1) and (s2 == -1):
            return False
        elif (s1 == s2):
            return True
        else:
            return False


    def calculate_reward(self, state, new_state):
        manhattan_old = self.calculate_manhattan(state, self.goal)
        manhattan_new = self.calculate_manhattan(new_state, self.goal)
        
        if new_state == -1:
            return 100 #Extra duwtje in de rug
        elif manhattan_new < manhattan_old:
            return 1
        elif manhattan_new == manhattan_old:
            return -1
        else:
            return -2
        #~ moved_state = self.calculate_move(state, action)
        #~ if moved_state == self.goal:
            #~ return 100
        #~ else:
            #~ return 0
    
    def get_rewards(self, action1, state1, action2, state2):
        s1 = int(state1.split('|')[0])
        s2 = int(state1.split('|')[1])
        
        nextstates = self.next_states(state1, action1, state2, action2)[0].split('|')
        
        
        rew1 = self.calculate_reward(s1, int(nextstates[0]))
        rew2 = self.calculate_reward(s2, int(nextstates[1]))
 
        # Return the tuple
        return (rew1, rew2)
        
    def play_till_the_end(self):
        player1_steps = []
        player2_steps = []
        
        while not (self.player1.state == '-1|-1'):
            self.play_game()
            s1 = int(self.player1.state.split('|')[0])
            s2 = int(self.player1.state.split('|')[1])
            
            player1_steps.append(s1)
            player2_steps.append(s2)
        return (player1_steps, player2_steps)

# State Format: ownstate|otherstate|stateb
class SoccerGame(Game):
    
    def is_same_future_state(self, state_player1, state_player2):
        return False
    
    def state_to_coordinate(self,state):
        x = state - 1 // self.rows
        y = state - 1 % self.columns
        
        return (x + 1, y + 1)
        
    # CODE DUPLICATION!!!!!    
    def calculate_move(self, state, action):
        if action == 0:
            if state < self.columns:
                retval = state # If you cannot move up anymore, stay there
            else:
                retval = state - self.columns
        elif action == 1:
            if (player1_state - (self.columns - 1)) % self.columns == 0:
                retval = state
            else:
                retval = state + 1
        elif action == 2:
            if state >= (self.nstates - self.columns):
                retval = state
            else:
                retval = state + self.columns
        elif action == 3:
            if (state % self.columns) == 0:
                retval = state
            else:
                retval = state - 1
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
        elif currentP2State == currentBallState:
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
        super(SoccerGame, self).__init__(states,actions, False)
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

