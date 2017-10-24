from random import randint


class Agent:
    def __init__(self, row, col, user):
        self.row = row
        self.col = col
        # set of all detected clues: undetected 0-square and non-0 squares
        self.clues = dict()
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.clues[(i, j)] = dict(
                    [('neighbours', set()), ('mines', set()), ('number', 10), ('priority', 10), ('isMine', False)])
                # add neighbours
                self.clues[(i, j)]['neighbours'] = self.allNeighbours((i, j))
        # set of all detected mines
        self.mines = set()
        # set of all detected squares： clicked squares and marked mines
        self.visited = set()
        self.unvisited = set()
        for i in range(self.row):
            for j in range(self.col):
                self.unvisited.add((i, j))
        # set of safe and unvisited squares
        self.safe = set()
        # first first click
        self.isFirst = True
        # for random operation
        self.randomPercentage = 0.35
        # the sequence of click or mark
        self.sequence = []
        # use rule 5
        self.rule5 = False

    def mark(self, point):
        # point is in mines
        if point in self.mines:
            return
        self.sequence.append(point)
        print('mark', point, 'as a mine', len(self.mines))
        self.clues[point]['isMine'] = True
        # add this point to mines and visited set
        self.mines.add(point)
        self.visited.add(point)
        # delete this point in unvisited
        self.unvisited.discard(point)
        for nei in self.allNeighbours(point):
            if nei not in self.clues:
                continue
            self.updateNeighbours(nei)
            self.updateMinesNeighbours(nei)
            # check mine's neighbours, denote them as N, if N's number is equal to length of mines around them,
            # then we can make sure that all N's undecteced neighbours are safe
            if len(self.clues[nei]['mines']) == self.clues[nei]['number']:
                for neiNei in self.allNeighbours(nei):
                    if neiNei in self.unvisited:
                        self.safe.add(neiNei)

    def nextClick(self):
        # exist safe squares
        if len(self.safe) != 0:
            self.rule5 = False
            for point in self.safe:
                self.sequence.append(point)
                return point
        # no safe squares left
        # use rule 5
        self.rule5 = True
        # case 1: mark mines to find safe squares
        # we try as we can to mark some square as mines
        for p in dict(self.clues):
            self.updateClues(p)
        # try another times to see if there exists a safe square
        if len(self.safe) != 0:
            for point in self.safe:
                self.sequence.append(point)
                return point
        # no safe squares. oops!!
        rPoint = self.randomOperation()
        self.sequence.append(rPoint)
        return rPoint

    def randomOperation(self):

        # before random, we should check if the map is valid
        # ----------
        # the logic to check if map is valid
        # ----------

        # and for random, we have two strategies.
        # 1, we click squares outside the clue
        # 2, we mark squares near the clue
        visitedPercentage = len(self.visited) / (self.row * self.col)
        listUnvisited = list(self.unvisited)
        # click squares outside the clues randomly
        if visitedPercentage < self.randomPercentage:
            count = 3  # try given times at most
            while count >= 0:
                count = count - 1
                flag = True
                rNum = randint(0, len(listUnvisited) - 1)
                for nei in self.allNeighbours(listUnvisited[rNum]):
                    if nei in self.visited:
                        flag = False
                        break
                if flag:
                    print(visitedPercentage, listUnvisited[rNum])
                    return listUnvisited[rNum]

                    # but if we can't find this type of point in given times?
                    # my idea is let it go, randomly give a square to click
                    # ----------
                    # what should we do?
                    # ----------

        # mark a square near clues and do a update operation
        else:
            nextMark = None
            pri = 0
            cmp = set()
            count = 0
            for point in self.unvisited:
                count = 0
                for nei in self.allNeighbours(point):
                    if nei in self.clues and self.clues[nei]['number'] >= 1 and self.clues[nei]['number'] <= 8:
                        count = count + 1
                cmp.add((point, count))
            for point, count in cmp:
                if count > pri:
                    pri = count
                    nextMark = point
            if nextMark != None:
                print('Uncertain: Through sound analysis, I decide mark', nextMark, 'as a mine')
                self.mark(nextMark)
                # try another time
                return self.nextClick()
        # choose a random square to click
        # why sometimes this will create a bug saying randint(0 ,0)
        # maybe in the last stage, we mark all left undetected squares as mines
        # so the agent should let the user know this condition
        listUnvisited = list(self.unvisited)
        if len(listUnvisited) == 0:
            return (-1, -1)  # this point is meaningless
        rNum = randint(0, len(listUnvisited) - 1)
        print('Finally rendomly generated', listUnvisited[rNum])
        return listUnvisited[rNum]

    def updateClues(self, point, number=None):
        # still exist safe squares
        # click to update, called by user's result() function
        if number != None:
            self.clues[point]['number'] = number
            self.visited.add(point)
            self.unvisited.discard(point)
            self.safe.discard(point)
        # when no safe squares exist
        # update by agent itself
        else:
            number = self.clues[point]['number']
        # before comparing, make sure that this point's neighbours and mines have been updated
        self.updateNeighbours(point)
        lenOfNeis = len(self.clues[point]['neighbours'])
        lenOfMines = len(self.clues[point]['mines'])
        # case 1: this point's number = len(mines)
        # all its left neighbours are safe clues, add them to safe set
        if number == lenOfMines:
            # print('number == lenOfMines', point)
            for nei in self.allNeighbours(point):
                if nei in self.clues and nei in self.unvisited:
                    # add nei to safe set
                    self.safe.add(nei)
                    # self.updateNeighbours(nei)
            # this clue has been used up, so delete it
            self.clues.pop(point)

        # case 2: this point's number = undetected neighbours + detected mines
        # mark its all neighbours as mines
        elif number == lenOfNeis + lenOfMines:
            print('number == lenOfNeis + lenOfMines', point)
            for nei in self.allNeighbours(point):
                if nei in self.visited:
                    continue
                # mark nei as a mine
                self.mark(nei)
            # this clue has been used up, so delete it
            self.clues.pop(point)

        else:
            # clue A and clue B aa
            # in the following comment, denote A as point A's undetected neighbours, denote num(A) as point A's number
            # make sure that A and B is clue
            if point in self.mines or point in self.unvisited:
                return
            for nei in self.extenedAllNeighbours(point):
                if nei not in self.clues or nei in self.unvisited:
                    continue
                A = self.clues[point]['neighbours']  # set of A's neighbours
                B = self.clues[nei]['neighbours']  # set of B's neighbours
                A_B = A - B  # those in A but not in B
                numA = self.clues[point]['number']
                numB = self.clues[nei]['number']
                lenOfMinesA = len(self.clues[point]['mines'])
                lenOfMinesB = len(self.clues[nei]['mines'])
                # case 3: num(A) > num(B) and A - B = num(A) - num(B)
                if self.clues[point]['number'] > self.clues[nei]['number'] and len(A_B) == (numA - lenOfMinesA) - (
                            numB - lenOfMinesB):
                    for p in A_B:
                        print('According to', point, 'and', nei, 'I am sure that', p, 'as a mine')
                        self.mark(p)
                # case 4: A contains B and A(num) - A(mines) = B(num) - B(mine)
                elif A > B and (numA - lenOfMinesA) == (numB - lenOfMinesB):
                    for p in A_B:
                        if p in self.unvisited:
                            print('According to', point, 'and', nei, 'I am sure that', p, 'is safe')
                            self.safe.add(p)
                # case 5: involves 3 clue squares
                elif self.rule5 and (numA - lenOfMinesA) > (numB - lenOfMinesB):
                    for anotherNei in self.extenedAllNeighbours(point):
                        if anotherNei not in self.clues or nei not in self.unvisited or anotherNei == nei:
                            continue
                        C = self.clues[anotherNei]['neighbours']
                        numC = self.clues[anotherNei]['number']
                        lenOfMinesC = len(self.clues[anotherNei]['mines'])
                        if (numA - lenOfMinesA) == (numB - lenOfMinesB) + (numC - lenOfMinesC):
                            A_B_C = A - B - C
                            for p in A_B_C:
                                if p in self.unvisited:
                                    print('According to', point, 'and', nei, 'and', anotherNei, 'I am sure that', p,
                                          'is safe')
                                    self.safe.add(p)

    def updateNeighbours(self, point):
        '''
        to update this point's undetected neighbours
        :param point: coordinate of this point
        :return: noting to return
        '''
        if point not in self.clues:
            return
        neighbours = set()
        for nei in self.allNeighbours(point):
            if nei in self.unvisited:
                neighbours.add(nei)
        self.clues[point]['neighbours'] = neighbours

    def updateMinesNeighbours(self, point):
        '''
        this point is mine, to update its all neighbours' mines
        :param point: coordinate of this point
        :return: nothing to return
        '''
        if point not in self.clues:
            return
        for nei in self.allNeighbours(point):
            if nei in self.mines:
                self.clues[point]['mines'].add(nei)

    def allNeighbours(self, point):
        nei = set()
        x, y = point
        for i in range(max(x - 1, 0), min(x + 1, self.row - 1) + 1):
            for j in range(max(y - 1, 0), min(y + 1, self.col - 1) + 1):
                nei.add((i, j))
        # remove self
        nei.discard((x, y))
        return nei

    def extenedAllNeighbours(self, point):
        nei = set()
        x, y = point
        for i in range(max(x - 2, 0), min(x + 2, self.row - 1) + 1):
            for j in range(max(y - 2, 0), min(y + 2, self.col - 1) + 1):
                nei.add((i, j))
        # remove self
        nei.discard((x, y))
        return nei
