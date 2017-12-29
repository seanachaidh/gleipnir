#!/usr/bin/env python3

import plotting, gleipnir

def check_correct(action1, action2, action3):
	for i in range(len(action1)):
		if not (action1[i] + action2[i] + action3[i]) == 1:
			print("Incorrect %f", action1[i] + action2[i] + action3[i])

game = gleipnir.MatrixGame(1, 3, randomize = True)
game.set_qvalue(0,0,0,None)
game.set_qvalue(1,1,0,None)
game.set_qvalue(2,2,0,None)
game.set_qvalue(0,1,-1,None)
game.set_qvalue(1,0,1,None)
game.set_qvalue(2,1,1,None)
game.set_qvalue(1,2,-1,None)
game.set_qvalue(0,2,1,None)
game.set_qvalue(2,0,-1,None)

game.add_players(gleipnir.PHCPlayer(3, 1, 0, 1, 0.0, 0.8), gleipnir.PHCPlayer(3, 1, 0, 1, 0.0, 0.8))
game.play_n_games(1000)

lineplot = plotting.LinePlot('Action selection probability', 'Probability', 'Games', 'matrixgamephc1.png', True)
lineplot.append_values('action1', game.player1_stats[0], True)
lineplot.append_values('action2', game.player1_stats[1], True)
lineplot.append_values('action3', game.player1_stats[2], True)

lineplot.plot()

lineplot2 = plotting.LinePlot('Action selection probability', 'Probability', 'Games', 'matrixgamephc2.png', True)
lineplot2.append_values('action1', game.player2_stats[0], True)
lineplot2.append_values('action2', game.player2_stats[1], True)
lineplot2.append_values('action3', game.player2_stats[2], True)
lineplot2.plot()

print(game.player2_stats[0])


wolfgame = gleipnir.MatrixGame(1, 3, randomize = True)
wolfgame.set_qvalue(0,0,0,None)
wolfgame.set_qvalue(1,1,0,None)
wolfgame.set_qvalue(2,2,0,None)
wolfgame.set_qvalue(0,1,-1,None)
wolfgame.set_qvalue(1,0,1,None)
wolfgame.set_qvalue(2,1,1,None)
wolfgame.set_qvalue(1,2,-1,None)
wolfgame.set_qvalue(0,2,1,None)
wolfgame.set_qvalue(2,0,-1,None)

wolfgame.add_players(gleipnir.WolfPlayer(3, 1, 0, 0.0, 0.1, 0.2, 0.4), gleipnir.WolfPlayer(3, 1, 0, 0.0, 0.0, 0.2, 0.4))
wolfgame.play_n_games(1000)

wolflineplot = plotting.LinePlot('Action selection probability', 'Probability', 'Games', 'wolf_matrixgamephc1.png', True)
wolflineplot.value_list.append(plotting.PlotElement('action1', wolfgame.player1_stats[0]))
wolflineplot.value_list.append(plotting.PlotElement('action2', wolfgame.player1_stats[1]))
wolflineplot.value_list.append(plotting.PlotElement('action3', wolfgame.player1_stats[2]))
wolflineplot.plot()

check_correct(wolfgame.player1_stats[0], wolfgame.player1_stats[1], wolfgame.player1_stats[2])

wolflineplot2 = plotting.LinePlot('Action selection probability', 'Probability', 'Games', 'wolf_matrixgamephc2.png', True)
wolflineplot2.value_list.append(plotting.PlotElement('action1', wolfgame.player2_stats[0]))
wolflineplot2.value_list.append(plotting.PlotElement('action2', wolfgame.player2_stats[1]))
wolflineplot2.value_list.append(plotting.PlotElement('action3', wolfgame.player2_stats[2]))
wolflineplot2.plot()

##for debugging
#print("wolfgame stats action 1")
#print(wolfgame.player2_stats[0])
#print("wolfgame stats action 2")
#print(wolfgame.player2_stats[1])
#print("wolfgame stats action 3")
#print(wolfgame.player2_stats[2])

