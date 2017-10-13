from random import randint

class Map:
    def __init__(self,row = None, col = None, minesNum = None):
        self.row = row
        self.col = col
        self.minesNum = minesNum

    def loadMap(self,filename):
        map = []
        f = open(filename,'r')
        for line in f:
            str = line[:len(line) - 1]
            temp = [ int(c) for c in str]
            map.append(temp)
        return map

    def randomGenerate(self):
        map = [[0 for j in range(self.col)] for i in range(self.row)]
        count = self.minesNum
        while count > 0:
            x = randint(0,self.row-1)
            y = randint(0,self.col-1)
            # this point is a mine, generate a random point again
            if map[x][y] != 0:
                continue
            map[x][y] = 9
            count = count - 1
        for x in range(self.row):
            for y in range(self.col):
                if map[x][y] != 9:
                    for xNei,yNei in self.neighbours((x,y)):
                        if map[xNei][yNei] == 9:
                            map[x][y] = map[x][y] + 1
        return map

    def neighbours(self,point):
        nei = set()
        x,y = point
        for i in range(max(x - 1, 0), min(x + 1, self.row - 1) + 1):
            for j in range(max(y - 1, 0), min(y + 1, self.col - 1) + 1):
                    nei.add((i,j))
        nei.discard((x,y))
        return nei

# unit test
m = Map(5,5,4)
map = m.randomGenerate()
