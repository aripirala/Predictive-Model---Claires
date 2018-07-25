# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 11:10:25 2018

@author: patelj
"""
from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import numpy as np

FILE_PATH_INPUT = 'C:/Users/patelj/Documents/Lat-Longs/'
FILE_PATH_OUTPUT = 'C:/Users/patelj/Documents/Lat-Longs/'

def dist_output(file_name):
    R = 6373.0
    comp_df = pd.read_excel(FILE_PATH_INPUT+file_name, sheetname='Data')
    claires_df = pd.read_excel(FILE_PATH_INPUT+'NA-Lat-Longs.xlsm', sheetname='Data')

    dist_list = []
    #dist_output_df = pd.DataFrame(index=claires_df.index)
    for x in range(len(claires_df.index)):
        lat1 = claires_df["Latitude"].values[x]
        lon1 = claires_df["Longitude"].values[x]
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        for i in range(len(comp_df.index)):
            lat2 = comp_df["Latitude"].values[i]
            lon2 = comp_df["Longitude"].values[i]
            lat2 = radians(lat2)
            lon2 = radians(lon2)
    
            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
            miles_dist = distance * 0.621371

            #print("Result:", miles_dist)
            dist_list.append(miles_dist)

    new_list = np.array(dist_list)
    new_list = new_list.reshape(len(claires_df.index),len(comp_df.index))

    dist_output_df = pd.DataFrame(new_list)        
    dist_output_df.to_excel(FILE_PATH_OUTPUT+'Competitor Distance Output.xlsx')
    
##########################################################################################
    
dist_output("Miniso-Lat-Long.xlsx")
