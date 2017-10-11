import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
from user import User
from generateMap import Map
from time import sleep
import win32api, win32con


class App(QWidget):
    def __init__(self):
        super().__init__()
        map = Map(20,20,80)
        self.user = User(map.randomGenerate())
        self.row = self.user.row
        self.col = self.user.col
        self.maxSize = 750
        self.buttonWidth = self.maxSize // max(self.row,self.col)
        self.buttonHeight = self.maxSize // max(self.row,self.col)
        self.buttons = []
        self.title = 'MineSweeper'
        self.left = 50
        self.top = 50
        self.width = (self.row + 1) * self.buttonWidth
        self.height = (self.col + 1) * self.buttonHeight
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # set table row && col
        for i in range(self.row + 1):
            for j in range(self.col + 1):
                if (i == 0 or j == 0) and i != j:
                    button = QPushButton(self)
                    button.setFixedSize(self.buttonWidth, self.buttonHeight)
                    button.setText(str(i + j - 1))
                    button.move(self.buttonWidth * i, self.buttonHeight * j)
        # set buttons
        for i in range(1, self.row + 1):
            temp = []
            for j in range(1, self.col + 1):
                button = QPushButton(self)
                button.setFixedSize(self.buttonWidth, self.buttonHeight)
                name = str(i - 1) + ',' + str(j - 1)
                button.setObjectName(name)
                button.setToolTip(name)
                button.setStyleSheet('background-color:grey')
                button.move(self.buttonWidth * j, self.buttonHeight * i)
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
        # real position
        x = self.buttonWidth * (j + 1) + self.left + self.buttonWidth // 2
        y = self.buttonHeight * (i + 1) + self.top + self.buttonHeight // 2
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    def play(self):
        while True:
            (x, y) = self.user.agent.nextClick()
            res = self.user.result((x, y))
            self.click((x,y))
            if res == 'FAILURE' or res == 'SUCCESS':
                for x,y in self.user.agent.mines:
                    self.buttons[x][y].setStyleSheet('background-color:indigo')
                break

    @pyqtSlot()
    def on_click(self):
        '''
        this function is used to monitor click event
        :return: nothing to return
        '''
        sleep(0.01) # used for people to see phenomenon
        # to get which button triggers this click event
        senderButton = self.sender()
        name = senderButton.objectName()
        pos = name.split(',')
        x = int(pos[0])
        y = int(pos[1])
        button = self.buttons[x][y]
        button.setText(str(self.user.map[x][y]))
        button.setStyleSheet('background-color:white')
        if self.user.map[x][y] == 0: # empty squares
            button.setText('')
        elif self.user.map[x][y] == 9: # booms
            button.setStyleSheet('background-color:yellow')
        else: # clues
            button.setStyleSheet('background-color:orange')
        if (x,y) in self.user.agent.clues:
            pass
            # print((x,y),self.user.agent.clues[(x,y)]['neighbours'])
            # used for users to play the game
            # condition = (x, y) in self.user.agent.visited
            # if not condition:
            #     pass
            #     # res = self.user.result((x, y), 'click')
            # else:
            #     if (x, y) in self.user.agent.clues:
            #         nei = self.user.agent.clues[(x, y)]['neighbours']
            #         print((x, y))
            #         print('len:', len(nei))
            #         print(nei)
            #     else:
            #         print('not in clues')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.play()
    sys.exit(app.exec_())
