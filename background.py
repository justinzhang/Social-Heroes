import pygame

#This code is all selfwritten with help from pygame documentation

#the building block for backgrounds/levels. Defines the basics needed to display pygame
class Background(pygame.sprite.Sprite):

    def __init__(self,res,image,caption='Social Heroes By Justin Zhang'):
        pygame.sprite.Sprite.__init__(self)

        #colors
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)

        self.res = res
        self.xDim,self.yDim = res
        self.screen = pygame.display.set_mode(res)
        self.background = pygame.Surface(res)
        self.font = pygame.font.Font('font/Fipps-Regular.otf', 24)
        self.smallFont = pygame.font.Font('font/Fipps-Regular.otf', 12)
        self.bigFont = pygame.font.Font('font/Fipps-Regular.otf', 40)
        self.image = self.imgLoad(image)
        
        self.width,self.height = self.image.get_size()
        pygame.display.set_caption(caption)

        #for scrolling backgrounds
        self.x,self.y = (0,0) 
        self.xDisplayRel = self.x
        self.yDisplayRel = self.y

        self.centerStage()
        
        self.xStartScroll,self.yStartScroll =(self.xDim // 2, (self.yDim) // 2)


    #same as game objects, for background images
    #must be in the background directory
    @staticmethod
    def imgLoad(img):
        playerImg = pygame.image.load(f"images/background/{img}").convert_alpha()

        return playerImg

    # I am very proud of this math that I did. Centers the stage in the middle of the map
    def centerStage(self):
        self.xStage,self.yStage= (self.xDim-self.width)/2,(self.yDim-self.height)/2


