import pygame
from start import Start
from level1 import Level1
from level2 import Level2

#This code is all selfwritten with help from pygame documentation

#main game file. run this to run the game
class Game(object):
    def __init__(self):
        pygame.init()

        self.res = (800,800)
        self.clock = pygame.time.Clock()
        self.victory = False #when full game has been completed
        self.start = Start(self.res)
        self.level1 = Level1(self.res)
        self.level2 = Level2(self.res)
        self.currLevel = self.start #starts on start screen


    def main(self):
        while self.currLevel.playing:
            self.currLevel.updateLoop()
            self.levelSwitch()
        pygame.quit()

    def levelSwitch(self):
        if self.currLevel.start== True:
            self.currLevel = self.start
            self.currLevel.l1 = False
            self.currLevel.l2 = False
        elif self.currLevel.l1 == True: 
            self.currLevel = self.level1
            self.currLevel.start = False
            self.currLevel.l2 = False
        elif self.currLevel.l2 == True: 
            self.currLevel = self.level2
            self.currLevel.start = False
            self.currLevel.l1 = False


          

game = Game()

game.main()
