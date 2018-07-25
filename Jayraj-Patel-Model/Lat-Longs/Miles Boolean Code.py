# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 09:39:06 2018

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

def tfcheck (comp_df, miles_radius):
    miles_comp = []
    for m in range(0,1276):
        comp_list = comp_df.values[m,:]<miles_radius
        if True in comp_list:
            miles_comp.append(1)
        else:
            miles_comp.append(0)
    #print(miles_comp)
    return miles_comp

#answer = tfcheck(miniso_df, 1)
#print(answer)

###-------Code for 1 mile radius-------###
one_miniso = tfcheck(miniso_df, 1)
one_pagoda = tfcheck(pagoda_df, 1)
one_hm = tfcheck(hm_df, 1)
one_zara = tfcheck(zara_df, 1)
one_justice = tfcheck(justice_df, 1)

###-------Code for 5 mile radius-------###
five_miniso = tfcheck(miniso_df, 5)
five_pagoda = tfcheck(pagoda_df, 5)
five_hm = tfcheck(hm_df, 5)
five_zara = tfcheck(zara_df, 5)
five_justice = tfcheck(justice_df, 5)
    
###-------Code for 10 mile radius-------###
ten_miniso = tfcheck(miniso_df, 10)
ten_pagoda = tfcheck(pagoda_df, 10)
ten_hm = tfcheck(hm_df, 10)
ten_zara = tfcheck(zara_df, 10)
ten_justice = tfcheck(justice_df, 10)

one_mile_list_df = pd.DataFrame(index = range(0,1276))
#mile_list_df["Store #"] = claires_df["Store ID"]    
one_mile_list_df["Justice (<1)"] = one_justice
one_mile_list_df["Piercing Pagoda (<1)"] = one_pagoda
one_mile_list_df["Miniso (<1)"] = one_miniso
one_mile_list_df["H&M (<1)"] = one_hm
one_mile_list_df["Zara (<1)"] = one_zara
one_density = []
for x in range(0,1276):
    one_comp_density = one_mile_list_df.values[x,:].sum()
    one_density.append(one_comp_density)
one_mile_list_df["Competitor Density (<1)"] = one_density
one_mile_list_df["Store_Number"] = claires_df["Store ID"]
one_mile_list_df = one_mile_list_df[["Store_Number", "Justice (<1)", "Piercing Pagoda (<1)", "Miniso (<1)", "H&M (<1)", 
                                     "Zara (<1)", "Competitor Density (<1)"]]
                 
five_mile_list_df = pd.DataFrame(index = range(0,1276))
five_mile_list_df["Justice (<5)"] = five_justice
five_mile_list_df["Piercing Pagoda (<5)"] = five_pagoda
five_mile_list_df["Miniso (<5)"] = five_miniso
five_mile_list_df["H&M (<5)"] = five_hm
five_mile_list_df["Zara (<5)"] = five_zara
five_density = []
for x in range(0,1276):
    five_comp_density = five_mile_list_df.values[x,:].sum()
    five_density.append(five_comp_density)
five_mile_list_df["Competitor Density (<5)"] = five_density
five_mile_list_df["Store_Number"] = claires_df["Store ID"]
five_mile_list_df = five_mile_list_df[["Store_Number", "Justice (<5)", "Piercing Pagoda (<5)", "Miniso (<5)", "H&M (<5)", 
                                       "Zara (<5)", "Competitor Density (<5)"]]

ten_mile_list_df = pd.DataFrame(index = range(0,1276))
ten_mile_list_df["Justice (<10)"] = ten_justice
ten_mile_list_df["Piercing Pagoda (<10)"] = ten_pagoda
ten_mile_list_df["Miniso (<10)"] = ten_miniso
ten_mile_list_df["H&M (<10)"] = ten_hm
ten_mile_list_df["Zara (<10)"] = ten_zara
ten_density = []
for x in range(0,1276):
    ten_comp_density = ten_mile_list_df.values[x,:].sum()
    ten_density.append(ten_comp_density)
ten_mile_list_df["Competitor Density (<10)"] = ten_density
ten_mile_list_df["Store_Number"] = claires_df["Store ID"]
ten_mile_list_df = ten_mile_list_df[["Store_Number", "Justice (<10)", "Piercing Pagoda (<10)", "Miniso (<10)", "H&M (<10)", 
                                     "Zara (<10)", "Competitor Density (<10)"]]

#column_list = ["Justice (<1)", "Justice (<5)", "Justice (<10)", "Piercing Pagoda (<1)", "Piercing Pagoda (<5)", "Piercing Pagoda (<10)",
#               "Miniso (<1)", "Miniso (<5)", "Miniso (<10)", "H&M (<1)", "H&M (<5)", "H&M (<10)", "Zara (<1)", "Zara (<5)", "Zara (<10)"]
merge_one_df = pd.merge(one_mile_list_df, five_mile_list_df, how='left', on=['Store_Number'])
merge_one_df.shape
merge_all_df = pd.merge(merge_one_df, ten_mile_list_df, how='left', on=['Store_Number'])
merge_all_df.shape
#merge_all_df["Store #"] = claires_df["Store ID"]
#mile_list_df = mile_list_df[["Store #", "Justice (<1)", "Piercing Pagoda (<1)", "Miniso (<1)", "H&M" "Piercing Pagoda (<5)", 
#                             "Piercing Pagoda (<10)", "Miniso (<1)", "Miniso (<5)", "Miniso (<10)", "H&M (<1)", "H&M (<5)", "H&M (<10)", 
#                             "Zara (<1)", "Zara (<5)", "Zara (<10)", "Competitor Density"]]

writer = pd.ExcelWriter('Miles Radius Analysis-Boolean.xlsx', engine='xlsxwriter')
merge_all_df.to_excel(writer, sheet_name='Miles Radius Analysis')
writer.save()

