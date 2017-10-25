from random import randint
from itertools import permutations


class Agent:
    def __init__(self, row, col, user):
        self.row = row
        self.col = col
        # set of all detected clues: undetected 0-square and non-0 squares
        self.clues = dict()
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.clues[(i, j)] = dict(
                    [('neighbours', set()), ('mines', set()), ('number', 10)])
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
        self.randomPercentage = 0.3
        # the sequence of click or mark
        self.sequence = []
        # use rule 5 and 6 or not
        self.rule56 = False
        # know the number of mines or not
        self.numberOfMinesFromUser = None


    def mark(self, point):
        # point is in mines
        if point in self.mines:
            return
        self.sequence.append(point)
        print('mark', point, 'as a mine', len(self.mines))
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
            # # check mine's neighbours, denote them as N, if N's number is equal to length of mines around them,
            # # then we can make sure that all N's undecteced neighbours are safe
            # if len(self.clues[nei]['mines']) == self.clues[nei]['number']:
            #     for neiNei in self.allNeighbours(nei):
            #         if neiNei in self.unvisited:
            #             self.safe.add(neiNei)
            #     # this clue has been used up, delete it
            #     self.clues.pop(nei)

    def nextClick(self):
        # exist safe squares
        if len(self.safe) != 0:
            self.rule56 = False
            point  = self.safe.pop()
            self.sequence.append(point)
            return point
        # no safe squares left
        # to get useful information(mines or safe squares)
        for p in dict(self.clues):
            self.updateClues(p)
        # try another times to see if there exists a safe square
        if len(self.safe) != 0:
            point = self.safe.pop()
            self.sequence.append(point)
            return point

        # try not to use rule 5 and 6 because it's time-consuming, but we have no choice
        self.rule56 = True
        for p in dict(self.clues):
            self.updateClues(p)
        # try another times to see if there exists a safe square
        if len(self.safe) != 0:
            point = self.safe.pop()
            self.sequence.append(point)
            return point


        # If we know the total number of mines, try another time
        self.inferAtLast()

        if len(self.safe) != 0:
            point = self.safe.pop()
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
        if len(self.unvisited) == 0:
            return (-1, -1)
        visitedPercentage = (len(self.clues) - len(self.unvisited)) / (len(self.unvisited))
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
                    print('%.3f' % visitedPercentage, listUnvisited[rNum])
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
        # case special: 1-2-1
        elif number == 1:
            x,y = point
            neiA = x,y+1
            neiB = x,y+2
            # make sure the neiA and neiB are valid clue
            condition1 = neiA not in self.clues or neiB not in self.clues or neiA not in self.visited or neiB not in self.visited
            if condition1:
                return
            # make sure the number of neiA is 2 and neiB is 1
            condition2 = self.clues[neiA]['number'] == 2 and self.clues[neiB]['number'] == 1
            if condition2:
                print('special situation: 1-2-1', point, neiA, neiB)
                candidates = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y+1),(x+1,y+1),(x-1,y+3),(x,y+3),(x+1,y+3)]
                for candidate in candidates:
                    if candidate in self.unvisited:
                        self.safe.add(candidate)
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
                if numA - lenOfMinesA > numB - lenOfMinesB and len(A_B) == (numA - lenOfMinesA) - (
                            numB - lenOfMinesB):
                    for p in A_B:
                        print('According to', point, 'and', nei, 'I am sure that', p, 'as a mine')
                        self.mark(p)
                # case 4: A contains B and A(num) - A(mines) = B(num) - B(mine)
                elif (numA - lenOfMinesA) == (numB - lenOfMinesB) and A >= B :
                    for p in A_B:
                        if p in self.unvisited:
                            print('According to', point, 'and', nei, 'I am sure that', p, 'is safe')
                            self.safe.add(p)
                # case 5 and 6: involves 3 clue squares
                elif self.rule56 and (numA - lenOfMinesA) > (numB - lenOfMinesB) and len(A&B) != 0:
                    for anotherNei in self.extenedAllNeighbours(point):
                        if anotherNei not in self.clues or nei in self.unvisited or anotherNei == nei or len(A&self.clues[anotherNei]['neighbours']) == 0:
                            continue
                        C = self.clues[anotherNei]['neighbours']
                        numC = self.clues[anotherNei]['number']
                        lenOfMinesC = len(self.clues[anotherNei]['mines'])
                        # case 5: logic same as case 4, but involve 4 squares
                        # how many mines in A or C are also in C
                        # if B is in C
                        lenOfContributedMines = None
                        if C >= B:
                            lenOfContributedMines = numC - lenOfMinesC
                        elif B>= C:
                            lenOfContributedMines = numB - lenOfMinesB
                        elif len(B&C) == 0:
                            lenOfContributedMines = (numB - lenOfMinesB) + (numC - lenOfMinesC)
                        if lenOfContributedMines == None:
                            continue
                        if (numA - lenOfMinesA) == lenOfContributedMines and A >= (B | C):
                            A_B_C = A - B - C
                            for p in A_B_C:
                                if p in self.unvisited:
                                    print('According to', point, 'and', nei, 'and', anotherNei, 'I am sure that', p,
                                          'is safe')
                                    self.safe.add(p)
                        # case 6: logic same as case 5, but involve 4 squares
                        if (numA - lenOfMinesA) - lenOfContributedMines == len(A - B - C) and len(A&B) != 0:
                            A_B_C = A - B - C
                            for p in A_B_C:
                                if p in self.unvisited:
                                    print('According to', point, 'and', nei, 'and', anotherNei,
                                          'I am sure that', p,
                                          'is a mine')
                                    self.mark(p)


                                    # this function is used when: 1, the agent know the total number of mines. 2, the undetected squares is limited
                                    # 3, No safe squares left.
    def inferAtLast(self):
        if self.numberOfMinesFromUser == None or len(self.unvisited) > 15 or len(self.unvisited) == 0:
            return
        print('Yes, because only',self.numberOfMinesFromUser - len(self.mines),'I know total number of mines, so I choose to infer!')
        lenOfMinesLeft = self.numberOfMinesFromUser - len(self.mines)
        # if number of undetected squares is equal to number of mines left
        if lenOfMinesLeft == len(self.unvisited):
            print('all left squares are mine')
            for finalMine in self.unvisited:
                self.mark(finalMine)
        # if no mines left
        if lenOfMinesLeft == 0:
            print('all left squares are safe')
            for p in self.unvisited:
                print('infer:',p,'is safe!')
                self.safe.add(p)
        # else, we enumerate all possible combinations and check if it's valid
        else:
            # back up clues
            cp_clues = dict(self.clues)
            listOfUnvisited = list(self.unvisited)
            initial = [True if i < lenOfMinesLeft else False for i in range(len(listOfUnvisited))]
            for assignment in permutations(initial):
                mineSet = [listOfUnvisited[i] for i in range(len(self.unvisited)) if assignment[i] == True]
                safeSet = [listOfUnvisited[i] for i in range(len(self.unvisited)) if assignment[i] == False]
                isValid = True
                for mine in mineSet:
                    for nei in self.allNeighbours(mine):
                        if nei in self.clues and nei in self.visited:
                            self.clues[nei]['neighbours'].discard(mine)
                            self.clues[nei]['mines'].add(mine)
                for safeSquare in safeSet:
                    for nei in self.allNeighbours(mine):
                        if nei in self.clues and nei in self.visited:
                            self.clues[nei]['neighbours'].discard(mine)
                # check if there is a conflict
                for point in self.unvisited:
                    for nei in self.allNeighbours(point):
                        if nei not in self.clues or nei in self.unvisited:
                            continue
                        # Assignment is invalid
                        num = self.clues[nei]['number']
                        neiNum = len(self.clues[nei]['neighbours'])
                        mineNum = len(self.clues[nei]['mines'])
                        if num < mineNum or num > neiNum + mineNum:
                            isValid = False
                            break
                    if not isValid:
                        break
                if not isValid:
                    self.clues = dict(cp_clues)
                    break
                # mark mines and add safe squares
                print('This is a true assignment!')
                for safeSquare in safeSet:
                    self.safe.add(safeSquare)
                for mine in mineSet:
                    self.mark(mine)
                # find one valid permutation, the agent will stop
                return

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
