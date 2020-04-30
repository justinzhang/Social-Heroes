import pygame
import random
from gameobject import GameObject

#This code is all selfwritten with help from pygame documentation


class PowerUp(GameObject):

    #returns a random powerup from all powerups
    #inclGen: include general powerups like shield and health
    #inclGun: include gun powerups like machinegun and shotgun
    @staticmethod
    def randomUp(screen,coords,inclGen=True,inclGun=True):
        powerList = list()
        if inclGen: powerList += [Shield(screen,coords),Health(screen,coords),Speed(screen,coords)]    
        if inclGun: powerList += [Machinegun(screen,coords),Shotgun(screen,coords),Mortargun(screen,coords)]
        power = random.choice(powerList)
        return power

    def __init__(self,screen,img,coords):
        super().__init__(screen,img,coords)
        
        
#These are general powerups, affecting the player's stats
class Speed(PowerUp):
    def __init__(self,screen,coords,img='speed.png'):
        super().__init__(screen,img,coords)


    def effect(self,player):

        player.xVel = player.xVel + .26 if player.xVel > 0 else player.xVel - .26
        player.yVel = player.yVel + .26 if player.yVel > 0 else player.yVel - .26
        


#shield blocks 5 bullets each, with each shot shield loses transparancy
class Shield(PowerUp):
    def __init__(self,screen,coords,img='shield.png'):
        super().__init__(screen,img,coords)


    def effect(self,player):

        player.shield = 5
        player.status = 'shield'

class Health(PowerUp):
    def __init__(self,screen,coords,img='health.png'):
        super().__init__(screen,img,coords)
    
    def effect(self,player):
        if player.health + 5 > 20: player.health = 20
        else: player.health += 5

#The following powerups are gun based ie they give you a different gun
class Machinegun(PowerUp):
    def __init__(self,screen,coords,img='machinegunp.png'):
        super().__init__(screen,img,coords)

    def effect(self,player):
        player.gunType = 'machine'
        player.amountBullets = player.bulletDic[player.gunType]
        player.maxBullets = player.bulletDic[player.gunType]
        player.gunImg = player.machImg

class Shotgun(PowerUp):
    def __init__(self,screen,coords,img='shotgunp.png'):
        super().__init__(screen,img,coords)

    def effect(self,player):
        player.gunType = 'shotgun'
        player.amountBullets = player.bulletDic[player.gunType]
        player.maxBullets = player.bulletDic[player.gunType]
        player.gunImg = player.shotImg

class Mortargun(PowerUp):
    def __init__(self,screen,coords,img='mortarp.png'):
        super().__init__(screen,img,coords)
    def effect(self,player):
        player.gunType = 'mortar'
        player.amountBullets = player.bulletDic[player.gunType]
        player.maxBullets = player.bulletDic[player.gunType]
        player.gunImg = player.mortImg








