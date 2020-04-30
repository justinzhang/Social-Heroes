import pygame
from zone import ZoneLevel

#level 2 is a zone dungeon level. Enter zones to initiate enemy spawn. Boss spawns after all waves
class Level2(ZoneLevel):
    def __init__(self,res,img='attic.png'):
        super().__init__(res,img)
        self.zonePreset()

        self.start = False
        self.l1 = False
        self.l2 = True
        self.tutorial = False



    def updateLoop(self):
        keys = pygame.key.get_pressed()
        self.timeTick()
        self.zoneScroll(keys)
        self.zoneBoolUpdate()
        self.groupAdd()
        self.drawAll()
        self.zoneMode()
        self.forLoop()
        self.interactions()
        self.enemyUpdates()
        self.playerUpdates()
        
        
        

        pygame.display.flip()
        pygame.display.update()

    def drawAll(self):
        self.zoneDraw()
        self.player.draw(self.background)
        self.allObjects.draw(self.background)
        
    def interactions(self):
        self.playerEnemyInteractions()
        self.playerPowerInteractions()

    def winMenu(self,mousePos):
        x,y = mousePos

        xRange = range(int(self.nextLevelRect[0]),int(self.nextLevelRect[0] + self.nextLevelRect[2]))
        yRange = range(int(self.nextLevelRect[1]),int(self.nextLevelRect[1] + self.nextLevelRect[3]))


        if x in xRange and y in yRange:
            self.autoPreset()
            self.l2 = False
            self.start = True
            self.victory = True
        
 

    def loseMenu(self,mousePos):
        x,y = mousePos
        
        xTryRange = range(self.tryRect[0],self.tryRect[0]+self.tryRect[2])
        yTryRange = range(self.tryRect[1],self.tryRect[1]+self.tryRect[3])

        xGiveUp = range(self.giveUpRect[0],self.giveUpRect[0]+ self.giveUpRect[2])
        yGiveUp = range(self.giveUpRect[1],self.giveUpRect[1]+ self.giveUpRect[3])
        

        if x in xTryRange and y in yTryRange:
            self.zonePreset()

        if x in xGiveUp and y in yGiveUp:
            self.zonePreset()
            self.lose = False
            self.start = True
            self.l2 = False
            self.tutorial = False

    def pauseMenu(self,mousePos):
        x,y = mousePos

        unPauseX = range(int(self.unPauseRect[0]),int(self.unPauseRect[0] + self.unPauseRect[2]))
        unPauseY = range(int(self.unPauseRect[1]),int(self.unPauseRect[1] + self.unPauseRect[3]))

        titleX = range(int(self.titleRect[0]),int(self.titleRect[0]+ self.titleRect[2]))
        titleY = range(int(self.titleRect[1]),int(self.titleRect[1]+ self.titleRect[3]))

        if x in unPauseX and y in unPauseY:
            self.pause = False
        
        if x in titleX and y in titleY:
            self.zonePreset()
            self.start = True 
            self.l2 = False

