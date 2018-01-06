# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:07:20 2017

@author: esteban struve
"""

import pygame, sys 
from pygame.locals import *
import math
import csv
import numpy as np

file_reader= open('angles.csv', "rt")
read = csv.reader(file_reader)
co=0
listang=[0]*360
slopel=[0]*360
for row in read :
    if co!=0 and co < 360:
        listang[co]=float(row[0])
        slopel[co]=math.tan(math.radians(listang[co]))
    co+=1
# Define the colors we will use in RGB format
YELLOW = (255,   255,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

pygame.init()

size = width, height = 1216,830
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Aarhus Map")
layer = pygame.image.load("mapaarhus.png") 
cursor=pygame.image.load("arrow.png")
circul=pygame.image.load("boy.png")
ind=0
coordx,coordy=0,0
mousex,mousey=0,0
movex, movey=0,0
endx,endy=0,0
opx,opy=0,0
slope=0
angledeg=0
scale=30
#Draw the map in the screen
screen.blit(layer,(0,0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                print "izquierda"
                if ind > 0:
                    ind-=1
            elif event.key == K_RIGHT:
                print slope,endx,endy
                if ind <359:
                    ind+=1
    mousex,mousey=pygame.mouse.get_pos()
    mousex-=10
    mousey-=20
    angledeg=listang[ind]
    slope=slopel[ind]
    """ Chooses the end coordinates of the line according to angle"""
    if angledeg < 90.0:
        endy=0
        endx=(width/2)-((width/2)*slope)
        opy=height
        opx=(width/2)+((width/2)*slope)
        if endx<0:
            endy=(height/2)-((height/2)/slope)
            endx=0
        coordy=endy+(scale*angledeg*slope)
        coordx=endx+(scale*angledeg)
    elif angledeg < 180.0:
        if angledeg == 90:
            endy=height/2
            endx=0
            opy=height/2
            opx=width
        else:
            endy=height
            endx=(width/2)+((width/2)*slope)
            opy=0
            opx=(width/2)-((width/2)*slope)
            if endx<0:
                endy=(height/2)-((height/2)/slope)
                endx=0
    elif angledeg < 270.0:
        if angledeg == 180:
            endy=height
            endx=width/2
            opy=0
            opx=width/2
        else:
            endy=height
            endx=(width/2)+((width/2)*slope)
            opy=0
            opx=(width/2)-((width/2)*slope)
            if endx>width:
                endy=(height/2)+((height/2)/slope)
                endx=width
    elif angledeg < 360.0:
        if angledeg == 270:
            endy=height/2
            endx=width
            opy=height/2
            opx=0
        else:
            endy=0
            endx=(width/2)-((width/2)*slope)
            opy=height
            opx=(width/2)+((width/2)*slope)
            if endx>width:
                endy=(height/2)+((height/2)/slope)
                endx=width
    else:
        endy=0
        endx=width/2
        opy=0
        opx=width/2
    pygame.display.update()
    screen.blit(layer,(0,0))
    screen.blit(cursor,(mousex,mousey))
    screen.blit(circul,(endx,endy))
    pygame.draw.line(screen,YELLOW,(width/2,height/2),(opx,opy),3)
    pygame.draw.line(screen,GREEN,(width/2,height/2),(endx,endy),3)
    
    
    

