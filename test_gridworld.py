#!/usr/bin/env python3

import unittest

import gleipnir
import plotting

class TestGridWorldClass(unittest.TestCase):
    def setUp(self):
        self.grid = gleipnir.GridworldGame(9, 3, 3, 1)
        #Greed does appearantly pay in this game
        #~ self.grid.add_players(gleipnir.PHCPlayer(4, 9, '6|8', alpha=1.0), gleipnir.PHCPlayer(4, 9, '8|6', alpha=1.0))
        self.grid.add_players(gleipnir.WolfPlayer(4, 9, '6|8', 0.4, 0.9, 0.35, 0.7, True), gleipnir.WolfPlayer(4, 9, '8|6', 0.4, 0.9, 0.35, 0.7, True))
        self.grid.wall_off_state(6, 0)
        self.grid.wall_off_state(8, 0)
        self.grid.wall_off_state(3, 2)
        self.grid.wall_off_state(5, 2)
        
    def test_movement(self):
        north = self.grid.calculate_move(4, 0)
        east = self.grid.calculate_move(4, 1)
        south = self.grid.calculate_move(4, 2)
        west = self.grid.calculate_move(4, 3)
        gosouth = self.grid.calculate_move(2, 2)
        
        bounce_wall = self.grid.calculate_move(6, 0)
        
        #testing a bounce
        bounced = self.grid.calculate_move(7, 2)
        
        self.assertEqual(north, 1, 'not in the north')
        self.assertEqual(east, 5, 'not in the east')
        self.assertEqual(south, 7, 'not in the south')
        self.assertEqual(west, 3, 'not in the west')
        self.assertEqual(bounced, 7, 'I did not bounce')
        self.assertEqual(gosouth, 5, 'I did not go south')
        self.assertEqual(bounce_wall, 6, 'I went through a wall')
        
    def test_manhattan(self):
        corner = self.grid.calculate_manhattan(6, 1)
        middle = self.grid.calculate_manhattan(7, 1)
        nextTo = self.grid.calculate_manhattan(2, 1)
        onGoal = self.grid.calculate_manhattan(1, 1)
        
        self.assertEqual(corner, 3, 'Corner not equal')
        self.assertEqual(middle, 2, 'Middle not equal')
        self.assertEqual(nextTo, 1, 'NextTo Not equal')
        self.assertEqual(onGoal, 0, 'Not in the goal')
        
    def test_gameplaying(self):
        lengths = []
        for i in range(500):
            retval = self.grid.play_till_the_end()
            print("steps player1:", retval[0])
            print("steps player2:", retval[1])
            lengths.append(len(retval[0]))
            self.grid.player1.state = '6|8'
            self.grid.player2.state = '8|6'
            
            self.grid.player2.steps = 0
            self.grid.player1.steps = 0
            
            self.grid.player1.C = gleipnir.StateManager(4, lambda x: 0, False)
            self.grid.player2.C = gleipnir.StateManager(4, lambda x: 0, False)
            
        # Creating the plot
        plot = plotting.LinePlot("gridworld game with Wolf", "Amount of games played", "Amount of steps to goal", "gridplot.png")
        plot.append_values("vals", lengths)
        plot.plot()
        
if __name__ == '__main__':
    unittest.main()
