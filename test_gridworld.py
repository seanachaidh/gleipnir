#!/usr/bin/env python3

import unittest

import gleipnir
import plotting

class TestGridWorldClass(unittest.TestCase):
    def setUp(self):
        self.grid = gleipnir.GridworldGame(9, 3, 3, 1)
        #Greed does appearantly pay in this game
        #~ self.grid.add_players(gleipnir.PHCPlayer(4, 9, 6), gleipnir.PHCPlayer(4, 9, 8))
        self.grid.add_players(gleipnir.WolfPlayer(4, 9, 4, 0.01, 0.0, 0.035, 0.07), gleipnir.WolfPlayer(4, 9, 0, 0.01, 0.0, 0.035, 0.07))
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
        
    def test_gameplaying(self):
        lengths = []
        for i in range(500):
            retval = self.grid.play_till_the_end()
            print("steps player1:", retval[0])
            print("steps player2:", retval[1])
            lengths.append(len(retval[0]))
            self.grid.player1.state = 6
            self.grid.player2.state = 8

if __name__ == '__main__':
    unittest.main()
