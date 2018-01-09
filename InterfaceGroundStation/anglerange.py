# -*- coding: utf-8 -*-
"""
Created on Tue Jan 09 11:59:51 2018

@author: esteban struve
"""
import csv
#Define limits for the range of angles of direction and inclination
firstdirec=70
lastdirec=100
minang=0
maxang=180
#Build the ranges
angdir=range(firstdirec,lastdirec+1)
angincl=range(minang,maxang+1)
#Store data into a single csv file
myData = [angdir, angincl]  
myFile = open('angles2.csv', 'w')  
with myFile:  
   writer = csv.writer(myFile)
   writer.writerows(myData)
print "Data saved"
