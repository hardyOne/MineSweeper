from agent import Agent
from time import sleep


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
        self.agent.updateClues(point, self.map[x][y])

# unit test
# map = loadMap('example.txt')
# user = User(map)
