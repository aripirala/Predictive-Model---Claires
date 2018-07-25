# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 09:44:48 2018

@author: patelj
"""

from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import numpy as np

FILE_PATH_INPUT = 'C:/Users/patelj/Documents/Lat-Longs/'
FILE_PATH_OUTPUT = 'C:/Users/patelj/Documents/Lat-Longs/Zara Analysis/'

R = 6373.0
zara_df = pd.read_excel(FILE_PATH_INPUT+'Zara-Lat-Long.xlsx', sheetname='Data')
claires_df = pd.read_excel(FILE_PATH_INPUT+'NA-Lat-Longs.xlsm', sheetname='Data')

###-------Test Code for one set of coordinates-------###
#lat1 = claires_df["Latitude"].values[1274]
#lon1 = claires_df["Longitude"].values[1274]
#lat2 = miniso_df["Latitude"].values[11]
#lon2 = miniso_df["Longitude"].values[11]
#lat1 = radians(lat1)
#lon1 = radians(lon1)
#lat2 = radians(lat2)
#lon2 = radians(lon2)
#dlon = lon2 - lon1
#dlat = lat2 - lat1

#a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
#c = 2 * atan2(sqrt(a), sqrt(1 - a))

#distance = R * c

#print("Result:", distance)
###-------End Test Code-------###

dist_list = []
#dist_output_df = pd.DataFrame(index=claires_df.index)
for x in range(0,1276):
    lat1 = claires_df["Latitude"].values[x]
    lon1 = claires_df["Longitude"].values[x]
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    for i in range(0,69):
        lat2 = zara_df["Latitude"].values[i]
        lon2 = zara_df["Longitude"].values[i]
        lat2 = radians(lat2)
        lon2 = radians(lon2)
    
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        miles_dist = distance * 0.621371

        print("Result:", miles_dist)
        dist_list.append(miles_dist)

new_list = np.array(dist_list)
new_list = new_list.reshape(1276,69)

dist_output_df = pd.DataFrame(new_list)        
dist_output_df.to_excel(FILE_PATH_OUTPUT+'Zara Distance Output.xlsx')
