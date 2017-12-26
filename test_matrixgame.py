#!/usr/bin/env python3

import plotting, gleipnir

game = gleipnir.MatrixGame(1, 3)
game.set_qvalue(0,0,0,None)
game.set_qvalue(1,1,0,None)
game.set_qvalue(2,2,0,None)
game.set_qvalue(0,1,-1,None)
game.set_qvalue(1,0,1,None)
game.set_qvalue(2,1,1,None)
game.set_qvalue(1,2,-1,None)
game.set_qvalue(0,2,1,None)
game.set_qvalue(2,0,-1,None)

game.add_players(gleipnir.PHCPlayer(3, 1, 0, 0.2, 0.0, 0.001), gleipnir.PHCPlayer(3, 1, 0, 0.2, 0.0, 0.001))
game.play_n_games(1000)

lineplot = plotting.LinePlot('Action selection probability', 'Probability', 'Games', 'matrixgamephc1.png', True)
lineplot.value_list.append(plotting.PlotElement('action1', game.player1_stats[0]))
lineplot.value_list.append(plotting.PlotElement('action2', game.player1_stats[1]))
lineplot.value_list.append(plotting.PlotElement('action3', game.player1_stats[2]))

lineplot.plot()

lineplot2 = lineplot = plotting.LinePlot('Action selection probability', 'Probability', 'Games', 'matrixgamephc2.png', True)
lineplot2.value_list.append(plotting.PlotElement('action1', game.player2_stats[0]))
lineplot2.value_list.append(plotting.PlotElement('action2', game.player2_stats[1]))
lineplot2.value_list.append(plotting.PlotElement('action3', game.player2_stats[2]))
lineplot2.plot()


wolfgame = gleipnir.MatrixGame(1, 3)
wolfgame.set_qvalue(0,0,0,None)
wolfgame.set_qvalue(1,1,0,None)
wolfgame.set_qvalue(2,2,0,None)
wolfgame.set_qvalue(0,1,-1,None)
wolfgame.set_qvalue(1,0,1,None)
wolfgame.set_qvalue(2,1,1,None)
wolfgame.set_qvalue(1,2,-1,None)
wolfgame.set_qvalue(0,2,1,None)
wolfgame.set_qvalue(2,0,-1,None)

wolfgame.add_players(gleipnir.WolfPlayer(3, 1, 0, 0.2, 0.0, 0.2, 0.4), gleipnir.WolfPlayer(3, 1, 0, 0.2, 0.0, 0.2, 0.4))
wolfgame.play_n_games(10)

wolflineplot = plotting.LinePlot('Action selection probability', 'Probability', 'Games', 'wolf_matrixgamephc1.png', True)
wolflineplot.value_list.append(plotting.PlotElement('action1', wolfgame.player1_stats[0]))
wolflineplot.value_list.append(plotting.PlotElement('action2', wolfgame.player1_stats[1]))
wolflineplot.value_list.append(plotting.PlotElement('action3', wolfgame.player1_stats[2]))
wolflineplot.plot()

wolflineplot2 = plotting.LinePlot('Action selection probability', 'Probability', 'Games', 'wolf_matrixgamephc2.png', True)
wolflineplot2.value_list.append(plotting.PlotElement('action1', wolfgame.player2_stats[0]))
wolflineplot2.value_list.append(plotting.PlotElement('action2', wolfgame.player2_stats[1]))
wolflineplot2.value_list.append(plotting.PlotElement('action3', wolfgame.player2_stats[2]))
wolflineplot2.plot()

#for debugging
print("wolfgame stats action 1")
print(wolfgame.player2_stats[0])
print("wolfgame stats action 2")
print(wolfgame.player2_stats[1])
print("wolfgame stats action 3")
print(wolfgame.player2_stats[2])

