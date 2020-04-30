import pygame
from autoscroll import AutoscrollLevel

#an autoscrolling level, defined as level 1.
#player objective to collect speed powerups
class Level1(AutoscrollLevel):
    def __init__(self,res,img='highway.png'):
        super().__init__(res,img)
        self.start = False
        self.l1 = True
        self.l2 = False
        self.tutorial = False



    def updateLoop(self):
        keys = pygame.key.get_pressed()
        self.boolUpdate()
        self.autoScrollTimeUpdate()
        self.groupAdd()
        self.enemyUpdates()
        self.playerUpdates()
        self.drawAll()
        self.autoScrollMode()
        self.forLoop()
        self.interactions()
        

        pygame.display.flip()
        pygame.display.update()

    def drawAll(self):
        self.autoScrollDraw()
        self.player.draw(self.background)
        self.allObjects.draw(self.background)
        
    def interactions(self):
        self.playerEnemyInteractions()
        self.playerPowerInteractions()

    def loseMenu(self,mousePos):
        x,y = mousePos
        
        xTryRange = range(self.tryRect[0],self.tryRect[0]+self.tryRect[2])
        yTryRange = range(self.tryRect[1],self.tryRect[1]+self.tryRect[3])

        xGiveUp = range(self.giveUpRect[0],self.giveUpRect[0]+ self.giveUpRect[2])
        yGiveUp = range(self.giveUpRect[1],self.giveUpRect[1]+ self.giveUpRect[3])
        

        if x in xTryRange and y in yTryRange:
            self.lose = False
            self.autoPreset()

        if x in xGiveUp and y in yGiveUp:
            self.autoPreset()
            self.start = True 
            self.l1 = False

    def winMenu(self,mousePos):
        x,y = mousePos

        xRange = range(int(self.nextLevelRect[0]),int(self.nextLevelRect[0] + self.nextLevelRect[2]))
        yRange = range(int(self.nextLevelRect[1]),int(self.nextLevelRect[1] + self.nextLevelRect[3]))

        xGiveUp = range(self.mainUpRect[0],self.mainUpRect[0]+ self.mainUpRect[2])
        yGiveUp = range(self.mainUpRect[1],self.mainUpRect[1]+ self.mainUpRect[3])

        if x in xRange and y in yRange:
            self.l1 = False 
            self.l2 = True
        
        if x in xGiveUp and y in yGiveUp:
            self.autoPreset()
            self.start = True 
            self.l1 = False

    def pauseMenu(self,mousePos):
        x,y = mousePos

        unPauseX = range(int(self.unPauseRect[0]),int(self.unPauseRect[0] + self.unPauseRect[2]))
        unPauseY = range(int(self.unPauseRect[1]),int(self.unPauseRect[1] + self.unPauseRect[3]))

        titleX = range(int(self.titleRect[0]),int(self.titleRect[0]+ self.titleRect[2]))
        titleY = range(int(self.titleRect[1]),int(self.titleRect[1]+ self.titleRect[3]))

        if x in unPauseX and y in unPauseY:
            self.pause = False
        
        if x in titleX and y in titleY:
            self.autoPreset()
            self.start = True 
            self.l1 = False
            self.tutorial = False

