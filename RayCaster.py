# -*- coding: utf-8 -*-
# Silvio Orozco 18282
# Universidad del Valle de Guatemala
# Gráficas por computadora
# Guatemala 15/10/2020
#  RayCasterayCaster.py

#This an implentation of a RayCaster using PyGame

import pygame
from math import cos, sin, pi



# Colors used in our RayCaster
BLACK = (0,0,0)
WHITE = (255,255,255)
BACKGROUND = (64,64,64)
# Colors used for RayCasting colors of maps
colors = {
    '1' : (106, 59, 3),
    '2' : (215, 117, 0),
    '3' : (255, 207, 149),
    '4' : (0, 20, 201),
    '5' : (133, 145, 255)
}

#Loading textures
textures = {
    '1' : pygame.image.load('wall6.png'),
    '2' : pygame.image.load('wall7.png'),
    '3' : pygame.image.load('wall8.png'),
    '4' : pygame.image.load('wall9.png'),
    '5' : pygame.image.load('wall10.png')
}


#Class Ray Caster
class Raycaster(object):
    #Init gets screen where it will render
    def __init__(self,screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        #Block size of each point in map
        self.blocksize = 50
        self.wallHeight = 50
        #Step size our player will be moving
        self.stepSize = 10
        #We set our block color
        self.setBlockColor(WHITE)

        #We create our player that has information of its position, angle of view and fov field of view
        self.player = {
            "x" : 120,
            "y" : 200,
            "angle" : 0,
            "fov" : 60
        }

    #Set Block Color
    def setBlockColor(self, color):
        self.blockColor = color

    #Load a map from a file
    def loadMap(self, filename):
        #We open file and read each line and append it to our self.map as a list
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))
        self.blocksize = int((self.width/2)/len(self.map))

    #Draw a reactangle
    def drawRectangle(self, x, y,texture=None):
        
        texture = pygame.transform.scale(texture, (self.blocksize, self.blocksize))
        rectangle=texture.get_rect()
        rectangle=rectangle.move((x,y))
        self.screen.blit(texture, rectangle)

    #Draw our players icon
    def drawPlayerIcon(self,color=BLACK):
        rectangle = (self.player['x'] - 2, self.player['y'] - 2, 6, 6)
        self.screen.fill(color, rectangle)

    #Function for casting a ray
    def castRay(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))
            i = int(x/self.blocksize)
            j = int(y/self.blocksize)
            #Verify where ray hits and return distance, texture and tx if hits
            if self.map[j][i] != ' ':
                hitX = x - i*self.blocksize
                hitY = y - j*self.blocksize

                if 1 < hitX < self.blocksize - 1:
                    maxHit = hitX
                else:
                    maxHit = hitY

                tx = maxHit / self.blocksize

                return dist, self.map[j][i], tx
                
            self.screen.set_at((x,y), WHITE)
            dist += 2

    #Function to render our scene
    #This has to be called each time to update our scene
    def render(self):
        halfWidth = int(self.width / 2)
        halfHeight = int(self.height / 2)
        #Half width for 2d View, halfwidth for 3D view
        #We first draw our map left
        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':
                    self.drawRectangle(x, y, texture=textures[self.map[j][i]])

        self.drawPlayerIcon(BLACK)

        #We draw our 3D World
        for i in range(halfWidth):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / halfWidth
            dist, textureType,tx = self.castRay(angle)
            x = halfWidth + i
            
            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle) * wallHeight
            try:
                h = self.height / (dist * cos( (angle - self.player['angle']) * pi / 180 )) * self.wallHeight

                start = int( halfHeight - h/2)
                end = int( halfHeight + h/2)
                texture = textures[textureType]
                tx = int(tx * texture.get_width())
                for y in range(start, end):
                    ty = (y - start) / (end - start)
                    ty = int(ty * texture.get_height())
                    textureColor = texture.get_at((tx, ty))
                    self.screen.set_at((x, y), textureColor)
            except ZeroDivisionError:
                print("Error on wall")



        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), BLACK)
            self.screen.set_at( (halfWidth+1, i), BLACK)
            self.screen.set_at( (halfWidth-1, i), BLACK)

#Init Pygame
pygame.init()
screenWidth=1000
screenHeight=500
screen = pygame.display.set_mode((screenWidth,screenHeight),pygame.DOUBLEBUF | pygame.HWACCEL) #, pygame.FULLSCREEN)
screen.set_alpha(None)

#Used to calculate FPS
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

rayCaster = Raycaster(screen)
rayCaster.setBlockColor( (128,0,0) )
rayCaster.loadMap('ownmap.txt')

isRunning = True

while isRunning:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        playerXpos = rayCaster.player['x']
        playerYpos = rayCaster.player['y']
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            elif ev.key == pygame.K_w:
                playerXpos += cos(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
                playerYpos += sin(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
            elif ev.key == pygame.K_s:
                playerXpos -= cos(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
                playerYpos -= sin(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
            elif ev.key == pygame.K_a:
                playerXpos -= cos((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
                playerYpos -= sin((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
            elif ev.key == pygame.K_d:
                playerXpos += cos((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
                playerYpos += sin((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
            elif ev.key == pygame.K_q:
                rayCaster.player['angle'] -= 5
            elif ev.key == pygame.K_e:
                rayCaster.player['angle'] += 5

            i = int(playerXpos / rayCaster.blocksize)
            j = int(playerYpos / rayCaster.blocksize)

            if rayCaster.map[j][i] == ' ':
                rayCaster.player['x'] = playerXpos
                rayCaster.player['y'] = playerYpos

    screen.fill(BACKGROUND)
    


    #Ceilign
    screen.fill(pygame.Color("skyblue"), (int(rayCaster.width / 2), 0, int(rayCaster.width / 2),int(rayCaster.height / 2)))
    
    #Floor
    screen.fill(pygame.Color("dimgray"), (int(rayCaster.width / 2), int(rayCaster.height / 2), int(rayCaster.width / 2),int(rayCaster.height / 2)))

    #Render RayCaster
    rayCaster.render()

    # FPS
    screen.fill(pygame.Color("black"), (0,0,30,30))
    screen.blit(updateFPS(), (10,5))
    clock.tick(30)  

    pygame.display.update()

pygame.quit()
