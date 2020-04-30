import pygame
import random
from level import Level
from player import *
from enemies import *
from powerup import *
from gameobject import GameImage


#for autoscrolling levels. Screen will automatically scroll in a direction,
#and change direction occasionally
class AutoscrollLevel(Level):
    #preset for autoscroll levels
    def autoPreset(self):
        self.preset()
        self.name = 'autoscroll'
        #reset autoscroll pos and dir to original location
        self.dir = 'right' 
        self.changingDir = self.dir
        self.image = self.imgLoad("highwayright.png")
        self.changeImage = self.image
        self.changeFlag = False
        self.changeDisX = 0
        self.changeDisY = 0
        self.x = 0
        self.y = 0
        self.xDisplayRel = 0
        self.yDisplayRel = 0
        self.transitionFlag = True
        self.transitionCounter = 0
        self.winCond = 5.25
        self.initPlayer(self.res)
        self.centerStage()

    def __init__(self,res,img):
        super().__init__(res,img)
        self.autoPreset()

    #time update specifically for autoscroll
    def autoScrollTimeUpdate(self):
        self.timeTick()
        if self.timer % 800 == 0 and random.randint(0,2) == 1:
            self.dirChange()

    #changes direction variables here
    def dirChange(self):
        changeList = ['up','down'] if self.dir == 'right' or self.dir == 'left' else ['right','left']
        self.changingDir = random.choice(changeList)


        self.changeImage = self.imgLoad(f"highway{self.dir+self.changingDir}.png")
        self.changeFlag = True

        self.changeDisX = -self.width if self.dir == 'left' else self.width
        self.changeDisY = -self.height if self.dir == 'up' else self.height

        self.xDisplayRel = 0
        self.yDisplayRel = 0

    #auto scroll logic
    #map moves depending on direction
    def autoScroll(self):
        if self.dir == 'right' or self.dir == 'left':
            
            rightFlag = 1 if self.dir == 'right' else -1
            self.xDisplayRel = self.x % self.image.get_rect().width
            self.x -= 2 * rightFlag

            self.changeDisX -= 2 * rightFlag
                                           #this extra bit ensures powerups and gameimages move as well,
            for sprite in self.allObjects: #weird bug == weird fix
                if sprite in self.powerups or self.gameImages: sprite.move(None,-2*rightFlag,0)
                sprite.xRel -= 2 * rightFlag
                sprite.x = sprite.xRel
                sprite.y = sprite.yRel

                if not (-sprite.xDim < sprite.x < self.width):
                    sprite.kill()

        elif self.dir == 'up' or self.dir == 'down': 
            upFlag = -1 if self.dir == 'up' else 1
            self.yDisplayRel = self.y % self.image.get_rect().height
            self.y -= 2 * upFlag

            self.changeDisY -= 2 * upFlag

            for sprite in self.allObjects:
                if sprite in self.powerups or self.gameImages: sprite.move(None,-2*upFlag,0)
                sprite.yRel -= 2 * upFlag
                sprite.x = sprite.xRel
                sprite.y = sprite.yRel

                if not (0 < sprite.y < self.height + 60):
                    sprite.kill()

    #draws screen given directional logic from autoscroll gamemode
    def autoScrollDraw(self):
        self.screen.fill(self.black)
        self.screen.blit(self.background,(0,0))

        
        if self.dir == 'right' or self.dir == 'left':
            self.transitionCounter += 2
            #transition counter counts the ticks of when a transformation is occuring
            #each tick is equal to one square dim
            if self.dir == 'right':
                if self.xDisplayRel < self.width:
                    self.background.blit(self.image, (self.xDisplayRel,self.yDisplayRel)) 
                    #refreshes the image offscreen, slowly comes into display
                if not self.transitionFlag:
                    self.background.blit(self.changeImage,(self.xDisplayRel- self.width,self.yDisplayRel))
                    self.transitionFlag = self.transitionCounter == self.width
                    
                else:
                    self.background.blit(self.image,(self.xDisplayRel - self.width,self.yDisplayRel))
            #different directions mean different blitting start points
            if self.dir == 'left':
                if self.xDisplayRel < self.width:
                    self.background.blit(self.image,(self.xDisplayRel - self.width,self.yDisplayRel))

                if not self.transitionFlag:
                    self.background.blit(self.changeImage,(self.xDisplayRel,self.yDisplayRel))
                    self.transitionFlag = self.transitionCounter == self.width
                    
                else:
                    self.background.blit(self.image,(self.xDisplayRel,self.yDisplayRel))
                
            if self.changeFlag:
                self.background.blit(self.changeImage,(self.changeDisX,0))

            if self.changeFlag and self.changeDisX == 0:
                self.transitionCounter = 0
                self.dir = self.changingDir
                self.image = self.imgLoad(f"highwayup.png")
                self.changeFlag = False
                self.transitionFlag = False
                self.xDisplayRel = 0
                self.y = 0 if self.dir == 'up' else self.height - 2 #preventing screen glitching

                               
        elif self.dir == 'up' or self.dir == 'down':
            self.transitionCounter += 2
            if self.dir == 'up':
                if self.yDisplayRel < self.height:
                    self.background.blit(self.image,(self.xDisplayRel,self.yDisplayRel - self.height))
                if not self.transitionFlag:
                    self.background.blit(self.changeImage,(self.xDisplayRel,self.yDisplayRel))
                    self.transitionFlag = self.transitionCounter >= self.height
                else:
                    self.background.blit(self.image,(self.xDisplayRel,self.yDisplayRel ))

            if self.dir == 'down':
                if self.yDisplayRel < self.height:
                    self.background.blit(self.image,(self.xDisplayRel,self.yDisplayRel))

                if not self.transitionFlag:
                    self.background.blit(self.changeImage,(self.xDisplayRel,self.yDisplayRel - self.height))
                    self.transitionFlag = self.transitionFlag = self.transitionCounter == self.height
                else:
                    #self.transitionCounter = 0
                    self.background.blit(self.image,(self.xDisplayRel,self.yDisplayRel - self.height))
                    
            if self.changeFlag:
                self.background.blit(self.changeImage,(0,self.changeDisY))      

            if self.changeFlag and self.changeDisY == 0:
                self.dir = self.changingDir
                self.image = self.imgLoad(f"highwayright.png")
                self.changeFlag = False
                self.transitionFlag = False
                self.transitionCounter = 0
                self.x = 0 if self.dir == 'left' else self.width - 2 #preventing screen glitching
                self.yDisplayRel = 0

  
        

    #returns scroll spawn coords given direction and dims
    def scrollSpawn(self):
        if self.changingDir == 'right':
            spawnX = self.width + random.randint(100,200)
            spawnY = random.randint(0,self.height)
        elif self.changingDir == 'left':
            spawnX = -random.randint(100,200)
            spawnY = random.randint(0,self.height)
        elif self.changingDir == 'up':
            spawnX = random.randint(0,self.width)
            spawnY = -random.randint(100,200)
        else: #changingDir == 'down'
            spawnX = random.randint(0,self.width)
            spawnY = self.height + random.randint(100,200)
        return spawnX,spawnY

    #blitting autoscroll mode info onto hud
    def autoBlit(self):
        if not self.win:
            relSpeed = int((abs(self.p.xVel) - 4)*4) #speed in terms of how much speed obtained
            text = f"SPEED: {relSpeed}/5"
        if self.win:
            text = 'YOU WIN'
            self.winScreen()
        if self.lose:
            text = "Try again"
            self.loseScreen()
        if self.pause:
            self.pauseScreen()

        escapeText = self.font.render(text,True,self.black,(255,255,255))
        self.background.blit(escapeText,(0,60,100,100))

    #autoscroll gamemode logic
    #fun fact: originally called escape mode! Also this was really hard to implement for me so I'm happy it works
    def autoScrollMode(self):
        if self.inGame:
            self.autoScroll()

            #win condition
            if self.p.xVel >= self.winCond:
                if self.inGame: self.time = self.timer // 120 #number of seconds
                self.win = True

            #timer based spawns
            if self.inGame:
                if self.timer % 240 == 0:
                    coords = self.scrollSpawn()
                    enemy = Cat(self,coords)
                    self.enemies.add(enemy)
        
                if self.timer % 360 == 0:
                    coords = self.scrollSpawn()
                    if self.changingDir == 'left' or self.changingDir == 'right':
                        enemy = RoadBlock(self,'blockV.png',coords)
                    else:
                        enemy = RoadBlock(self,'blockH.png',coords)
                    self.enemies.add(enemy)

                if self.timer % 500 == 0:
                    coords = self.scrollSpawn()
                    if random.randint(0,9) > 2: #80% chance to spawn general powerup
                        self.powerSpawn(coords,True,False)
                    else:   #20% chance to spawn weapon
                        self.powerSpawn(coords,False,True)

        self.autoBlit()

    

    
    
