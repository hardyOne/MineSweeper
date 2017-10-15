import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from user import User
from generateMap import Map
from time import sleep
import win32api, win32con
from random import random


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # to set map
        self.row = 20
        self.col = 20
        self.p = 0.15
        self.mineNo = int(self.row * self.col * self.p)
        map = Map(self.row, self.col, self.mineNo)
        # create a user
        self.user = User(map.randomGenerate())
        # set button width and height
        self.maxSize = 600
        self.buttonWidth = self.maxSize // max(self.row, self.col)
        self.buttonHeight = self.maxSize // max(self.row, self.col)
        # set window
        self.left = 50
        self.top = 50
        self.width = (self.row + 1) * self.buttonWidth
        self.height = (self.col + 2) * self.buttonHeight
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.title = 'MineSweeper' + '(' + str(self.row) + '*' + str(self.col) + ')'
        self.setWindowTitle(self.title)
        # if allowed simulate click
        self.simulateClick = False
        # is game finished
        self.finished = False
        self.setWindowIcon(QIcon('icon.jpg'))
        # create buttons
        # set font
        font = QFont()
        font.setPointSizeF(self.buttonHeight / 3)
        # set function button
        beginButton = QPushButton(self)
        beginButton.setText("Run")
        beginButton.setFixedSize(self.buttonWidth * 2, self.buttonHeight)
        beginButton.setFont(font)
        beginButton.move(self.buttonWidth, 0)
        beginButton.clicked.connect(self.play)
        resetButton = QPushButton(self)
        resetButton.setText("Reset")
        resetButton.clicked.connect(self.reset)
        resetButton.setFixedSize(self.buttonWidth * 2, self.buttonHeight)
        resetButton.setFont(font)
        resetButton.move(self.buttonWidth * (self.col - 1), 0)
        # set simulate click
        chooseButton = QPushButton(self)
        chooseButton.setText("simulate")
        chooseButton.setFixedSize(self.buttonWidth * 4, self.buttonHeight)
        chooseButton.setFont(font)
        chooseButton.move(self.buttonWidth*(self.col/2-1), 0)
        chooseButton.clicked.connect(self.simulate)
        # set table row && col
        for i in range(self.row + 1):
            for j in range(self.col + 1):
                if (i == 0 or j == 0) and i != j:
                    button = QPushButton(self)
                    button.setFixedSize(self.buttonWidth, self.buttonHeight)
                    button.setText(str(i + j - 1))
                    button.setFont(font)
                    button.move(self.buttonWidth * i, self.buttonHeight * (j + 1))
                    # set buttons
        # set square button
        self.buttons = []
        for i in range(1, self.row + 1):
            temp = []
            for j in range(1, self.col + 1):
                button = QPushButton(self)
                button.setFixedSize(self.buttonWidth, self.buttonHeight)
                name = str(i - 1) + ',' + str(j - 1)
                button.setObjectName(name)
                button.setToolTip(name)
                button.setStyleSheet('background-color:grey')
                button.setFont(font)
                button.move(self.buttonWidth * j, self.buttonHeight * (i + 1))
                button.clicked.connect(self.on_click)
                temp.append(button)
            self.buttons.append(temp)
        self.show()

    # simulate click (used for agent)
    def click(self, point):
        '''
        this function is used to simulate click of agent
        :param point: the coordinate of the next point to click for agent
        :return:
        '''
        # logical position
        i = point[0]
        j = point[1]
        button = self.buttons[i][j]
        x = button.x() + self.left + self.buttonWidth // 2
        y = button.y() + self.top + self.buttonHeight // 2
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    def play(self):
        if self.finished:
            return
        self.finished = True
        if self.simulateClick:
            point = None
            while True:
                point = self.user.agent.nextClick()
                res = self.user.result(point)
                if res == 'FAILURE' or res == 'SUCCESS':
                    self.finished = True
                    break
            for p in self.user.agent.sequence:
                self.click(p)

        else:
            while True:
                (x, y) = self.user.agent.nextClick()
                res = self.user.result((x, y))
                button = self.buttons[x][y]
                button.setText(str(self.user.map[x][y]))
                button.setStyleSheet('background-color:white')
                if self.user.map[x][y] == 0:  # empty squares
                    button.setText('')
                elif self.user.map[x][y] == 9:  # booms
                    button.setStyleSheet('background-color:yellow')
                else:  # clues
                    button.setStyleSheet('background-color:orange')
                if res == 'FAILURE':
                    button.setText('T')
                    for fakeMineX, fakeMineY in self.user.agent.mines - self.user.mines:
                        self.buttons[fakeMineX][fakeMineY].setText('F')
                    break
                if res == 'SUCCESS':
                    break
            # display the mines marked by agent
            for (mineX, mineY) in self.user.agent.mines:
                self.buttons[mineX][mineY].setStyleSheet('background-color:yellow')

    def on_click(self):
        '''
        this function is used to monitor click event
        :return: nothing to return
        '''
        sleep(0.05)  # used for people to see phenomenon
        # to get which button triggers this click event
        senderButton = self.sender()
        name = senderButton.objectName()
        pos = name.split(',')
        x = int(pos[0])
        y = int(pos[1])
        button = self.buttons[x][y]
        button.setText(str(self.user.map[x][y]))
        button.setStyleSheet('background-color:white')
        if self.user.map[x][y] == 0:  # empty squares
            button.setText('')
        elif self.user.map[x][y] == 9:  # booms
            button.setStyleSheet('background-color:yellow')
            button.setText('')
            if (x,y) not in self.user.agent.mines:
                button.setText('T')
        else:  # clues
            button.setStyleSheet('background-color:orange')
        # agent mark fake mines, display them
        if (x, y) in self.user.agent.mines and (x, y) not in self.user.mines:
            button.setStyleSheet('background-color:red')

    def reset(self):
        self.p = random() / 10 + 0.1
        map = Map(self.row, self.col, int(self.row * self.col * self.p))
        self.user = User(map.randomGenerate())
        self.finished = False
        self.simulateClick = False
        for i in range(0, self.row):
            for j in range(0, self.col):
                button = self.buttons[i][j]
                button.setStyleSheet('background-color:grey')
                button.setText("")

    def simulate(self):
        self.simulateClick = True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
