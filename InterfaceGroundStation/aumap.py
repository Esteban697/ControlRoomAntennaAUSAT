# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:07:20 2017

@author: Esteban Struve
"""
"""*******************************Libraries********************************"""
import pygame, sys 
from pygame.locals import *
import math
import csv
"""*********************Reading angle information**************************"""
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
"""***************************Initialization*******************************"""
#Start the pygame interface
pygame.init()
#Initialize values for the VISUAL INTERFACE
# Define the COLORS we will use in RGB format
YELLOW= (255, 255,   0)
BLUE =  (  0,   0, 255)
BLUE2 = (204, 222, 243)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
ORANGE= (255, 154,   0)
BLACK = (  0,   0,   0)
GREY1 = (200, 200, 200)
GREY2 = (50, 50, 50)
GREY3 = (80, 80, 80)
#Setting screen
mapsize = width, height = 850,850
screensize = 1500,850
screen = pygame.display.set_mode(screensize)
#Scaling of map with respect to angles
scalex=(width/2)
scaley=(height/2)
#Setting margins in screen
margtextx,margtexty = width+170,80
margswitchx,margswitchy = width+40,140
margmodex,margmodey = width+50,(height/2)+100
margsw1x,margsw1y = margmodex+110,margmodey+40
margin=0
#Initializing variables for visual objects
m=0
ind1=0 #indexes to point to data in csv file
ind2=0
coordx,coordy=0,0 #for map
mousex,mousey=0,0
mxdisp,mydisp=0,0
mxfixed,myfixed=0,0
movex, movey=0,0
endx,endy=0,0
opx,opy=0,0
slope=0
angledeg=0
elevang=0
seconds=0 #for time
timer=0
timerdisp=0
#Fonts for text
myfont=pygame.font.SysFont("Arial Black",20)
myfont2=pygame.font.Font(None,20)
#Create and load text for right side of screen
texttit1=myfont.render("Angle values:",0,ORANGE)
texttit2=myfont.render("Position of cursor:",0,ORANGE)
texttit3=myfont.render("Time:",0,ORANGE)
textbut1=myfont.render("Play",0,BLACK)
textbut2=myfont.render("Playing",0,BLACK)
textbut3=myfont.render("Stop",0,BLACK)
textbut4=myfont.render("Reset",0,BLACK)
textmanual1=myfont.render("Use the arrow keys",0,GREY1)
textmanual2=myfont.render("to navigate de values",0,GREY1)
textcursor1=myfont.render("Right-clik map to save location",0,GREY1)
textcursor2=myfont.render("Right-clik map to drop location",0,GREY1)
#Start clock
clock=pygame.time.Clock()
#Booleans for states
boolmode=True
boolzoom=True
timerrun=False
boolcursor=True
"""*************************Pygame While Loop******************************"""
while True:
    if timerrun == True:
        #Measuring time enlapsed
        seconds=clock.get_time()/1000.0
        timer+=seconds
        timerdisp=math.trunc(timer)
    #Events in the loop
    for event in pygame.event.get():
        #Exit execution when closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
            """******************ARROW KEYS********************************"""
        #Using the arrow keys to change de direction angle if in Manual Mode
        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:#When left key gets pressed
                if boolmode == True:
                    if ind1 > 0: #safe limits for index
                        ind1-=1
            elif event.key == K_RIGHT: #when right key gets pressed
                if boolmode == True:
                    if ind1 <(len(listang)-1): #safe limits for index
                        ind1+=1
            #You can use the up-down keys to change de inclination angle
            elif event.key == K_UP: #When up key gets pressed
                if boolmode == True:
                    if ind2 > 0: #safe limits for index
                        ind2-=1
            elif event.key == K_DOWN: #when down key gets pressed
                if boolmode == True:
                    if ind2 <(len(listincl)-1): #safe limits for index
                        ind2+=1
    """****************************MOUSE************************************"""
    #Get information from the mouse
    clicked=pygame.mouse.get_pressed() #gets the buttons information
    mousex,mousey=pygame.mouse.get_pos() #gets the position of the cursor
    globmx,globmy=mousex,mousey
    #coordinates inside the map
    if mousex > width:
        mousex=width
    elif mousex < 0:
        mousex=0
    if mousey > height:
        mousey=height
    elif mousey < 0:
        mousey=0
    #Update the displayed coordinates only when cursor inside the map
    if 0 < mousex < width and 0 < mousey < height:
        if clicked[2]==0:
            mxdisp=mousex
            mydisp=mousey
        else:
            mxfixed=mousex
            myfixed=mousey
            if boolcursor==True:
                boolcursor=False
            else:
                boolcursor=True
    #coordinates for cursor arrow to allign to arrow tip
    arrowx=mxdisp-10
    arrowy=mydisp-20
    """*******************SELECT ANGLE INFORMATION**************************"""
    #If in Auto Mode the indexes are set by the clock
    if boolmode==False:
        ind1,ind2=timerdisp,timerdisp
    #Choose an angle and slope from the list created by the csv file
    angledeg=azangles[ind1]
    slope=slopel[ind1]
    elevang=elevangles[ind2]
    """*****************Calculate Lines and Target**************************"""
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
        coordx=(width/2)-(math.sin(math.radians(angledeg)))*((scalex)*((90-elevang)/90))
        coordy=(height/2)-(math.cos(math.radians(angledeg)))*((scaley)*((90-elevang)/90))
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
        coordx=(width/2)-(math.sin(math.radians(angledeg)))*((scalex)*((90-elevang)/90))
        coordy=(height/2)-(math.cos(math.radians(angledeg)))*((scaley)*((90-elevang)/90))
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
            coordx=(width/2)-(math.sin(math.radians(angledeg)))*((scalex)*((90-elevang)/90))
            coordy=(height/2)-(math.cos(math.radians(angledeg)))*((scaley)*((90-elevang)/90))
    #When angle between 270 and 360
    elif angledeg <= 360.0:
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
            coordx=(width/2)-(math.sin(math.radians(angledeg)))*((scalex)*((90-elevang)/90))
            coordy=(height/2)-(math.cos(math.radians(angledeg)))*((scaley)*((90-elevang)/90))
    """**********************Loading image objects**************************"""
    pygame.display.set_caption("Ground Station")
    if boolzoom == True:
        layer = pygame.image.load("mapin.png")
        scalex=(width/2)*2
        scaley=(height/2)*2
    else:
        layer = pygame.image.load("mapout.png")
        scalex=(width/2)*1.2
        scaley=(height/2)*1.2
    cursor=pygame.image.load("arrow.png")
    margmarkx1=pygame.image.load("marginmarkerx1.png")
    margmarkx2=pygame.image.load("marginmarkerx2.png")
    margmarky1=pygame.image.load("marginmarkery1.png")
    margmarky2=pygame.image.load("marginmarkery2.png")
    circul=pygame.image.load("bluecircle.png")
    switch1=pygame.image.load("switch1.png")
    switch2=pygame.image.load("switch2.png")
    switch3=pygame.image.load("switch3.png")
    switch4=pygame.image.load("switch4.png")
    """*************************UPDATE SCREEN*******************************"""
    pygame.display.update()
    #Update text
    textang1=myfont.render("Azimut: "+str(angledeg)+" degrees",0,GREEN)
    textang2=myfont.render("Elevation: "+str(elevang)+" degrees",0,BLUE2)
    if boolcursor==True: 
        textcursor=myfont.render("X: "+str(mxdisp)+" Y: "+str(mydisp),0,YELLOW)
    else:#Freezes coordinates when saving location
        textcursor=myfont.render("X: "+str(mxfixed)+" Y: "+str(myfixed)+" fixed",0,YELLOW)
    texttime=myfont.render(str(timerdisp)+" seconds",0,YELLOW)
    #Black background
    screen.fill(GREY2)
    """***************************DRAWING MAP*******************************"""
    #Draw map
    screen.blit(layer,(0,0))
    #Draw information boxes
    pygame.draw.rect(screen,GREY3,(margtextx-50,margtexty-50,450,450))
    pygame.draw.rect(screen,GREY3,(margmodex,margmodey,520,200))
    #Draw the lines
    pygame.draw.line(screen,YELLOW,(width/2,height/2),(opx,opy),3)
    pygame.draw.line(screen,GREEN,(width/2,height/2),(endx,endy),3)
    #Draw cursor margin markers
    if boolcursor==True:
        screen.blit(margmarkx1,(0,mydisp-11))
        screen.blit(margmarkx2,(width-30,mydisp-11))
        screen.blit(margmarky1,(mxdisp-11,0))
        screen.blit(margmarky2,(mxdisp-11,height-30))
    else: #Freeze margin markers
        screen.blit(margmarkx1,(0,myfixed-11))
        screen.blit(margmarkx2,(width-30,myfixed-11))
        screen.blit(margmarky1,(mxfixed-11,0))
        screen.blit(margmarky2,(mxfixed-11,height-30))
    """***************************DRAWING TEXT******************************"""
    #Draw text on the right side of the screen
    screen.blit(texttit1,(margtextx,margtexty))
    screen.blit(textang1,(margtextx,margtexty+40))
    screen.blit(textang2,(margtextx,margtexty+80))
    screen.blit(texttit2,(margtextx,margtexty+130))
    screen.blit(textcursor,(margtextx,margtexty+170))
    if boolcursor==True: #Changes text according to cursor mode
        screen.blit(textcursor1,(margtextx,margtexty+220))
    else:
        screen.blit(textcursor2,(margtextx,margtexty+220))
    screen.blit(texttit3,(margtextx,margtexty+260))
    screen.blit(texttime,(margtextx,margtexty+300))
    """***************************SWITCHES*********************************"""
    #Configuration of switch 1 "Change Mode"
    if margsw1x < globmx < margsw1x+150 and margsw1y < globmy < margsw1y+50:
        if clicked[0] == 1:
            boolmode=True 
    if margsw1x+150 < globmx < margsw1x+300 and margsw1y < globmy < margsw1y+50:
        if clicked[0] == 1:
            boolmode=False
    if boolmode == True:
        screen.blit(switch1,(margsw1x,margsw1y))
    else:
        screen.blit(switch2,(margsw1x,margsw1y))
    #Configuration of switch 2 "Zoom Map"
    if margswitchx < globmx < margswitchx+50 and margswitchy < globmy < margswitchx+150:
        if clicked[0] == 1:
            boolzoom=True
            boolcursor=True #Drops location when map changes
    if margswitchx < globmx < margswitchx+50 and margswitchy+150 < globmy < margswitchy+300:
        if clicked[0] == 1:
            boolzoom=False
            boolcursor=True #Drops location when map changes
    if boolzoom == True:
        screen.blit(switch3,(margswitchx,margswitchy))
    else:
        screen.blit(switch4,(margswitchx,margswitchy))
    """****************************BUTTONS**********************************"""
    #Configuration for button 1
    if boolmode == False: #In Auto Mode
        pygame.draw.rect(screen,GREEN,(margmodex+110,margmodey+110,100,50))
        if margmodex+110 < globmx < margmodex+210 and margmodey+110 < globmy < margmodey+160:
            if clicked[0] == 1:
                timerrun=True
        if timerrun == False:
            screen.blit(textbut1,(margmodex+120,margmodey+120))
        else:
            pygame.draw.rect(screen,YELLOW,(margmodex+110,margmodey+110,100,50))
            screen.blit(textbut2,(margmodex+120,margmodey+120))
        #Configuration for button 2
        pygame.draw.rect(screen,RED,(margmodex+220,margmodey+110,70,50))
        screen.blit(textbut3,(margmodex+230,margmodey+120))
        if margmodex+220 < globmx < margmodex+290 and margmodey+120 < globmy < margmodey+170:
            if clicked[0] == 1:
                timerrun=False #Stop clock
                seconds=0
        #Configuration for button 3
        pygame.draw.rect(screen,BLUE,(margmodex+300,margmodey+110,100,50))
        screen.blit(textbut4,(margmodex+320,margmodey+120))
        if margmodex+310 < globmx < margmodex+410 and margmodey+120 < globmy < margmodey+170:
            if clicked[0] == 1:
                timerrun=False
                #Reset clock
                seconds=0
                timer=0 
                timerdisp=0
    else:
        screen.blit(textmanual1,(margmodex+160,margmodey+110))
        screen.blit(textmanual2,(margmodex+150,margmodey+140))
    """*****************************CURSOR*********************************"""
    #Draw cursor in map
    if boolcursor==True:
        screen.blit(cursor,(arrowx,arrowy))
    else:
        screen.blit(cursor,(mxfixed-10,myfixed-20))
    """****************************TARGET**********************************"""
    #Create angle value inside circle
    textcirc=myfont2.render(str(int(elevang)),0,BLUE2)
    textcircshad=myfont2.render(str(int(elevang)),0,BLACK)
    #Draw pointing circle in map
    if coordx < 0 or coordy < 0: #if target out of map
        coordx=endx
        coordy=endy #target circle stays in ending of line
    if coordx > width or coordy > height: #if tager out of map
        coordx=endx
        coordy=endy #target circle stays in ending of line
    screen.blit(circul,(coordx-30,coordy-30))
    #Draw text for angles insode circle
    screen.blit(textcircshad,(coordx-9,coordy+1))
    screen.blit(textcirc,(coordx-10,coordy))
    """**************************TIME OF LOOP******************************"""
    #Time is being counted
    clock.tick()
    
    
    

