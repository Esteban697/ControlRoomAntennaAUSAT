# -*- coding: utf-8 -*-
"""
Created on Tue Jan 09 11:59:51 2018

@author: Esteban Struve
"""
import csv

#Define limits for the range of angles of Azimuth and Elevation
firstaz=0
lastaz=360
minelev=0
maxelev=180
#Build the ranges
angaz=range(firstaz,lastaz+1) #for Azimuth
angelev=range(minelev,maxelev+1) #for Elevation
#Save data into a single csv file
myData = [angaz, angelev]  
myFile = open('angles.csv', 'w')  
with myFile:  
   writer = csv.writer(myFile)
   writer.writerows(myData)
print "Data saved"