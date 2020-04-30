import random
import pygame
from level import Level
from player import *
from enemies import *
from powerup import *
from gameobject import GameImage

#defining zone levels from level class
#camera moves based off of player location
class ZoneLevel(Level):
    #preset for zone gamemode
    def zonePreset(self):
        self.preset()
        self.name = 'zone'
        self.scrollFlag = False
        self.wave = 0
        self.zoneFlag = False
        self.zones = list()
        self.completedZones = set()
        self.generateZones() 
        self.initPlayer(self.res)
        self.centerStage()

    #generates zones on the map of max dim 800x800 randomly
    #zones in format: (xStart,yStart,xEnd,yEnd)
    def generateZones(self,amount=5):
        for zone in range(amount):
            x,y = random.randint(0,self.width-800),random.randint(0,self.height - 800)
            xDim,yDim = random.randint(600,800),random.randint(600,800)
            self.zones.append((x,y,x+xDim,y+yDim))

    #starts a new wave of enemies, difficulty increases with wave num
    def initWave(self):
        self.wave += 1
        for numEnemies in range(3 + 2*self.wave):
            coord1 = random.randint(0,self.xDim)
            coord2 = random.randint(0,self.yDim)
            enemy = Rat(self,(coord1,coord2))
            self.enemies.add(enemy)

    #zone mode scrolling. Scrolls with player at the center. Screen moves only when player does
    #uses stage variable to define the 800x800 view
    def zoneScroll(self,keys):
        #if before starting scroll, relative x = x
        if 0<self.p.xRel < self.xStartScroll and (keys[pygame.K_d] or keys[pygame.K_a]):
            self.p.x = self.p.xRel
        
        #scroll if after startscroll but before scroll ends
        elif self.xStartScroll <= self.p.xRel <= self.width and (keys[pygame.K_d] or keys[pygame.K_a]):    
            if self.xStage <= self.xDim -self.width and self.p.x >= self.xStartScroll:
                self.xStage = self.xDim - self.width
                self.p.x += self.p.xVel

            else: #middle of scroll
                self.p.x = self.xStartScroll
                self.xStage -= self.p.xVel
                
                #move all other sprites to compensate for screen move
                #AN I L L U S I O N
                for sprite in self.allObjects:
                    if sprite in self.enemyBullets: 
                        sprite.x -= self.p.xVel
                        sprite.xRel -= self.p.xVel
                    sprite.move(None,-self.p.xVel,0)
        self.xDisplayRel = self.x % self.image.get_rect().width
        self.x -= 1

                
        #likewise for y
        if 0<self.p.yRel < self.yStartScroll and (keys[pygame.K_w] or keys[pygame.K_s]):
            self.p.y = self.p.yRel
        elif self.yStartScroll <= self.p.yRel <= self.height and (keys[pygame.K_w] or keys[pygame.K_s]):            
            if self.yStage <= self.yDim -self.height and self.p.y >= self.yStartScroll:
                self.yStage = self.yDim - self.height
                self.p.y += self.p.yVel
            else:
                self.p.y = self.yStartScroll
                self.yStage -= self.p.yVel
                for sprite in self.allObjects:
                    if sprite in self.enemyBullets:
                        sprite.y -= self.p.yVel
                        sprite.yRel -= self.p.yVel
                    sprite.move(None,0,-self.p.yVel)

    #boolean var updates specific to the zone gamemode
    def zoneBoolUpdate(self):
        self.boolUpdate()
        if self.p.health <= 0: 
            self.p.kill()
            self.lose = True
            self.loseScreen()
        if self.zoneFlag and len(self.enemies) == 0: #no longer in zone mode
            self.zoneFlag = False
        elif self.bossFought and len(self.enemies) == 0:
            self.win = True
    
    #finds distance to the center of the zone and returns zone with lowest distance
    #also returns text indicating directions to go to get to zone
    def closestZone(self):
        closest = None
        closestDist = self.width * 2 #some arbitrary too large number
        zoneNum = 0
        closestText = ''

        #closest zone
        while zoneNum < len(self.zones):
            xStart,yStart,xEnd,yEnd = self.zones[zoneNum]
            xMid,yMid = (xStart + xEnd)/2,(yStart+yEnd)/2

            dist = math.sqrt( (self.p.xRel - xMid)**2 + (self.p.yRel - yMid)**2)

            if dist < closestDist:
                closest = zoneNum
                closestDist = dist
            
            zoneNum += 1

        #directions defined by distance in x and y from the player
        if len(self.zones) > 0:
            xStart,yStart,xEnd,yEnd = self.zones[closest]
            if xEnd < self.p.xRel:     horizText = 'left'
            elif self.p.xRel < xStart: horizText = 'right'
            else:                      horizText = ''

            if yEnd < self.p.yRel:     vertText = 'up'
            elif self.p.yRel < yStart: vertText = 'down'
            else:                      vertText = ''

            if horizText != '' and vertText != '':
                closestText = f"Go {horizText} and {vertText}."
            elif horizText == '' and vertText== '':
                closestText = ""
            else:
                direction = horizText if horizText != '' else vertText
                closestText = f"Go {direction}."

        return closestDist,closestText

    def zoneDraw(self):
        self.screen.fill(self.black)
        self.screen.blit(self.background,(0,0))  
        self.background.blit(self.image,(self.xStage,self.yStage))

        self.player.draw(self.background)
        self.allObjects.draw(self.background)

    #hud display for zone gamemode
    def zoneBlit(self):
        closestDist,dirText = self.closestZone()
        closestStatus = closestDist / max(self.width,self.height) #percent distance
        
        if not self.zoneFlag:
            if len(self.zones) == 0:
                text = 'Danger!!! A humungous super powered rat approaches! '
            elif closestStatus < .20:
                text = 'Entering rat zone. '
            elif closestStatus < .40:
                text = 'Rats are closeby! '
            elif closestStatus < .60:
                text = "Getting closer... "
            elif closestStatus < .75:
                text = 'Pretty quiet here... '
            else:
                text = 'No rats nearby... '

            text += dirText

            closestText = self.font.render(text,True,self.black,(255,255,255))
            closestRect = (0,self.yDim-self.font.size(text)[1]) + self.font.size(text)
            self.background.blit(closestText,closestRect)

        #top hud blit
        if self.pause:
            self.pauseScreen()
        if len(self.completedZones) == 0 and not self.zoneFlag:
            text = f'Objective: Clear all {len(self.zones)} rat clusters'
        elif self.zoneFlag:
            text = f'Rat Cluster {self.wave}'
        elif len(self.completedZones) != len(self.zones) + len(self.completedZones) and not self.zoneFlag:
            text = f'{self.wave}/{len(self.zones) + len(self.completedZones)} clusters cleared!'
        elif not self.bossFought:
            text = 'Head to center to fight boss rat!'
        elif self.bossFought and len(self.enemies) != 0:
            text = 'BOSS FIGHT WITH THE BIG RAT'
        elif self.win:
            text = 'YOU WIN!'
            self.winScreen()
        elif self.lose:
            text = 'You lose...'
            self.loseScreen()
        

        zoneText = self.font.render(text,True,self.black,(255,255,255))
        self.background.blit(zoneText,(0,60,100,100))

    #in zone mode, there are zones in the map. once those zones are entered,
    #a wave is started and enemies spawn. Once all zones are complete, a boss will appear
    def zoneMode(self):
    
        #if currently in a zone, another zone cannot be initiated
        if self.inGame:
            zoneIndex = 0
            while not self.zoneFlag and zoneIndex < len(self.zones):
                zone = self.zones[zoneIndex]
                lowX,lowY,highX,highY = zone
                if self.p.xRel in range(lowX,highX) and self.p.yRel in range(lowY,highY) or self.timer % 2000 == 0:
                    self.completedZones.add(zone)
                    self.zones.pop(zoneIndex)
                    self.initWave()
                    self.zoneFlag = True
                zoneIndex += 1 #ensures only one boss is spawned
            if len(self.zones) == 0 and self.bossFought == False and not self.zoneFlag:
                boss = Boss(self)
                self.enemies.add(boss)
                self.bossFought = True

        self.zoneBlit()
    
    

    


    
