import pygame
from autoscroll import AutoscrollLevel

#technically the start screen is an autoscroll level, without player in it
#creates the start screen
class Start(AutoscrollLevel):
    def startPreset(self):
        self.autoPreset()
        self.start = True
        self.l1 = False
        self.l2 = False
        self.menuFlag1 = False
        self.menuFlag2 = False
        self.menuFlagL1 = False
        self.menuFlagL2 = False #There are 4 different menu popups


    def __init__(self,res,img='highway.png'):
        super().__init__(res,img)
        self.startPreset()

        self.next = self.font.render('Next',True,self.black,self.green)
        self.level1 = self.font.render('Level1: Chaos on Cat Street',True,self.black,self.green)
        self.level2  = self.font.render('Level2: Rat Trap Crusaders',True,self.black,self.green)
        self.back = self.font.render('Back',True,self.black,self.red) 
        self.levelSelect = self.font.render('Level Select',True,self.black,pygame.SRCALPHA)

        self.nextRect = (600, self.yDim - 50 - self.font.size('Next')[1]) + self.font.size('Next')
        self.levelSelectRect = (self.xDim/2 - self.font.size("Level Select")[0]/2,100) + self.font.size('Level Select')
        self.l1Rect = (100,150) + self.font.size('Level1: Chaos on Cat Street')
        self.l2Rect = (100,250) + self.font.size('Level2: Rat Trap Crusaders')
        self.backRect = (100,self.yDim - 50 - self.font.size('Back')[1]) + self.font.size('Back')

        self.story = self.imgLoad("story.png")
        self.l1Story = self.imgLoad('l1story.png')
        self.l2Story = self.imgLoad('l2story.png')

        self.menuRect = (50,50,self.xDim - 100,self.yDim - 100)
        self.startRect = (320,680,100,50)
        self.quitRect  = (470,680,100,50)
        self.titleRect = (119,134,400,100)
        self.image = self.imgLoad("highwayright.png")
        self.titleImage = self.imgLoad("logo.png")

    def updateLoop(self):
        self.autoScrollTimeUpdate()
        self.autoScroll()
        self.drawAll()
        self.menuScreen()
        self.startForLoop()


        pygame.display.flip()
        pygame.display.update()


    #custom designed for start menu
    def startForLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.menuInteraction(pygame.mouse.get_pos())


            if event.type == pygame.QUIT:
                self.playing = False
    

    def drawAll(self):
        self.autoScrollDraw()
        pygame.draw.rect(self.background,self.green,self.startRect)
        pygame.draw.rect(self.background,self.red,self.quitRect)
        startText = self.font.render('Start',True,self.black)
        quitText  = self.font.render('Quit',True,self.black)
        self.background.blit(self.titleImage,(300,180,400,400))
        self.background.blit(startText,self.startRect)
        self.background.blit(quitText,self.quitRect)

    def menuScreen(self):
        if self.menuFlag1 or self.menuFlag2 or self.menuFlagL1 or self.menuFlagL2:
            #menu background
            pygame.draw.rect(self.background,self.white,self.menuRect)
        if self.menuFlag1:
            self.background.blit(self.story,self.menuRect)
            self.background.blit(self.story,self.menuRect)
            self.background.blit(self.next,self.nextRect)
        elif self.menuFlag2:
            self.background.blit(self.level1,self.l1Rect)
            self.background.blit(self.level2,self.l2Rect)
            self.background.blit(self.back,self.backRect)
            self.background.blit(self.levelSelect,self.levelSelectRect)
        elif self.menuFlagL1:
            self.background.blit(self.l1Story,self.menuRect)
            self.background.blit(self.back,self.backRect)
            self.background.blit(self.next,self.nextRect)
        elif self.menuFlagL2:
            self.background.blit(self.l2Story,self.menuRect)
            self.background.blit(self.back,self.backRect)
            self.background.blit(self.next,self.nextRect)

    #defines all the menu interactions given mousepos
    def menuInteraction(self,mousePos):
        x,y = mousePos

        xStartLow = self.startRect[0]
        xStartHigh = xStartLow + self.startRect[2]
        yStartLow = self.startRect[1]
        yStartHigh = yStartLow + self.startRect[3]

        xQuitLow = self.quitRect[0]
        xQuitHigh = xQuitLow + self.quitRect[2]
        yQuitLow = self.quitRect[1]
        yQuitHigh = yQuitLow + self.quitRect[3]

        if x in range(xStartLow,xStartHigh) and y in range(yStartLow,yStartHigh):
            #self.l1 = True #proceed into game
            #self.start = False

            self.menuFlag1 = True
            

        if x in range(xQuitLow,xQuitHigh) and y in range(yQuitLow,yQuitHigh):
            self.playing = False

        if self.menuFlag1:
            nextXRange = range(self.nextRect[0],self.nextRect[0]+self.nextRect[2])
            nextYRange = range(self.nextRect[1],self.nextRect[1]+self.nextRect[3])

            if x in nextXRange and y in nextYRange:
                self.menuFlag1 = False
                self.menuFlag2 = True
        elif self.menuFlag2:
            l1XRange = range(self.l1Rect[0],self.l1Rect[0] + self.l1Rect[2])
            l1YRange = range(self.l1Rect[1],self.l1Rect[1] + self.l1Rect[3])

            l2XRange = range(self.l2Rect[0],self.l2Rect[0] + self.l2Rect[2])
            l2YRange = range(self.l2Rect[1],self.l2Rect[1] + self.l2Rect[3])

            backXRange = range(self.backRect[0],self.backRect[0] + self.backRect[2])
            backYRange = range(self.backRect[1],self.backRect[1] + self.backRect[3])
            
            if x in l1XRange and y in l1YRange:
                self.menuFlagL1 = True
                self.menuFlag2 = False
                #self.start = False
            if x in l2XRange and y in l2YRange:
                self.menuFlagL2 = True
                self.menuFlag2 = False
                #self.start = False
            if x in backXRange and y in backYRange:
                self.menuFlag1 = False
                self.menuFlag2 = False

        elif self.menuFlagL1:
            backXRange = range(self.backRect[0],self.backRect[0] + self.backRect[2])
            backYRange = range(self.backRect[1],self.backRect[1] + self.backRect[3])
            nextXRange = range(self.nextRect[0],self.nextRect[0]+self.nextRect[2])
            nextYRange = range(self.nextRect[1],self.nextRect[1]+self.nextRect[3])

            if x in nextXRange and y in nextYRange:
                self.l1 = True
                self.start = False
            if x in backXRange and y in backYRange:
                self.menuFlagL1 = False 
                self.menuFlag2 = True

        elif self.menuFlagL2:
            backXRange = range(self.backRect[0],self.backRect[0] + self.backRect[2])
            backYRange = range(self.backRect[1],self.backRect[1] + self.backRect[3])
            nextXRange = range(self.nextRect[0],self.nextRect[0]+self.nextRect[2])
            nextYRange = range(self.nextRect[1],self.nextRect[1]+self.nextRect[3])

            if x in nextXRange and y in nextYRange:
                self.l2 = True
                self.start = False
            if x in backXRange and y in backYRange:
                self.menuFlagL2 = False 
                self.menuFlag2 = True



