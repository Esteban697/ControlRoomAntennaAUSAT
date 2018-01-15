# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:07:20 2017

@author: esteban struve
"""

import pygame, sys 
from pygame.locals import *
import math
import csv

#Read a csv file with the angle information
original = file('angles.csv')
reader = csv.reader(original)
listang = reader.next()
listincl = reader.next()
#The information about the slope direction of antenna in map - Azimut
slopel= [0] * len(listang)
azangles= [0] * len(listang)
for i in range(len(listang)):
    azangles[i]=float(listang[i])
    slopel[i]=math.tan(math.radians(azangles[i]))
#Store the inclination azangles as floats - Elevation
elevangles= [0] * len(listincl)
for j in range(len(listincl)):
    elevangles[j]=float(listincl[j])
# Define the colors we will use in RGB format
YELLOW= (255, 255,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
BLUE2 = (204, 222, 243)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
ORANGE= (255, 154,   0)
BLACK = (  0,   0,   0)
#Start the pygame interface
pygame.init()
#Initialize values for the visual interface
#Setting screen
mapsize = width, height = 930,930
screensize = 1400,930
screen = pygame.display.set_mode(screensize)
margin = width+50
#Loading image objects
pygame.display.set_caption("Aarhus Map")
layer = pygame.image.load("mapaarhusn.png") 
cursor=pygame.image.load("arrow.png")
margmarkx1=pygame.image.load("marginmarkerx1.png")
margmarkx2=pygame.image.load("marginmarkerx2.png")
margmarky1=pygame.image.load("marginmarkery1.png")
margmarky2=pygame.image.load("marginmarkery2.png")
circul=pygame.image.load("bluecircle.png")
#Initializing variables for visual objects
linerange=180
m=0
ind1=0
ind2=0
coordx,coordy=0,0
mousex,mousey=0,0
movex, movey=0,0
endx,endy=0,0
opx,opy=0,0
slope=0
angledeg=0
elevang=0
seconds=0
timer=0
myfont=pygame.font.SysFont("Arial Black",20)
myfont2=pygame.font.Font(None,20)
timerrun=False
clock=pygame.time.Clock()
timerdisp=0
#This scale is based on the map size to point the sky correctly
scale=5
#Draw the map in the screen
screen.blit(layer,(0,0))
while True:
    if timerrun == True:
        seconds=clock.get_time()/1000.0
        timer+=seconds
        timerdisp=math.trunc(timer)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() #Exit execution when closing wind1ow
        #You can use the left-right keys to change de direction angle
        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT: #When left key gets pressed
                if ind1 > 0: #safe limits
                    ind1-=1
                    print angledeg,linerange
            elif event.key == K_RIGHT: #when right key gets pressed
                if ind1 <(len(listang)-1): #safe limits
                    ind1+=1
                    print angledeg,linerange
            #You can use the up-down keys to change de inclination angle
            elif event.key == K_UP: #When up key gets pressed
                if ind2 > 0: #safe limits
                    ind2-=1
                    print m,coordx,coordy
            elif event.key == K_DOWN: #when down key gets pressed
                if ind2 <(len(listincl)-1): #safe limits
                    ind2+=1
                    print m,coordx,coordy
    #Get information from the mouse
    clicked=pygame.mouse.get_pressed()
    mousex,mousey=pygame.mouse.get_pos() #gets the position of the cursor
    globmx,globmy=mousex,mousey
    #coordinates for map
    if mousex > width:
        mousex=width
    elif mousex < 0:
        mousex=0
    if mousey > height:
        mousey=height
    elif mousey < 0:
        mousey=0
    #coordinates for cursor arrow to allign to arrow tip
    arrowx=mousex-10
    arrowy=mousey-20
    #Choose an angle and slope from the list created by the csv file
    angledeg=azangles[ind1]
    slope=slopel[ind1]
    elevang=elevangles[ind2]
    #Chooses the end coordinates of each line to be drawn according to angle
    #When angle between 0 and 89
    if angledeg < 90.0:
        endy=0
        endx=(width/2)-((width/2)*slope)
        if endx<0:
            endy=(height/2)-((height/2)/slope)
            endx=0
        opy=height-endy
        opx=width-endx
        #Calculate the (x,y) coordinates in the line according to inclination
        if (endx-opx)!=0:
            m=((endy-opy)/(endx-opx))
        #linerange=130*math.cos(math.radians(angledeg))
        linerange=180
        coordx=endx-(((endx-opx)/linerange)*elevang)
        coordy=endy-((m*((endx-opx)/linerange))*elevang)
    #When angle between 90 and 179
    elif angledeg < 180.0:
        if angledeg == 90:
            endy=height/2
            endx=0
            opy=height/2
            opx=width
        else:
            endy=height
            endx=(width/2)+((width/2)*slope)
            if endx<0:
                endy=(height/2)-((height/2)/slope)
                endx=0
        opy=height-endy
        opx=width-endx
        #Calculate the (x,y) coordinates in the line according to inclination
        if (endx-opx)!=0:
            m=((endy-opy)/(endx-opx))
        coordx=endx-(((endx-opx)/180)*elevang)
        coordy=endy-((m*((endx-opx)/180))*elevang)
    #When angle between 180 and 269
    elif angledeg < 270.0:
        if angledeg == 180:
            endy=height
            endx=width/2
            opy=0
            opx=width/2
        else:
            endy=height
            endx=(width/2)+((width/2)*slope)
            if endx>width:
                endy=(height/2)+((height/2)/slope)
                endx=width
            opy=height-endy
            opx=width-endx
            #Calculate the (x,y) coordinates in the line according to inclination
            if (endx-opx)!=0:
                m=((endy-opy)/(endx-opx))
            coordx=endx-(((endx-opx)/180)*elevang)
            coordy=endy-((m*((endx-opx)/180))*elevang)
    #When angle between 270 and 359
    elif angledeg < 360.0:
        if angledeg == 270:
            endy=height/2
            endx=width
            opy=height/2
            opx=0
        else:
            endy=0
            endx=(width/2)-((width/2)*slope)
            if endx>width:
                endy=(height/2)+((height/2)/slope)
                endx=width
            opy=height-endy
            opx=width-endx
            #Calculate the (x,y) coordinates in the line according to inclination
            if (endx-opx)!=0:
                m=((endy-opy)/(endx-opx))
            coordx=endx-(((endx-opx)/180)*elevang)
            coordy=endy-((m*((endx-opx)/180))*elevang)
    #When angle exactly 360
    else:
        endy=0
        endx=width/2
        opy=0
        opx=width/2
    #The screen is updated by:
    pygame.display.update()
    #Black background
    screen.fill(BLACK)
    #Draw map again
    screen.blit(layer,(0,0))
    #Draw the lines
    pygame.draw.line(screen,YELLOW,(width/2,height/2),(opx,opy),3)
    pygame.draw.line(screen,GREEN,(width/2,height/2),(endx,endy),3)
    #Create text right side of screen
    texttit1=myfont.render("Angle values for antenna position:",0,ORANGE)
    textang1=myfont.render("Azimut: "+str(angledeg)+" degrees",0,GREEN)
    textang2=myfont.render("Elevation: "+str(elevang)+" degrees",0,BLUE)
    texttit2=myfont.render("Position of cursor:",0,ORANGE)
    texttit3=myfont.render("Time:",0,ORANGE)
    textcursor=myfont.render("X: "+str(mousex)+" Y: "+str(mousey),0,YELLOW)
    texttime=myfont.render(str(timerdisp)+" seconds",0,YELLOW)
    textbut1=myfont.render("Play",0,BLACK)
    textbut2=myfont.render("Playing",0,BLACK)
    textbut3=myfont.render("Stop",0,BLACK)
    #Draw cursor margin markers
    screen.blit(margmarkx1,(0,mousey-11))
    screen.blit(margmarkx2,(width-30,mousey-11))
    screen.blit(margmarky1,(mousex-11,0))
    screen.blit(margmarky2,(mousex-11,height-30))
    #Create angle value inside circle
    textcirc=myfont2.render(str(int(elevang)),0,BLUE2)
    textcircshad=myfont2.render(str(int(elevang)),0,BLACK)
    #Draw text on the right side of the screen
    screen.blit(texttit1,(margin,40))
    screen.blit(textang1,(margin,80))
    screen.blit(textang2,(margin,110))
    screen.blit(texttit2,(margin,160))
    screen.blit(textcursor,(margin,200))
    screen.blit(texttit3,(margin,250))
    screen.blit(texttime,(margin,290))
    #Draw buttons on the right side of screen
    #Configuration for button 1
    if margin < globmx < margin+100 and 600 < globmy < 600+50:
        pygame.draw.rect(screen,YELLOW,(margin,600,100,50))
        if clicked[0] == 1:
            timerrun=True
    else:
        pygame.draw.rect(screen,GREEN,(margin,600,100,50))
    if timerrun == False:
        screen.blit(textbut1,(margin+10,610))
    else:
        screen.blit(textbut2,(margin+10,610))
    #Configuration for button 2
    pygame.draw.rect(screen,RED,(margin+120,600,70,50))
    screen.blit(textbut3,(margin+130,610))
    if margin+130 < globmx < margin+230 and 600 < globmy < 600+50:
        if clicked[0] == 1:
            timerrun=False
            seconds=0
    #Draw image objects in map
    screen.blit(cursor,(arrowx,arrowy))
    screen.blit(circul,(coordx-30,coordy-30))
    #Draw text for angles insode circle
    screen.blit(textcircshad,(coordx-9,coordy+1))
    screen.blit(textcirc,(coordx-10,coordy))
    #Time is being counted
    clock.tick()
    
    
    

