import pygame, sys
from pygame.locals import*

pygame.init()

width = 1200
height = 800
origin = 0
margin = 25
top_left = origin+margin, origin+margin
top_right = width-margin, origin+margin
bottom_left = origin+margin, height-margin
bottom_right = width-margin, height-margin

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)
FPS =60
Buffer = 25
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
Blocks = pygame.sprite.Group()

def draw_blocks():
    for block in Blocks:
        block.draw()

class Mover(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = width/2
        self.y = .9*height
        self.speed = 10
        self.size = 100
        self.current_pos = (self.x, self.x+self.size)
    def draw(self):
        pygame.draw.rect(screen,BLUE,(self.x,self.y,self.size,5))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.new_x = self.x + self.speed
            if self.new_x >=Buffer and self.new_x<=width-Buffer-self.size:
                self.x = self.new_x
        if keys[pygame.K_LEFT]:
            self.new_x = self.x - self.speed
            if self.new_x >=Buffer and self.new_x<=width-Buffer-self.size:
                self.x = self.new_x
        self.draw()

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,color,width,height):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color 
        self.width = width 
        self.height = height
        self.rect = Rect(self.x,self.y,self.width,self.height)
        Blocks.add(self)        

    def draw(self):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.height))

class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,color,x_speed,y_speed,size):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.x_speed = x_speed 
        self.y_speed = y_speed
        self.size = size
        self.hit_count = 0
        self.rect = Rect(self.x,self.y,self.size,self.size)        
        
    def draw(self):        
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.size)
    def collide(self):
        # check collisions with rectangles, if collision, return True, else return False
        if Blocks:
            for block in Blocks:
                if self.rect.colliderect(block.rect):            
                    block.kill()
                    return True            
        return False
            
    def update(self):
        self.new_x = self.x + self.x_speed
        self.new_y = self.y + self.y_speed
        
        if self.collide() == False:
            if self.new_x >=Buffer and self.new_x<=width-Buffer-self.size:
                self.x = self.new_x
            else:
                self.x_speed *=-1
            if self.new_y >=Buffer:
                self.y = self.new_y
            else:
                self.y_speed *=-1            
        else:
            # TODO check where collision happened on the ball relative to the rectangle and change speeds
            self.y_speed *=-1

        self.rect = Rect(self.x,self.y,self.size,self.size) 
        self.draw()

bl = Block(200,150,RED,50,10)
b = Ball(200,200,BLUE,1,-1,15)
m= Mover()
while True:
    
    clock.tick(FPS)
    screen.fill(WHITE)
    
    draw_blocks()
    m.update()
    b.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
          
    pygame.display.flip()
           