from gameobject import GameObject
from bullets import *
from powerup import *
from healthbar import *
import pygame
import math
import random

#default enemy, can shoot straight and spray. More enemies defined below
class Enemy(GameObject):
    def __init__(self,screen,img,coords,health = 2):
        super().__init__(screen,img,coords)
        self.name = 'default'
        self.type = random.choice(['shootAt','spray','ram'])
        self.health = health
        self.healthBar = HealthBar(screen,(self.x + 5,self.y+10),self.health)
        self.deathImg = 'ratcage.png' #default death img

        if self.type == 'ram':
            self.velocity = (8,8)
            self.xVel,self.yVel = self.velocity

    def spray(self,group,amount=10):
        degreeStagger = 2 * math.pi / amount
        for indBullet in range(amount):
            b = Bullet(self.screen,'enemyBullet.png',(self.x,self.y),(self.x,self.y), degreeStagger * indBullet)
            b.velocity = (2,2)
            b.xVel, b.yVel = b.velocity
            group.add(b)

    def shootAt(self,whomst,enemyBullet,player):
        delta = (player.x-whomst.x,player.y-whomst.y)
        b = Bullet(self.screen,'enemyBullet.png',(whomst.x,whomst.y),delta)
        b.velocity = (2,2)
        b.xVel, b.yVel = b.velocity
        enemyBullet.add(b)
        

class RoadBlock(Enemy):
    def __init__(self,screen,img,coords,health = 2):
        super().__init__(screen,img,coords)
        self.name = 'road block'
        self.deathImg = 'dblock.png'
        self.type = None
        self.health = health
        self.healthBar = HealthBar(screen,(self.x + 5,self.y+10),self.health)
        
    #enemy update - movement, shooting, and bullet drop
    def update(self,player,enemyBullets,timer):
        
        if self.screen.dir == 'right': self.xRel -= 1
        elif self.screen.dir == 'left': self.xRel += 1
        elif self.screen.dir == 'up': self.yRel += 1
        elif self.screen.dir == 'down': self.yRel -= 1

        self.getDim()
        self.getRect()
        self.healthBar.update(self)

class Cat(Enemy):
    def __init__(self,screen,coords,health = 2):
        color = random.choice(['red','blue','green','orange'])
        self.img = color + 'cat.png' #rainbow cats 
        super().__init__(screen,self.img,coords)
        self.name = 'cat'
        self.deathImg = f'd{color}cat.png'
        self.velocity = (2.5,2.5)
        
        self.health = health
        self.healthBar = HealthBar(screen,(self.x + 5,self.y+10),self.health)
        self.image = pygame.transform.scale(self.image,(60,60))
        self.dir = 1 #pos or neg determines if it is moving up or down


    #cats will zigzag across the scrolling map
    def update(self,player,enemyBullets,timer):
        dist = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        timeMove = 40
        timeShoot = 75

        if timer % 120 == 0:
            self.dir = -self.dir
        
        rightFlag = self.screen.dir == 'right' or self.screen.dir == 'left'
        upFlag = self.screen.dir == 'up' or self.screen.dir == 'down'

        if rightFlag: 
            self.y += 3*self.dir
            self.yRel += 3*self.dir
        if upFlag:
            self.x += 3*self.dir 
            self.xRel += 3*self.dir
        
        if timer % timeShoot == 0 and self.type == 'spray' and dist < 300:
            self.spray(enemyBullets,5)
    
        elif timer % timeShoot == 0 and self.type == 'shootAt' and dist < 300:
            self.shootAt(self,enemyBullets,player)
        elif self.type == 'ram':
            self.move(player,3,3)
        elif timer % timeMove and dist >= 300:
            self.move(player)

        self.healthBar.update(self)
        self.getRect()
        self.getDim()
    

#default spawn in center of screen
class Boss(Enemy):
    def __init__(self,screen,img='boss.png',coord=(200,200)):
        super().__init__(screen,img,coord,20)
        self.name = 'boss'
        self.velocity = (4,4)
        self.xVel,self.yVel = self.velocity
        self.healthBar = BossHealthBar(screen,(self.x + 5,self.y+10),self.health)

    def update(self,player,enemyBullets,timer):

        #Focused enemy, heads straight for the player
        if timer % 60 == 0:
            self.spray(enemyBullets,10)
        elif timer % 40:
            self.move(player,3,3)

        self.healthBar.update(self)
        self.getRect()
        self.getDim()

#rats are small enemies with 2 health. They scurry around and shoot straight at the player
class Rat(Enemy):
    def __init__(self,screen,coords,health = 3):
        self.image = random.choice(['rat.png','angryrat.png'])
        super().__init__(screen,self.image,coords,health)
        self.name = 'rat'
        
    def update(self,player,enemyBullets,timer):
        dist = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        timeMove = 30        
        timeShoot = 120
        
        if timer % timeShoot == 0 and self.type == 'spray' and dist < 200:
            self.spray(enemyBullets,5)
            self.move(None,0,0,True)
        elif timer % timeShoot == 0 and self.type == 'shootAt' and dist < 200:
            self.shootAt(self,enemyBullets,player)
            self.move(None,0,0,True)
        elif self.type == 'ram':
            self.move(player,2,2)
        elif dist > 200:
            self.move(player,1,1,True)
            
        self.healthBar.update(self)
        self.getRect()
        self.getDim()
        



    




            
