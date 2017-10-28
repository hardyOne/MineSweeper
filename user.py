from agent import Agent
from time import sleep
from generateMap import Map
from random import random
import logging
logging.basicConfig(level=logging.INFO)


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
            logging.debug('You have detected all squares! Congratulations!')
            logging.debug('you have detected  mines'.format(len(self.agent.mines)))
            logging.debug('mines: {}'.format( self.agent.mines))
            return 'SUCCESS'
        # case 1: have detected all squares but not mark all the mines correctly
        if len(self.agent.visited) == self.row * self.col and self.mines != self.agent.mines:
            logging.debug('you have walked {} steps'.format(len(self.agent.visited)))
            # logging.debug('you have detected {} mines rightly, but you have marked {} as mine wrongly'.format(len(self.agent.mines.intersection(self.mines))),len(self.agent.mines-self.mines))
            return 'FAILURE'
        # case 2: click the mine => failure
        if self.map[x][y] == 9:
            logging.debug('{} is a mine'.format(point))
            logging.debug('you have walked {} steps'.format(len(self.agent.visited)))
            logging.debug('you have detected {} mines rightly, but you have marked {} as mine wrongly'.format(len(self.agent.mines.intersection(self.mines)),self.agent.mines-self.mines))
            return 'FAILURE'
        # update agent's clues
        # But I don't want to give the agent the clue number
        p = random()
        if p <= 1:
            self.agent.updateClues(point, self.map[x][y])
        else:
            logging.debug('You clicked point {},but I do not want to tell you the clue number.'.format(point))

    def play(self):
        while True:
            point = self.agent.nextClick()
            res = self.result(point)
            if res == 'SUCCESS' or res == 'FAILURE':
                logging.debug(res)
                return res

# unit test
count = 0
total = 0
while True:
    map = Map(20,20,0.10)
    user = User(map.randomGenerate())
    res = user.play()
    # if calculate general success rate, the line below can be commented
    if user.map[user.agent.sequence[0][0]][user.agent.sequence[0][1]] == 0:
        total += 1
        if(res == 'SUCCESS'):
            count += 1
    if total >= 100:
        break
logging.info('success rate: {}'.format(count/total))


