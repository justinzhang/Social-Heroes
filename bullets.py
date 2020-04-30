import pygame
import math
from gameobject import GameObject
from powerup import *
import random

#This code is all selfwritten with help from pygame documentation

#bullet class, which both player and enemy uses. Different bullets with different speeds in this file
class Bullet(GameObject): #bullet initialized with either deltaXY or radians
    def __init__(self,screen,img,coords,direct,radians = False,bulletVelocity = (2.5,2.5)): 
        super().__init__(screen,img,coords,bulletVelocity)
        self.name = 'bullet'
        deltaX,deltaY = direct
        self.deathTime = 100
        if radians:
            self.angle = radians
        else:
            self.dist = math.sqrt(deltaX**2 + deltaY**2)
            self.angle = math.atan(deltaY/deltaX) if deltaX != 0 else 1
        self.screenTime = 0
        self.xChange = math.cos(self.angle) if deltaX >= 0 else -math.cos(self.angle)
        self.yChange = math.sin(self.angle) if deltaX >= 0 else -math.sin(self.angle)
    #different bullet trajections: straight and explosive
    def update(self,group):

        Xvelocity,Yvelocity = self.velocity
        self.xRel += self.xChange * Xvelocity
        self.yRel += self.yChange * Yvelocity
        self.x = self.xRel
        self.y = self.yRel
        self.getRect()
        self.screenTime += 1
        if self.screenTime == self.deathTime:
            pygame.sprite.Sprite.kill(self)

class RoadBullet(Bullet): #bullet but faster and longer screen time
    def __init__(self,screen,img,coords,direct,radians = False,bulletVelocity = (10,10)): 
        super().__init__(screen,img,coords,direct,radians,bulletVelocity)
        deltaX,deltaY = direct
        self.deathTime = 200
        
    def update(self,group):

        Xvelocity,Yvelocity = self.velocity
        self.xRel += self.xChange * Xvelocity
        self.yRel += self.yChange * Yvelocity
        self.getRect()
        self.screenTime += 1
        if self.screenTime == self.deathTime:
            pygame.sprite.Sprite.kill(self)



#this bullet explodes into different bullets
class MortarBullet(Bullet): #bullet initialized with either deltaXY or radians
    def __init__(self,screen,img,coords,direct,radians = False,bulletVelocity = (8,8)): 
        super().__init__(screen,img,coords,direct,radians,bulletVelocity)
        self.name = 'bullet'
        deltaX,deltaY = direct
        self.deathTime = 40

    def update(self,group):

        Xvelocity,Yvelocity = self.velocity
        self.x += self.xChange * Xvelocity
        self.y += self.yChange * Yvelocity
        self.getRect()
        self.screenTime += 1
        if self.screenTime == self.deathTime:
            degreeStagger = 2 * math.pi / 8
            for indBullet in range(0,30): #launches 30 bullets in different directions!
                b = Bullet(self.screen,'mortarpost.png',(self.x,self.y),(self.x,self.y), degreeStagger * indBullet)
                b.velocity = (12,12)
                b.xVel,b.yVel = b.velocity
                group.add(b)
            pygame.sprite.Sprite.kill(self)



            
            
            


