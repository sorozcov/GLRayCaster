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

    #Draw a reactangle
    def drawRectangle(self, x, y, color = WHITE):
        rectangle = (x, y, self.blocksize, self.blocksize)
        self.screen.fill(color, rectangle)

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
            if self.map[j][i] != ' ':
                return dist, self.map[j][i]
            self.screen.set_at((x,y), WHITE)
            dist += 5

    #Function to render our scene
    #This has to be called each time to update our scene
    def render(self):
        halfWidth = int(self.width / 2)
        halfHeight = int(self.height / 2)
        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':
                    self.drawRectangle(x, y, colors[self.map[j][i]])
        self.drawPlayerIcon(BLACK)

        for i in range(halfWidth):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / halfWidth
            dist, c = self.castRay(angle)
            x = halfWidth + i
            
            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle) * wallHeight
            try:
                h = self.height / (dist * cos( (angle - self.player['angle']) * pi / 180 )) * self.wallHeight

                start = int( halfHeight - h/2)
                end = int( halfHeight + h/2)

                for y in range(start, end):
                    self.screen.set_at((x, y), colors[c])
            except ZeroDivisionError:
                print("Error on wall")



        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), BLACK)
            self.screen.set_at( (halfWidth+1, i), BLACK)
            self.screen.set_at( (halfWidth-1, i), BLACK)


pygame.init()
screenWidth=1000
screenHeight=500
screen = pygame.display.set_mode((screenWidth,screenHeight)) #, pygame.FULLSCREEN)

rayCaster = Raycaster(screen)
rayCaster.setBlockColor( (128,0,0) )
rayCaster.loadMap('ownmap.txt')

isRunning = True

while isRunning:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            elif ev.key == pygame.K_w:
                rayCaster.player['x'] += cos(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
                rayCaster.player['y'] += sin(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
            elif ev.key == pygame.K_s:
                rayCaster.player['x'] -= cos(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
                rayCaster.player['y'] -= sin(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
            elif ev.key == pygame.K_a:
                rayCaster.player['x'] -= cos((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
                rayCaster.player['y'] -= sin((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
            elif ev.key == pygame.K_d:
                rayCaster.player['x'] += cos((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
                rayCaster.player['y'] += sin((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
            elif ev.key == pygame.K_q:
                rayCaster.player['angle'] -= 5
            elif ev.key == pygame.K_e:
                rayCaster.player['angle'] += 5

    screen.fill(BACKGROUND)
    rayCaster.render()

    
    pygame.display.flip()

pygame.quit()
