import pygame
import math
from gameobject import *
from bullets import *

#This code is all selfwritten with help from pygame documentation

#player can shoot bullets by clicking screen
#wasd movement
class Player(GameObject):
    health = 20 #default health, changed only by upgrades
    bulletDic = {'pistol':1,'machine':60,'shotgun':10,'mortar':5}

    #preload images. one for each eight direction
    def preload(self):
        self.up = GameObject.imgLoad('upPlayer.png',True)
        self.down = GameObject.imgLoad('downPlayer.png',True)
        self.left = GameObject.imgLoad('leftPlayer.png',True)
        self.right = GameObject.imgLoad('rightPlayer.png',True)
        self.upRight = GameObject.imgLoad('upRightPlayer.png',True)
        self.upLeft = GameObject.imgLoad('upLeftPlayer.png',True)
        self.downRight = GameObject.imgLoad('downRightPlayer.png',True)
        self.downLeft = GameObject.imgLoad('downLeftPlayer.png',True)

        self.pistImg = GameObject.imgLoad('pistol.png')
        self.machImg = GameObject.imgLoad('machinegun.png')
        self.shotImg = GameObject.imgLoad('shotgun.png')
        self.mortImg = GameObject.imgLoad('mortar.png')

    def __init__(self,screen,coords,img='upPlayer.png'):
        self.velocity = (2.5,2.5)
        super().__init__(screen,img,coords,self.velocity)
        
        
        self.health = 20
        self.shield = 0
        self.justShot = False
        self.timeSinceShot = 0
        self.preload()
        self.gunType = 'pistol'
        self.amountBullets = Player.bulletDic[self.gunType]
        self.maxBullets = self.amountBullets
        self.gunImg = self.pistImg

        self.healthUpdate()
        self.bulletUpdate()

#generalized shooting for all different weapons
#modular, just add functionality here
    def genShoot(self,mousePos,bulletGroup,timer,isShooting=False):
        if self.amountBullets > 0 and isShooting:
            if self.gunType == 'pistol' and not self.justShot:
                self.bulletShoot(mousePos,bulletGroup)
                self.justShot = True
                self.timeSinceShot = 0
            if self.gunType == 'shotgun' and not self.justShot:
                self.spray(mousePos,bulletGroup)
                self.amountBullets -= 1
                self.justShot = True
                self.timeSinceShot = 0
            if self.gunType == 'machine' and timer % 15 == 0:
                self.amountBullets -= 1
                self.bulletShoot(mousePos,bulletGroup)
                self.timeSinceShot = 0
            if self.gunType == 'mortar' and not self.justShot and self.timeSinceShot > 60:
                self.amountBullets -= 1
                self.mortarShot(mousePos,bulletGroup)
                self.timeSinceShot = 0
                self.justShot = True


    #initializes a bullet from player location
    def bulletShoot(self,where,bulletGroup):
        x0,y0 = where
        deltaX,deltaY = x0 - self.x, y0 - self.y
        b = Bullet(self.screen,'bullet.png',(self.x,self.y),(deltaX,deltaY),False)
        b.velocity = (10,10)
        b.xVel, b.yVel = b.velocity

        bulletGroup.add(b)


    def spray(self,where,group,amount=4):
        x0,y0 = where
        deltaX,deltaY = x0 - self.x, y0 - self.y
        
        for offset in range(-amount*2,amount*2,4): #mult. by 2, better spread
            radianMode = (deltaX+amount*offset,deltaY+amount*offset)
            b = Bullet(self.screen,'bullet.png',(self.x,self.y),radianMode)
            group.add(b)

    #basically a bullet that shoots straight then exploads in a circular spray ie just like enemy spray
    def mortarShot(self,where,group):
        x0,y0 = where
        deltaX,deltaY = x0 - self.x, y0 - self.y
        b = MortarBullet(self.screen,'mortarpre.png',(self.x,self.y),(deltaX,deltaY),False)
        group.add(b)

    #update health amount text
    def healthUpdate(self):
        color = (255,0,0) if self.health <= 5 else (0,0,0)
        self.hText = self.screen.font.render(f'Health:{self.health}/{Player.health}', True, color,(255,255,255))
        self.hTextRect = self.hText.get_rect()

    #pistols shoot infinite amount of bullets, when gun is picked up, change text
    def bulletUpdate(self):
        if self.gunType == 'pistol':
            self.bText = self.screen.font.render("Ammo:Inf/Inf",True, (0,0,0),(255,255,255))
        else:
            color = (255,0,0) if self.amountBullets <= 5 else (0,0,0)
            self.bText = self.screen.font.render(f'Ammo:{self.amountBullets}/{self.maxBullets}', True, color,(255,255,255))
        
        self.bTextRect = self.hText.get_rect(right = self.screen.xDim - 200) 

        #gun img blitting
        self.gunRect = (self.screen.xDim - self.gunImg.get_rect().width,0) + (self.gunImg.get_rect().width,self.gunImg.get_rect().height)

        

    #nice cheat codes
    def devTest(self,keys):
        if keys[pygame.K_1]:
            self.gunType = 'pistol'
            self.gunImg = self.pistImg
            self.maxBullets = self.bulletDic[self.gunType]
            self.amountBullets = self.maxBullets            
        if keys[pygame.K_2]:
            self.gunType = 'machine'
            self.gunImg = self.machImg
            self.maxBullets = self.bulletDic[self.gunType]
            self.amountBullets = self.maxBullets
        if keys[pygame.K_3]:
            self.gunType = 'shotgun'
            self.gunImg = self.shotImg
            self.maxBullets = self.bulletDic[self.gunType]
            self.amountBullets = self.maxBullets
        if keys[pygame.K_4]:
            self.gunType = 'mortar'
            self.gunImg = self.mortImg
            self.maxBullets = self.bulletDic[self.gunType]
            self.amountBullets = self.maxBullets
        if keys[pygame.K_0]:
            self.health = Player.health
        if keys[pygame.K_9]:
            self.xVel = self.xVel + .25 if self.xVel > 0 else self.xVel - .25
            self.yVel = self.yVel + .25 if self.yVel > 0 else self.yVel - .25
            self.velocity = (abs(self.xVel),abs(self.yVel))

    def update(self,horiz=1,vert=1,timer=1):
        keys = pygame.key.get_pressed()
        xUpdate = 0
        yUpdate = 0
        self.imgUpdate(keys)
        self.timeSinceShot += 1
        
        if keys[pygame.K_w]:
            self.yVel = -abs(self.yVel)
            yUpdate = vert*self.yVel

        if keys[pygame.K_s]:
            self.yVel = abs(self.yVel)
            yUpdate = vert*self.yVel
            
        if keys[pygame.K_a]:
            self.xVel = -abs(self.xVel)
            xUpdate = horiz*self.xVel
            
        if keys[pygame.K_d]:
            self.xVel = abs(self.xVel)
            xUpdate = horiz*self.xVel
        self.xRel += xUpdate
        self.yRel += yUpdate

        if keys[pygame.K_ESCAPE]:
            self.screen.pause = True
            print('paused')

        if timer % 100 == 0 and self.amountBullets > self.maxBullets:
            self.amountBullets -= 1

        self.devTest(keys)
        self.getRect()
        self.getDim()
        self.healthUpdate()
        self.bulletUpdate()
        self.effectUpdate()

        #this is the hud
        pygame.draw.rect(self.screen.background,(255,255,255),(0,0,self.screen.xDim,60))
        self.screen.background.blit(self.hText,self.hTextRect)
        self.screen.background.blit(self.bText,self.bTextRect)
        self.screen.background.blit(self.gunImg,self.gunRect)
            

        
    
    #based on powerup/status of player, certain effects will show up
    def effectUpdate(self):
        if self.shield > 0:
            shieldText = self.screen.smallFont.render(f"{self.shield}",True,(50,0,200),pygame.SRCALPHA)
            center = (int(self.x),int(self.y))
            textRect = (int(self.x + self.xDim),int(self.y)) + self.screen.smallFont.size(f'{self.shield}')
            pygame.draw.circle(self.screen.background,(50,0,200,0),center,int(self.radius*1.1),1)
            self.screen.background.blit(shieldText,textRect)

        #bullet effects
        self.maxBullets = self.bulletDic[self.gunType]
        if self.amountBullets == 0:
            self.gunType = 'pistol'
            self.gunImg = self.pistImg
            self.amountBullets = self.bulletDic[self.gunType]
            self.maxBullets = self.amountBullets



    def imgUpdate(self,keys):
        
        if keys[pygame.K_w]:
               self.image = self.up
        if keys[pygame.K_s]:
           self.image = self.down
        if keys[pygame.K_a]:
           self.image = self.left
        if keys[pygame.K_d]:
           self.image = self.right
        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.image = self.upRight
        if keys[pygame.K_w] and keys[pygame.K_a]:
            self.image = self.upLeft
        if keys[pygame.K_s] and keys[pygame.K_d]:
            self.image = self.downRight
        if keys[pygame.K_s] and keys[pygame.K_a]:
            self.image = self.downLeft
        
    def takeDamage(self,damageNum):
        if self.shield > 0:
            if self.shield > damageNum:
                self.shield -= damageNum
            else:
                self.health -= (damageNum - self.shield)
                self.shield = 0
        else:
            self.health -= damageNum
                


class RoadPlayer(Player):
    health = 20 #default health, changed only by upgrades
    bulletDic = {'pistol':1,'machine':60,'shotgun':10,'mortar':5}

    #preload images. one for each eight direction
    def preload(self):
        self.up = GameObject.imgLoad('upPlayer.png',True)
        self.down = GameObject.imgLoad('downPlayer.png',True)
        self.left = GameObject.imgLoad('leftPlayer.png',True)
        self.right = GameObject.imgLoad('rightPlayer.png',True)
        self.upRight = GameObject.imgLoad('upRightPlayer.png',True)
        self.upLeft = GameObject.imgLoad('upLeftPlayer.png',True)
        self.downRight = GameObject.imgLoad('downRightPlayer.png',True)
        self.downLeft = GameObject.imgLoad('downLeftPlayer.png',True)

        self.pistImg = GameObject.imgLoad('pistol.png')
        self.machImg = GameObject.imgLoad('machinegun.png')
        self.shotImg = GameObject.imgLoad('shotgun.png')
        self.mortImg = GameObject.imgLoad('mortar.png')

    def __init__(self,screen,coords,img='upPlayer.png'):
        super().__init__(screen,coords,img)
        self.velocity = (4,4)
        self.xVel,self.yVel = self.velocity



    #inits a road bullet instead of a normal bullet, for autoscroll levels
    def bulletShoot(self,where,bulletGroup):
        x0,y0 = where
        deltaX,deltaY = x0 - self.x, y0 - self.y
        bulletGroup.add(RoadBullet(self.screen,'bullet.png',(self.x,self.y),(deltaX,deltaY),False,(10,10)))
        
    def spray(self,where,group,amount=4):
        x0,y0 = where
        deltaX,deltaY = x0 - self.x, y0 - self.y
        
        for offset in range(-amount*2,amount*2,4): #mult. by 2, better spread
            radianMode = (deltaX+amount*offset,deltaY+amount*offset)
            b = RoadBullet(self.screen,'bullet.png',(self.x,self.y),radianMode)
            group.add(b)

    

    



        
        

    
