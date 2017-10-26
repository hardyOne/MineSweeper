from agent import Agent
from time import sleep
from generateMap import Map
from random import random


class User:
    def __init__(self, map):
        self.map = map
        self.row = len(map)
        self.col = len(map[0])
        self.mines = set()
        self.agent = Agent(self.row, self.col, self)
        # store all mines' coordinates
        for i in range(self.row):
            for j in range(self.col):
                if map[i][j] == 9:
                    self.mines.add((i, j))
        # Let the agent know how many mines there are in the map
        self.agent.numberOfMinesFromUser = len(self.mines)

    def result(self, point):
        x, y = point
        # terminate conditions
        # case 1: have detected all squares and has marked all the mines correctly
        if len(self.agent.visited) == self.row * self.col and self.mines == self.agent.mines:
            print('You have detected all squares! Congratulations!')
            print('you have detected', len(self.agent.mines), ' mines')
            print('mines:', self.agent.mines)
            return 'SUCCESS'
        # case 1: have detected all squares but not mark all the mines correctly
        if len(self.agent.visited) == self.row * self.col and self.mines != self.agent.mines:
            print('you have walked', len(self.agent.visited), 'steps')
            print('you have detected',len(self.agent.mines.intersection(self.mines)),' mines rightly, but you have marked', self.agent.mines-self.mines,'as mine wrongly')
            return 'FAILURE'
        # case 2: click the mine => failure
        if self.map[x][y] == 9:
            print(point, ' is a mine')
            print('you have walked', len(self.agent.visited), 'steps')
            print('you have detected',len(self.agent.mines.intersection(self.mines)),' mines rightly, but you have marked', self.agent.mines-self.mines,'as mine wrongly')
            return 'FAILURE'
        # update agent's clues
        # But I don't want to give the agent the clue number
        p = random()
        if p <= 1:
            self.agent.updateClues(point, self.map[x][y])
        else:
            print('You clicked point',point, ',but I do not want to tell you the clue number.')

    def play(self):
        while True:
            point = self.agent.nextClick()
            res = self.result(point)
            if res == 'SUCCESS' or res == 'FAILURE':
                print(res)
                break

# unit test
map = Map(30,30,0.15)
user = User(map.randomGenerate())
user.play()