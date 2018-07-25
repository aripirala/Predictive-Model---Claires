# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:35:44 2018

@author: patelj
"""

import pandas as pd


FILE_PATH_INPUT = 'C:/Users/patelj/Documents/Lat-Longs/'
FILE_PATH_OUTPUT = 'C:/Users/patelj/Documents/Lat-Longs/'

R = 6373.0
miniso_df = pd.read_excel(FILE_PATH_INPUT+'Miniso Analysis/Miniso Distance Output.xlsx', sheetname='Sheet1')
claires_df = pd.read_excel(FILE_PATH_INPUT+'NA-Lat-Longs.xlsm', sheetname='Data')
pagoda_df = pd.read_excel(FILE_PATH_INPUT+'Pagoda Analysis/Pagoda Distance Output.xlsx', sheetname='Sheet1')
hm_df = pd.read_excel(FILE_PATH_INPUT+'HM Analysis/H&M Distance Output.xlsx', sheetname='Sheet1')
zara_df = pd.read_excel(FILE_PATH_INPUT+'Zara Analysis/Zara Distance Output.xlsx', sheetname='Sheet1')
justice_df = pd.read_excel(FILE_PATH_INPUT+'Justice Analysis/Justice Distance Output.xlsx', sheetname='Sheet1')

one_miniso = []
one_pagoda = []
one_hm = []
one_zara = []
one_justice = []
###-------Code for 1 mile radius-------###
for m in range(0,1276):    
    miniso_list = (miniso_df.values[m,:]<1).sum()
    pagoda_list = (pagoda_df.values[m,:]<1).sum()
    hm_list = (hm_df.values[m,:]<1).sum()
    zara_list = (zara_df.values[m,:]<1).sum()
    justice_list = (justice_df.values[m,:]<1).sum()
    one_miniso.append(miniso_list)
    one_pagoda.append(pagoda_list)
    one_hm.append(hm_list)
    one_zara.append(zara_list)
    one_justice.append(justice_list)
    
one_mile_list_df = pd.DataFrame(index = range(len(one_miniso)))
one_mile_list_df["Store Number"] = claires_df["Store ID"]    
one_mile_list_df["Justice"] = one_justice
one_mile_list_df["Piercing Pagoda"] = one_pagoda
one_mile_list_df["Miniso"] = one_miniso
one_mile_list_df["H&M"] = one_hm
one_mile_list_df["Zara"] = one_zara

five_miniso = []
five_pagoda = []
five_hm = []
five_zara = []
five_justice = []
###-------Code for 5 mile radius-------###
for m in range(0,1276):    
    miniso_list = (miniso_df.values[m,:]<5).sum()
    pagoda_list = (pagoda_df.values[m,:]<5).sum()
    hm_list = (hm_df.values[m,:]<5).sum()
    zara_list = (zara_df.values[m,:]<5).sum()
    justice_list = (justice_df.values[m,:]<5).sum()
    five_miniso.append(miniso_list)
    five_pagoda.append(pagoda_list)
    five_hm.append(hm_list)
    five_zara.append(zara_list)
    five_justice.append(justice_list)
    
five_mile_list_df = pd.DataFrame(index = range(len(five_miniso)))
five_mile_list_df["Store Number"] = claires_df["Store ID"]    
five_mile_list_df["Justice"] = five_justice
five_mile_list_df["Piercing Pagoda"] = five_pagoda
five_mile_list_df["Miniso"] = five_miniso
five_mile_list_df["H&M"] = five_hm
five_mile_list_df["Zara"] = five_zara

ten_miniso = []
ten_pagoda = []
ten_hm = []
ten_zara = []
ten_justice = []
###-------Code for 10 mile radius-------###
for m in range(0,1276):    
    miniso_list = (miniso_df.values[m,:]<10).sum()
    pagoda_list = (pagoda_df.values[m,:]<10).sum()
    hm_list = (hm_df.values[m,:]<10).sum()
    zara_list = (zara_df.values[m,:]<10).sum()
    justice_list = (justice_df.values[m,:]<10).sum()
    ten_miniso.append(miniso_list)
    ten_pagoda.append(pagoda_list)
    ten_hm.append(hm_list)
    ten_zara.append(zara_list)
    ten_justice.append(justice_list)
    
ten_mile_list_df = pd.DataFrame(index = range(len(ten_miniso)))
ten_mile_list_df["Store Number"] = claires_df["Store ID"]    
ten_mile_list_df["Justice"] = ten_justice
ten_mile_list_df["Piercing Pagoda"] = ten_pagoda
ten_mile_list_df["Miniso"] = ten_miniso
ten_mile_list_df["H&M"] = ten_hm
ten_mile_list_df["Zara"] = ten_zara

writer = pd.ExcelWriter('Miles Radius Analysis.xlsx', engine='xlsxwriter')
one_mile_list_df.to_excel(writer, sheet_name='<1 Mile')
five_mile_list_df.to_excel(writer, sheet_name='<5 Miles')
ten_mile_list_df.to_excel(writer, sheet_name='<10 Miles')
writer.save()

