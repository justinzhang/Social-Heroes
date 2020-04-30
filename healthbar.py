import pygame
from gameobject import GameObject

red = (255,0,0)
green = (0,255,0)
minion = 5

#health bar displayed on top of enemies. green is remaining health.
class HealthBar(pygame.sprite.Sprite):

    def __init__(self,screen,coords,health = 5):
        pygame.sprite.Sprite.__init__(self)
        self.initHealth = health #this value will never change
        self.health = health
        self.screen = screen.background
        self.x,self.y = coords
        self.xDim,self.yDim = 20,5 #Adjustable
        self.getRemHealth()
        pygame.draw.rect(self.screen,red,(self.x,self.y,self.xDim,self.yDim))
        pygame.draw.rect(self.screen,green,(self.x,self.y,self.remHealthDim,self.yDim))
    
    #when implemented, pass enemy so you can get health
    def draw(self):
        pygame.draw.rect(self.screen,red,(self.x,self.y,self.xDim,self.yDim))
        pygame.draw.rect(self.screen,green,(self.x,self.y,self.remHealthDim,self.yDim))

    def getRemHealth(self):
        self.remHealthDim = int((self.health/self.initHealth) * self.xDim) #This changes based on the amount of health
        
    #updates based on mob
    def update(self,mob):
        self.health = mob.health
        self.x = mob.x - self.xDim / 2
        self.y = mob.y - self.yDim * 4
        self.getRemHealth()
        self.draw()

class BossHealthBar(pygame.sprite.Sprite):
    def __init__(self,screen,coords,health = 5):
        pygame.sprite.Sprite.__init__(self)
        self.initHealth = health #this value will never change
        self.health = health
        self.screen = screen.background
        self.x,self.y = coords
        self.xDim,self.yDim = 100,5 #Adjustable
        self.getRemHealth()
        pygame.draw.rect(self.screen,red,(self.x,self.y,self.xDim,self.yDim))
        pygame.draw.rect(self.screen,green,(self.x,self.y,self.remHealthDim,self.yDim))
    
    #when implemented, pass enemy so you can get health
    def draw(self):
        pygame.draw.rect(self.screen,red,(self.x,self.y,self.xDim,self.yDim))
        pygame.draw.rect(self.screen,green,(self.x,self.y,self.remHealthDim,self.yDim))

        

    def getRemHealth(self):
        self.remHealthDim = int((self.health/self.initHealth) * self.xDim) #This changes based on the amount of health
        
    #updates based on mob
    def update(self,mob):
        self.health = mob.health
        self.x = mob.x - self.xDim / 2
        self.y = mob.y - self.yDim * 8 #proportional to image
        self.getRemHealth()
        self.draw()

