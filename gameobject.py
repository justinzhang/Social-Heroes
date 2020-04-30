import pygame

import random


#This code is all selfwritten with help from pygame documentation

#basic game object implementation. Players, bullets, enemies, etc. all derive from this class
class GameObject(pygame.sprite.Sprite):
    def __init__(self,screen,img,coords,velocity = (2,2)):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'default'
        self.screen = screen #for extension manipulation
        self.x,self.y = coords
        self.velocity = velocity #for all tuple needs of velocity
        self.xVel,self.yVel = velocity #for all int needs of velocity
        self.justShot = False
        self.image = self.imgLoad(img)
        
        #scrolling background stuff
        self.xRel = self.x
        self.yRel = self.y
        
        self.getDim()
        self.getRect()


    #load all the images at once so it doesnt need to be done constantly
    #must be in the game image directory
    #default resize will be 80x80
    @staticmethod
    def imgLoad(img,resizeDim = False):
        playerImg = pygame.image.load(f"images/objects/{img}").convert_alpha()
        if resizeDim:
            playerImg = pygame.transform.scale(playerImg,(80,80))
        return playerImg

    def getDim(self):
        self.xDim,self.yDim = self.image.get_rect().size
        self.radius = max(self.xDim / 2, self.yDim / 2 ) 
        #want the greatest radius so no weird Out Of Bounds (oob) errors

    def getRect(self):
        if self.name != 'bullet': #bullets are allowed oob
            self.oob(self.screen)
        self.velocity = self.xVel,self.yVel
        self.rect = pygame.Rect(self.x - self.xDim/2,self.y - self.yDim/2,
                                self.xDim,self.yDim)

    #universal move function. The mult variables is what degree movement happens
    def move(self,player=None,xMult=1,yMult=1,offset = False):    
        xMove,yMove = 1,1
        if player != None:
            xMove = 1 if self.x - player.x < 0 else -1
            yMove = 1 if self.y - player.y < 0 else -1
        xOffset,yOffset = 0,0
        if offset and random.randint(0,2) == 1: #method to make sure the enemies don't jerk around too often, simple solution
            xOffset,yOffset = random.randint(-10,10),random.randint(-10,10) 
        self.x += xMove*xMult + xOffset
        self.y += yMove*yMult + yOffset

        self.getDim()
        self.getRect()
    
    #prevents game objects from going out of bounds (OOB)
    def oob(self,screen):
        if screen.name == 'autoscroll':
            if screen.dir == 'right':
                if self.xRel > self.screen.width:
                    self.x = self.screen.xDim
                    self.xRel = self.screen.width
                if self.yRel < 60 + self.radius:
                    self.y = 60 + self.radius
                    self.yRel = 60 + self.radius
                if self.yRel > self.screen.height:
                    self.y = self.screen.yDim
                    self.yRel = self.screen.height
            elif screen.dir == 'left':
                if self.xRel < self.radius:
                    self.x = self.radius
                    self.xRel = self.radius
                if self.yRel < 60 + self.radius:
                    self.y = 60 + self.radius
                    self.yRel = 60 + self.radius
                if self.yRel > self.screen.height:
                    self.y = self.screen.yDim
                    self.yRel = self.screen.height
            elif screen.dir == 'up':
                if self.xRel < self.radius:
                    self.x = self.radius
                    self.xRel = self.radius
                if self.xRel > self.screen.width:
                    self.x = self.screen.xDim
                    self.xRel = self.screen.width
                if self.yRel < 60 + self.radius:
                    self.y = 60 + self.radius
                    self.yRel = 60 + self.radius  
            else:
                if self.xRel < self.radius:
                    self.x = self.radius
                    self.xRel = self.radius
                if self.xRel > self.screen.width:
                    self.x = self.screen.xDim
                    self.xRel = self.screen.width
                if self.yRel > self.screen.height:
                    self.y = self.screen.yDim
                    self.yRel = self.screen.height

        elif self.screen.name == 'zone':
            if self.xRel < 0 + self.radius: #the lower x bound + radius, written for clarity
                self.x = self.radius
                self.xRel = self.radius
            if self.xRel > self.screen.width:
                self.x = self.screen.xDim
                self.xRel = self.screen.width
            if self.yRel < 60 + self.radius:
                self.y = 60 + self.radius
                self.yRel = 60 + self.radius
            if self.yRel > self.screen.height:
                self.y = self.screen.yDim
                self.yRel = self.screen.height


#same attributes and methods as gameObject
#except classified to not interact with the environment
class GameImage(GameObject):
    def __init__(self,screen,img,coords):
        super().__init__(screen,img,coords)
        self.image = pygame.transform.scale(self.image,(80,80))



