# -*- coding: utf-8 -*-
"""
Created on Tue Jan 09 11:59:51 2018

@author: esteban struve
"""
import csv

angdir=range(50,101)
angincl=range(0,181)

myData = [angdir, angincl]  
myFile = open('angles2.csv', 'w')  
with myFile:  
   writer = csv.writer(myFile)
   writer.writerows(myData)
