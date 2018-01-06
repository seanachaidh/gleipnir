#!/usr/bin/env python3

import gleipnir
import plotting
import unittest

class TestSoccerGame(unittest.TestCase):
    
    def setUp(self):
        self.voetbal = gleipnir.SoccerGame(25, 4, 5, 5, 12, 2, 22)
        self.voetbal.add_players(gleipnir.WolfPlayer(4, 25, '10|14|12', 0.4, 0.9, 0.35, 0.7, True), gleipnir.PHCPlayer(4, 25, '14|10|12', alpha=1.0))
    
    def test_movement(self):
        north = self.voetbal.calculate_move(12, 0)
        east = self.voetbal.calculate_move(12, 1)
        south = self.voetbal.calculate_move(12, 2)
        west = self.voetbal.calculate_move(12, 3)

        self.assertEqual(north, 7, 'not in the north')
        self.assertEqual(east, 13, 'not in the east')
        self.assertEqual(south, 17, 'not in the south')
        self.assertEqual(west, 11, 'not in the west')

    def test_manhattan(self):
        corner = self.voetbal.calculate_manhattan(6, 1)
        middle = self.voetbal.calculate_manhattan(7, 1)
        nextTo = self.voetbal.calculate_manhattan(2, 1)
        onGoal = self.voetbal.calculate_manhattan(1, 1)
        
        self.assertEqual(middle, 2, 'Middle not equal')
        self.assertEqual(nextTo, 1, 'NextTo Not equal')
        self.assertEqual(onGoal, 0, 'Not in the goal')

    def test_soccer(self):
        wolf_wins = 0
        phc_wins = 0
        
        for x in range(1000):
            winning = self.voetbal.play_till_the_end()
            if winning == 1:
                wolf_wins += 1
            else:
                phc_wins += 1
            
            #Reset the game
            self.voetbal.player1.state = '10|14|12'
            self.voetbal.player2.state = '14|10|12'
            
            self.voetbal.player1.steps = 0
            self.voetbal.player2.steps = 0

            self.voetbal.player1.C = gleipnir.StateManager(4, lambda x: 0, False)
            self.voetbal.player2.C = gleipnir.StateManager(4, lambda x: 0, False)
        print("wins Wolf:", wolf_wins)
        print("Wins PHC:", phc_wins)
        hist = plotting.PercentHistogram('Histogram soccer game', 'game type', 'frequency games won')
        hist.append_values('Wolf', wolf_wins)
        hist.append_values('PHC', phc_wins)
        hist.plot()

if __name__ == '__main__':
    unittest.main()

