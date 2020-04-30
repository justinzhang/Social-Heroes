import random
import pygame
from background import Background
from player import *
from enemies import *
from powerup import *
from gameobject import GameImage


#level class, essentials for each level, built off of background
class Level(Background):
    def preset(self):
        self.name='default'
        self.clock = pygame.time.Clock()
        self.player = pygame.sprite.GroupSingle()
        self.enemyBullets = pygame.sprite.Group()
        self.yourBullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group() 
        self.enemies = pygame.sprite.Group()
        self.gameImages= pygame.sprite.Group()
        self.allObjects = pygame.sprite.Group()
        self.playing = True
        self.pause = False
        self.inGame = True
        self.pShooting = False
        self.timer = 0
        self.bossFought = False
        self.win = False
        self.lose = False
        self.deathLoc = set() #here if blitting image upon death is needed

        #text blitting sucks, all this is required to draw menu text

        #win
        text = 'YOU WON'
        giveUp = 'Main Menu'
        self.winText = self.font.render(text,True,self.black,pygame.SRCALPHA)
        self.giveupText =  self.font.render(giveUp,True,self.black,self.red)
        self.winRect = (self.xDim/4 + 50, self.yDim/4 + 50,self.xDim/2,self.yDim/2)
        self.statRect = (self.xDim/4 ,self.yDim/4 + 100, self.xDim/2,self.yDim/2)
        self.boxRect = (0,self.yDim/4,self.xDim,self.yDim/2)
        self.mainUpRect = (self.xDim//2,self.yDim - 300) + self.font.size(giveUp)

        #pause
        paused = 'Paused'
        unpause = 'Resume Game'
        title = 'Return to Title'

        self.pausedText = self.font.render(paused,True,self.black,pygame.SRCALPHA)
        self.unPauseText = self.font.render(unpause,True,self.black,self.green)
        self.titleText =  self.font.render(title,True,self.black,self.red)
        
        self.pausedRect = (self.xDim/2 - self.font.size(paused)[0]/2, self.yDim/4 + 50) + self.font.size(paused)
        self.unPauseRect = (self.xDim/8 ,self.yDim - 300) + self.font.size(unpause)
        self.titleRect = (self.xDim/2,self.yDim - 300) + self.font.size(title)

        #lose
        lose = 'GAME OVER'
        tryT = 'Try Again'
        giveUp = 'Main Menu'

        self.boxRect =(0,self.yDim//4,self.xDim,self.yDim//2)
        self.tryRect = (self.xDim//4,self.yDim//3) + self.font.size(tryT)
        self.giveUpRect = (self.xDim//2,self.yDim//3) + self.font.size(giveUp)
        self.loseText = self.font.render(lose,True,self.black,self.white)
        self.tryText = self.font.render(tryT,True,self.black,(0,255,0))
        self.giveupText =  self.font.render(giveUp,True,self.black,self.red)

    def __init__(self,res,img):
        super().__init__(res,img)
        self.preset()

    #initialize player in the center of the screen
    def initPlayer(self,res):
        xCenter,yCenter = res[0]//2,res[1]//2
        #although this is added to the sprite group, I have
        #to keep it because of weird attribute retainment in pygame
        self.p = RoadPlayer(self,(xCenter,yCenter)) if self.name == 'autoscroll' else Player(self,(xCenter,yCenter))
        self.player.add(self.p)
        #player needed in all objects if autoscrolled background
        if self.name == 'autoscroll': self.allObjects.add(self.p)
        
        self.p.xRel, self.p.yRel = self.width/2,self.height/2
        self.p.x,self.p.y = self.xDim / 2, self.yDim / 2

    #sets clock tick rate and upkeeps timer
    def timeTick(self,rate=120):
        self.clock.tick(rate)
        if self.inGame: self.timer += 1
        if self.inGame: self.time = self.timer // 120

    
    #update all true/false vars here
    #this is going to be pretty small since many conditionals are gamemode based
    def boolUpdate(self):
        self.inGame = (not self.win and not self.lose) and not self.pause
        #lose condition
        if self.p.health <= 0 or len(self.player) < 1: self.lose = True

    #general forLoop
    def forLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pShooting = True
                mousePos = pygame.mouse.get_pos()
                if self.win == True:
                    self.winMenu(mousePos)
                if self.lose == True:
                    self.loseMenu(mousePos)
                if self.pause == True:
                    self.pauseMenu(mousePos)

            if event.type == pygame.MOUSEBUTTONUP:
                self.pShooting = False
                self.p.justShot = False

            
            if event.type == pygame.QUIT:
                self.playing = False
        

    #all sprite group (except player) is used for mostly screen moving funcs
    def groupAdd(self):
        for sprite in self.enemyBullets:
            if sprite not in self.allObjects:
                self.allObjects.add(sprite)

        for sprite in self.yourBullets:
            if sprite not in self.allObjects:
                self.allObjects.add(sprite)

        for sprite in self.powerups:
            if sprite not in self.allObjects:
                self.allObjects.add(sprite)

        for sprite in self.enemies:
            if sprite not in self.allObjects:
                self.allObjects.add(sprite)
    
    #update the player in updateloop
    def playerUpdates(self):
        if self.inGame:
            self.player.update(1,1,self.timer)
            self.p.genShoot(pygame.mouse.get_pos(),self.yourBullets,self.timer,self.pShooting)
            self.yourBullets.update(self.yourBullets)


    #each enemy is updated individually based on enemy type
    def enemyUpdates(self):
        if self.inGame:
            self.enemyBullets.update(self.enemyBullets)
            for enemy in self.enemies:
                enemy.update(self.p,self.enemyBullets,self.timer)

    #uses random to determine if a powerup drops at the coords listed
    #see powerup.py for additional documentation
    def powerSpawn(self,coords,incGen=True,incGun=True):
        spawned = PowerUp.randomUp(self,coords,incGen,incGun)
        self.powerups.add(spawned)


    def playerPowerInteractions(self):
        pickUp = pygame.sprite.groupcollide(self.powerups,self.player,True,False)
        for powerup,player in pickUp.items():
                powerup.effect(self.p)
        
    def playerEnemyInteractions(self):
        if pygame.sprite.groupcollide(self.player,self.enemyBullets,False,True):
            if self.bossFought:
                self.p.takeDamage(2)
            else:
                self.p.takeDamage(1)

        epInteraction = pygame.sprite.groupcollide(self.enemies,self.player,False,False)
        for enemy,player in epInteraction.items():
            self.p.takeDamage(1)
            if enemy.name != 'boss':
                pygame.sprite.Sprite.kill(enemy)
                enemy.health -= 1 
    

        
            

        enemyHit = pygame.sprite.groupcollide(self.enemies,self.yourBullets,False,True)
        
        for enemy,bullet in enemyHit.items():
            enemy.health -= 1
            if enemy.health <= 0:
                spawn = random.randint(0,4) == 1
                if spawn: self.powerSpawn((enemy.x,enemy.y))
                deathImg = GameImage(self,enemy.deathImg,(enemy.x,enemy.y))
                self.gameImages.add(deathImg)
                self.allObjects.add(deathImg)
                self.deathLoc.add((enemy.x,enemy.y))
                self.p.amountBullets += 1
                
                pygame.sprite.Sprite.kill(enemy)

    def pauseScreen(self):
        pygame.draw.rect(self.background,self.white,self.boxRect)
        self.background.blit(self.pausedText,self.pausedRect)
        self.background.blit(self.unPauseText,self.unPauseRect)
        self.background.blit(self.titleText,self.titleRect)



    

    def winScreen(self):
        stats = f'Time Elapsed: {self.time} seconds'
        nextLevel = 'Next Level' if self.l2 == False else 'You beat the game!'

        self.statText = self.font.render(stats,True,self.black,pygame.SRCALPHA)
        self.nextLevelText = self.font.render(nextLevel,True,self.black,(10,255,0))
        self.nextLevelRect = (self.xDim/5,self.yDim - 300) + self.font.size(nextLevel)
        
        
        pygame.draw.rect(self.background,self.white,self.boxRect)
        self.background.blit(self.winText,self.winRect)
        self.background.blit(self.statText,self.statRect)
        self.background.blit(self.nextLevelText,self.nextLevelRect)
        self.background.blit(self.giveupText,self.mainUpRect)

    def loseScreen(self):
        if self.lose:
            pygame.draw.rect(self.background,self.white,self.boxRect)

            self.background.blit(self.loseText,self.boxRect)
            self.background.blit(self.tryText,self.tryRect)
            self.background.blit(self.giveupText,self.giveUpRect)

#menu functions are the functionality of the win/lose screens
#therefore, they will be defined in respective levels due to different vars


    




        


    

