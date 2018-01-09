# -*- coding: utf-8 -*-
"""
Created on Fri Jan 05 19:13:35 2018

@author: esteb
"""

import csv

original = file('angles2.csv')
reader = csv.reader(original)
ejemplo = reader.next()
ejemplo2 = reader.next()

for row in reader:
    #will print each row by itself (all columns from names up to what they wear)
    print row
    print "-----------------"
    #will print first column (character names only)
    #print row[1]
